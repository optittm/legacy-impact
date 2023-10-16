import dbm  # Python native key/value persisted DB
import dbm.ndbm
import pickle
from typing import Any, Dict, List, Union  # Python serializer
import tqdm  # Progressbar in the terminal
import lizard  # Static file Anaylyzer
from lizard_languages import (
    languages,
    get_reader_for,
)  # Detect the programming language of a source code file
import hashlib  # To hash the function content with sha256
import os  # Check if file exists, list folder content
import click  # Command line interface
import time
import concurrent.futures  # For concurrent coding
import threading  # For threading with Python
from sentence_transformers import SentenceTransformer, util  #
from transformers import AutoModel, AutoTokenizer  #

# Program config
checkpoint = "Salesforce/codet5p-220m-bimodal"
device = "cpu"
tokenizer = None
codeT5 = None
bert = None
folder = None
db = None
supported_langs = ["go", "js", "php", "java", "ruby", "python"]


TOKEN_LIMIT = 512

def code_to_natural_text(code_body: str) -> str:
    """Convert a piece of code into a summary readable by a human

    Parameters
    ----------
    code_body : str
        The content of the code

    Returns
    -------
    str
        the description of the code content in natural language

    Raises
    ------
    NotImplementedError
        If the number of tokens is higher than TOKEN_LIMIT
    """
    input_ids = tokenizer(code_body, return_tensors="pt").input_ids.to(device)
    generated_ids = codeT5.generate(input_ids, max_length=20)
    if len(generated_ids) > TOKEN_LIMIT:
        raise NotImplementedError(f"The number of tokens is higher than {TOKEN_LIMIT}")
    return tokenizer.decode(generated_ids[0], skip_special_tokens=True)


def extract_function_body(fun_info: lizard.FunctionInfo) -> str:
    """Extract the code content of a function (its body)

    Parameters
    ----------
    fun_info : lizard.FunctionInfo
        Function object returned by Lizard static analyzer

    Returns
    -------
    str
        the body of the function
    """
    with open(fun_info.filename, "r") as fp:
        line_numbers = range(fun_info.start_line, fun_info.end_line)
        lines = []
        for i, line in enumerate(fp):
            if i in line_numbers:
                lines.append(line.strip())
            elif i > fun_info.end_line:
                break
        return " ".join(lines)


def get_hash(text: str) -> str:
    """Get the hash of a string with sha256

    Parameters
    ----------
    text : str
        The content of the string

    Returns
    -------
    str
        the hexadecimal representation of the hash
    """
    m = hashlib.sha256()
    m.update(bytes(text, "utf-8"))
    return m.hexdigest()


def process_function(fun_info: lizard.FunctionInfo) -> str:
    """Process function (concurrent programming)
    Check

    Parameters
    ----------
    text : str
        The content of the text

    Returns
    -------
    str
        the function name processed
    """
    start = time.time()
    if fun_info.token_count <= TOKEN_LIMIT:
        body = extract_function_body(fun_info)
        hash = get_hash(body)
        # print(body)
        # check if it is already into the dictionary
        if hash not in db:
            description = code_to_natural_text(body)
            # TODO : assess the opportunity to get and store the simhash : features = get_features(body)
            entry = {
                "filename": fun_info.filename,
                "long_name": fun_info.long_name,
                "start_line": fun_info.start_line,
                "end_line": fun_info.end_line,
                "body": body,
                "description": description,
            }
            db[hash] = pickle.dumps(entry)
        else:
            return "Function <" + fun_info.name + "> was already analyzed."
    else:
        return f"Function <{fun_info.name}> exceeds {TOKEN_LIMIT} tokens."
    end = time.time()
    elapsed_time = end - start
    return (
        "Function <"
        + fun_info.name
        + "> analyzed in "
        + str(elapsed_time)
        + " seconds."
    )


@click.group()
@click.pass_context
def cli(ctx):
    """A CLI tool to assess the impact of a change on files"""
    pass


