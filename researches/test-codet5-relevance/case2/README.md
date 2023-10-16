To test this use case, make instals described in the main README.md, and run these commands on this repo root : 

```
mkdir tmp
git clone https://github.com/kidk/felt.git ./tmp/felt/
git --git-dir=./tmp/felt/.git --work-tree=./tmp/felt/ checkout 428b71cc20e07664b7dac0720857cc2ab2f25006
python main.py analyze --database case2.db --folder ./tmp/felt/
python main.py lookup --textfile=./researches/test-codet5-relevance/case2/issue.txt --database=case2.db
rm -rf tmp
```