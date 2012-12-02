import sys
import os
import re
import string 
import urllib
from subprocess import Popen, PIPE
from HTMLParser import HTMLParser
from collections import defaultdict

class TaskHTMLParser(HTMLParser):
  def __init__(self):
    self.inBox = False
    self.collecting = False
    self.input = []
    self.output = []
    self.tmp = []
    # HTMLParser is an old style class. 
    # writing this down in case it changes in future python version and breaks my script
    HTMLParser.__init__(self)

  def handle_starttag(self, tag, attrs):
    attrs = defaultdict(str, attrs)
    if attrs['class'] == 'input':
      self.inBox = True
      self.destination = self.input
    elif attrs['class'] == 'output':
      self.inBox = True
      self.destination = self.output
    if tag == 'pre' and self.inBox:
      self.collecting = True

  def handle_endtag(self, tag):
    if tag == 'pre':
      self.destination.append('\n'.join(self.tmp))
      self.tmp = []
      self.collecting = False
      self.inBox = False

  def handle_data(self, data):
    if self.collecting:
      self.tmp.append(data)

def extractName(taskName):
  pattern = re.compile('([0-9]*)([a-zA-Z])')
  if pattern.search(taskName):
    return pattern.search(taskName).groups()
  else:
    print "Cannot parse problem name"
    raise ValueError

def runCommand(cmd, inputData=None, verbose=False, stderr=True):
  if verbose:
    print "Running:", ' '.join(cmd)
  p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

  out, err = p.communicate(inputData)

  if p.returncode == 0:
    if err and stderr:
      print "WARNING:\n", err
    print "Status: [OK]"
    return out
  else:
    print "Status: [FAIL]"
    print "Exit code:", p.returncode
    print "Out:", out
    print "Errors:", err
    exit(1)

def findAndCompile(number, letter, sourceDirectory='.'):
  allFiles = os.listdir(sourceDirectory)
  fullName = number + letter
  for f in allFiles:
    if f == (fullName + '.cpp'):
      runCommand(['g++', '-Wall', '-O2', fullName + '.cpp', '-o', fullName + '.out'], verbose=True)
      return ['./{0}.out'.format(fullName)]
    elif f == (fullName + '.c'):
      runCommand(['gcc', '-O2', fullName + '.c', '-o', fullName + '.out'], verbose=True)
      return ['./{0}.out'.format(fullName)]
    elif f == (fullName + '.py'):
      return ['python', (fullName + '.py')]
    elif f == (fullName + '.hs'):
      runCommand(['ghc', '--make', fullName + '.hs', '-o', fullName + '.out'], verbose=True)
      return ['./{0}.out'.format(fullName)]

def checkTask(taskName):
  problemNumber, problemLetter = extractName(taskName)
  solutionBinary = findAndCompile(problemNumber, problemLetter)
  runAllTests(solutionBinary, problemNumber, problemLetter)
  
def downloadTests(number, letter):
  # todo: potential different URL for contests outside training?
  u = urllib.urlopen('http://codeforces.com/problemset/problem/{0}/{1}'.format(number, letter))
  site = ''.join([line for line in u])
  p = TaskHTMLParser()
  p.feed(site)
  inp = p.input
  outp = p.output
  return zip(inp, outp)

def runTest(binary, t):
  (case, expected) = t
  inp, expected = t
  output = runCommand(binary, inputData=inp)
  output = output.strip()
  expected = expected.strip()
  if output != expected:
    print "WRONG ANSWER!\nInput:\n{0}\nExpected:\n{1}\nGot:\n{2}\n".format(case, expected, output)
    exit(0)

def runAllTests(binary, number, letter):
  tests = downloadTests(number, letter)  
  for i, t in enumerate(tests):
    print "Running test", i+1
    runTest(binary, t)
  print 
  print "All tests OK"

def showHelp():
  print 'usage: python testforces.py 123a'
  print 'supported languages: python, c, c++, haskell'
  pass

def main():
  if len(sys.argv) < 2:
    showHelp()
  else:
    checkTask(sys.argv[1])

if __name__ == '__main__':
  main()