@cli.command()
@click.option("--database", help="Database name")
@click.pass_context
def head(ctx, database):
    """Display the first 10 entries of the database

    Args:
        database (_type_): Full path to the database
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    db_filename = os.path.join(dir_path, "data/", database)
    # if os.path.exists(db_filename):
    print("Displaying the first 10 entries of the database: " + db_filename)
    print("Database type:" + dbm.whichdb(db_filename))
    with dbm.ndbm.open(db_filename, "r") as db:
        keys = db.keys()
        for i, k in enumerate(keys):
            if i < 10:
                entry = pickle.loads(db[k])
                print(
                    "-----------------------------------------------------------------------------"
                )
                print(
                    entry["filename"]
                    + ":"
                    + str(entry["start_line"])
                    + " - "
                    + str(entry["end_line"])
                    + "   "
                    + entry["long_name"]
                )
                print(entry["description"])
                print(
                    "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                )
                print(entry["body"])
                print(
                    "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                )
        if len(keys) == 0:
            print("The database is empty")


@cli.command()
@click.option("--database", help="Database name")
@click.option("--text", help="Text to search")
@click.option("--textfile", help="Text to search stored in file")
@click.option(
    "--maxentries",
    default=10,
    type=click.IntRange(min=1),
    help="Number of entries to retrieve",
    show_default=True,
)
@click.option(
    "--confidence",
    default=None,
    type=click.FloatRange(min=0),
    help="Minimum tensor confidence",
)
@click.pass_context
def lookup(
    ctx, database: str, text: str, textfile: str, maxentries: int, confidence: Union[float, None]
):
    """Finds the functions that are the closest to the text
    using cosine distance between the text and the computed description


    Args:
        database (_type_): Full path to the database
    """

    # storing entries linked to similarity
    # {"simA": [entryA, entryB], "simB": [entryC], ...}
    similarities: Dict[str, List[Any]] = {}

    if textfile is not None:
        with open(textfile, "r", encoding="utf-8") as textfile_read:
            text = textfile_read.read()

    print(f"==\nSearching similarities from text {text}\n==")

    db_filename = os.path.join("./data/", database)
    if os.path.exists(db_filename + ".db"):
        bert = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        with dbm.ndbm.open(db_filename, "r") as db:
            keys = db.keys()

            if len(keys) == 0:
                print("The database is empty")
                return

            for i, k in enumerate(keys):
                entry = pickle.loads(db[k])

                # Compute embedding for both lists
                embedding_1 = bert.encode(text, convert_to_tensor=True)
                embedding_2 = bert.encode(entry["description"], convert_to_tensor=True)

                similarity = util.pytorch_cos_sim(embedding_1, embedding_2)

                # store similarity with given entry
                # note : An entry can have the same similarity as another entry

                if similarities.get(similarity) is None:
                    similarities[similarity] = [entry]
                else:
                    similarities[similarity].append(entry)

            # Retrieve highest <maxentries> similarities
            similarities_desc = sorted(similarities.keys(), reverse=True)

            # NOTE filter before sort is better for perf
            if confidence is not None:
                similarities_desc = list(
                    filter(
                        lambda tensor: tensor.item() > confidence, similarities_desc
                    )
                )
                print(f"{similarities_desc}")

            # We need to do this if there is multiple entries with same similarity
            # if maxentries is 1 and 2 entries have the same similarity we display both entries

            display_index = 0

            while display_index < maxentries and display_index < len(
                similarities_desc
            ):
                similarity = similarities_desc[display_index]
                entries = similarities[similarity]

                for entry in entries:
                    print(
                        "\n"
                        f"Similarity  : {similarity}\n"
                        f"File        : {entry['filename']}:{entry['start_line']}\n"
                        f"Name        : {entry['long_name']}\n"
                        f"Description : {entry['description']}\n"
                    )
                    display_index += 1
    else:
        raise FileNotFoundError(f"Can not find database {db_filename}.db")


@cli.command()
@click.option("--folder", help="Folder where the sources are stored")
@click.option("--database", help="database name")
@click.pass_context
def analyze(ctx, folder, database):
    """Analyse the source code contained in folder

    Args:
        folder (_type_): Full path to the source code
    """
    global tokenizer
    global codeT5
    global db
    tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
    codeT5 = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to(device)

    db_filename = os.path.join("./data/", database)

    with dbm.ndbm.open(db_filename, "c") as db:
        files = lizard.analyze([folder])  # TODO : Add exclude pattern
        for file in files:
            # TODO : looks like we have a way to filter the language:
            # reader = get_reader_for(file.filename)
            print(
                file.filename
                + " has "
                + str(len(file.function_list))
                + " functions to analyze"
            )
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for function in file.function_list:
                    futures.append(executor.submit(process_function, fun_info=function))
                for future in concurrent.futures.as_completed(futures):
                    print(future.result())


if __name__ == "__main__":
    cli(obj={})
