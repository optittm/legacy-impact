
#from pygments.lexers import get_lexer_for_filename
#from pygments.token import Token
#from autocorrect import Speller
#import spacy
#from scispacy.abbreviation import AbbreviationDetector
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
#import fasttext
import string

# TODO: refactor :)
#nlp = spacy.load("en_core_web_sm")
#nlp.add_pipe("abbreviation_detector")
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('stopwords')

def replace_acronyms(text):
    doc = nlp(text)
    altered_tok = [tok.text for tok in doc]
    for abrv in doc._.abbreviations:
        altered_tok[abrv.start] = str(abrv._.long_form)
    return " ".join(altered_tok)


def split_function_name(s):
    """Splits a function name into diferent words, e.g.:
        thisIsMyVariable => "this is my variable"
        this_is_my_variable => "this is my variable"
    Args:
        s (_type_): _description_

    Returns:
        _type_: _description_
    """
    # use map to add an underscore before each uppercase letter
    modified_string = list(map(lambda x: '_' + x if x.isupper() else x, s))
    # join the modified string and split it at the underscores
    split_string = ''.join(modified_string).split('_')
    # remove any empty strings from the list
    split_string = list(filter(lambda x: x != '', split_string))
    return " ".join(split_string)


def transform_code_into_text(filename):
    # Get source code content
    f = open(filename)
    lines = ''.join(f.readlines())
    f.close()
    s = ""

    # See : https://pygments.org/docs/quickstart/
    #TODO: To be tested with C++ multi comment style, constants, etc.
    #TODO: remove comment mark
    lexer = get_lexer_for_filename(filename)
    tokens = lexer.get_tokens(lines)
    for token in tokens:
        if token[0] == Token.Literal.String.Doc:
            s = s + ' ' + token[1];
        elif token[0] == Token.Comment.Single:
            s = s + ' ' + token[1];
        elif token[0] == Token.Comment.Multiline:
            s = s + ' ' + token[1];
        elif token[0] == Token.Literal.String.Single:
            if token[1] not in ["'",':', ';']:
                s = s + ' ' + token[1];
        elif token[0] == Token.Name.Function:
            s = s + ' ' + split_function_name(token[1]);
        elif token[0] == Token.Name:
            s = s + ' ' + split_function_name(token[1]);     #Variable name
            
    print('---------------------------------------')            
    print(s)

    # Remove code vocabulary (keywords and punct.)
    # What we want to keep:
    # - variable names
    # - function names
    # - constant names
    # - content of comments
    # - Text literals might be of interest
    # What we want to delete:
    # - language keywords (e.g. for, function, if...)
    # - language punct. (e.g. {};...)
    #
    # Transformations:
    # thisIsMyVariable => "this is my variable"
    # this_is_my_variable => "this is my variable"
    # The same applies for function names


    # # Remove duplicate spaces and new lines
    s = " ".join(s.split())

    # #Expand acronyms
    s = replace_acronyms(s)

    print('---------------------------------------')            
    print(s)

    # #Auto correct
    spell = Speller()
    s = spell(s)

    print('---------------------------------------')            
    print(s)
    return s

def text_similarity_nltk(text1, text2):
    # Tokenize and lemmatize the texts
    tokens1 = word_tokenize(text1)
    tokens2 = word_tokenize(text2)
    lemmatizer = WordNetLemmatizer()
    tokens1 = [lemmatizer.lemmatize(token) for token in tokens1]
    tokens2 = [lemmatizer.lemmatize(token) for token in tokens2]

    # Remove stopwords
    stop_words = stopwords.words('english')
    tokens1 = [token for token in tokens1 if token not in stop_words]
    tokens2 = [token for token in tokens2 if token not in stop_words]

    # Create the TF-IDF vectors
    vectorizer = TfidfVectorizer()
    vector1 = vectorizer.fit_transform(tokens1)
    vector2 = vectorizer.transform(tokens2)

    # Calculate the cosine similarity
    similarity = cosine_similarity(vector1, vector2)

    return similarity

def text_similarity_scikit(text1, text2):
    # Convert the texts into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])

    # Calculate the cosine similarity between the vectors
    similarity = cosine_similarity(vectors)
    return similarity

def transform_code_into_text_nltk(filename):
    # Get source code content
    f = open(filename)
#    lines = ''.join(f.readlines())
    lines = f.read()
    f.close()
    lines_filtered = lines.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(lines_filtered)
    stop_words = set(stopwords.words('english'))
    textfile = filename + ".txt"
    f = open(textfile,'w')
    i = 0
    written_tokens = []
    for token in tokens:
        if token not in stop_words:
            if token not in written_tokens:
                written_tokens.append(token)
                if i == 0:
                    f.write(token)
                else:
                    f.write(" " + token)
                i += 1
    f.close()

print("Transform source code")
#s1 = transform_code_into_text('./samples/docparse.py')
#s2 = transform_code_into_text('./samples/gtest-printers.cc')
transform_code_into_text_nltk('./samples/docparse.py')
transform_code_into_text_nltk('./samples/gtest-printers.cc')

exit()

text = "Make it possible to customize the dict that cuntains the list of words that suggest we have a spam."
text = replace_acronyms(text)
spell = Speller()
text = spell(text)
print(text)

# dist_s1_text = text_similarity(s1, text)
# dist_s2_text = text_similarity(s2, text)
dist_s1_text = text_similarity_scikit(s1, text)
dist_s2_text = text_similarity_scikit(s2, text)
print('distance = ', dist_s1_text[0][1], " / ", dist_s2_text[0][1])


# autocorrect-2.6.1
# scispacy-0.5.2
# Pygments-2.15.1
# nltk-3.8.1
# scikit-learn 1.3.0
# fasttext-0.9.2
