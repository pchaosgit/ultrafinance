ultrafinance
============
Python project for real-time financial data collection, analyzing && backtesting trading strategies.

============
todolist:
从通达信文件中获取数据
增加保存到mangoDB

============
Changelog

version 0.1
2015-11-01 ultrafinance/dam/googleFinance.py 支持python 3
           修复split 'str' does not support the buffer interface


<!--
平时切换到dev分支开发
 update git to master
-->
git checkout master
git merge dev
<!-- delete brach -->
git branch -d dev
git push
git checkout -b dev
git push --set-upstream origin dev
