To test this use case, make instals described in the main README.md, and run these commands on this repo root : 

```
mkdir tmp
git clone https://github.com/Python-World/python-mini-projects.git ./tmp/python-mini-projects/
git --git-dir=./tmp/python-mini-projects/.git --work-tree=./tmp/python-mini-projects/ checkout 933393ca578c004d61e8c36294a8e0e63b9a96cd
python main.py analyze --database case3.db --folder ./tmp/python-mini-projects/
python main.py lookup --textfile=./researches/test-codet5-relevance/case3/issue.txt --database=case3.db
rm -rf tmp
```