This is a simple script for automated testing of codeforces tasks. The only dependency is Python2.6. Currently supported languages are: C, C++, Haskell, Python.

Usage:
Name your solution [problemname].[extension]. Run the script:
> python testforces.py [problemname]

where problemname is problem number + problem letter and extension is one of following: .c, .cpp, .py, .hs. You should see compilator's output (warnings or errors) and for each tests whether it is ok. If any of the tests fails, you will see expected output vs. what your program has produced.

Example:
> bash$ python testforces.py 177A
>
> Running: g++ -Wall -O2 177a.cpp -o 7a.out  
> WARNING:  
> 177a.cpp:5: warning: ISO C++ forbids declaration of 'main' with no type  
> 
> Status: [OK]  
> 
> Running test 1  
> Status: [OK]  
> Running test 2  
> Status: [OK]
> 
> All tests OK  
> bash$

Known issues:
- not all languages are supported  
- if test input/output contains html tags, it will probably break  
- if there are multiple correct answers and your solution return other than given on the website, it will be treated as a wrong answer  
- if you have two solutions in different languages, one of them will be ignored (you should probably remove/rename unneceessary files)  
- doesn't check for memory and time limits (this means that if your program gets into infinite loop, the script will freeze)

