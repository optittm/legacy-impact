mkdir tmp

echo "=================================================="
echo "CASE 1 :" 
echo "=================================================="
echo "Analyzing..."
python main.py analyze --database case1.db --folder ./researches/test-codet5-relevance/case1/src > /dev/null
python main.py lookup --textfile=./researches/test-codet5-relevance/case1/issue.txt --database=case1.db

echo "=================================================="
echo "CASE 2 :" 
echo "=================================================="
git clone https://github.com/kidk/felt.git ./tmp/felt/ > /dev/null
git --git-dir=./tmp/felt/.git --work-tree=./tmp/felt/ checkout 428b71cc20e07664b7dac0720857cc2ab2f25006 > /dev/null
echo "Analyzing..."
python main.py analyze --database case2.db --folder ./tmp/felt/ > /dev/null
python main.py lookup --textfile=./researches/test-codet5-relevance/case2/issue.txt --database=case2.db

echo "=================================================="
echo "CASE 3 :" 
echo "=================================================="
git clone https://github.com/Python-World/python-mini-projects.git ./tmp/python-mini-projects/ > /dev/null
git --git-dir=./tmp/python-mini-projects/.git --work-tree=./tmp/python-mini-projects/ checkout 933393ca578c004d61e8c36294a8e0e63b9a96cd > /dev/null
echo "Analyzing..."
python main.py analyze --database case3.db --folder ./tmp/python-mini-projects/ > /dev/null
python main.py lookup --textfile=./researches/test-codet5-relevance/case3/issue.txt --database=case3.db

echo "=================================================="
echo "CASE 4 :" 
echo "=================================================="
git clone https://github.com/TheAlgorithms/Java.git ./tmp/Java/ > /dev/null
git --git-dir=./tmp/Java/.git --work-tree=./tmp/Java/ checkout 9795bada907a533182496a56ccf8644cc7c274a4 > /dev/null
echo "Analyzing..."
python main.py analyze --database case4.db --folder ./tmp/Java/ > /dev/null
python main.py lookup --textfile=./researches/test-codet5-relevance/case4/issue.txt --database=case4.db

# clean
rm -rf tmp