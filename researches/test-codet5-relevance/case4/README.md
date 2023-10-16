To test this use case, make instals described in the main README.md, and run these commands on this repo root : 

```
mkdir tmp
git clone https://github.com/TheAlgorithms/Java.git ./tmp/Java/
git --git-dir=./tmp/Java/.git --work-tree=./tmp/Java/ checkout 9795bada907a533182496a56ccf8644cc7c274a4
python main.py analyze --database case4.db --folder ./tmp/Java/
python main.py lookup --textfile=./researches/test-codet5-relevance/case4/issue.txt --database=case4.db
rm -rf tmp
```