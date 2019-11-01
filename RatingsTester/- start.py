# -*- coding: utf-8 -*-
import os


def printme(content):
    try:
        print content
    except:
        print(content)


def getContents(path="./", ext="", fullpath=True):
    final_list = []
    files = os.listdir(path)
    for item in files:
        if item.endswith(ext):
            if fullpath:
                final_list.append(os.path.join(path, item))
            else:
                final_list.append(item)
    return final_list


def userInput(question, answers):
    answer = ''
    while not answer.upper() in answers:
        for item in question:
            print item
        answer = raw_input("Choose from %s: " % answers)
    print "\n"
    return answer.upper()


def sanitiseAndMerge(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    contents = []
    for line in lines:
        if not line.strip().startswith('<'):
            contents.append(line)
    return contents


def generatePy():
    paths = getContents(path=os.path.dirname(os.path.realpath(__file__)),
                        ext=".xml")
    for path in paths:
        try:
            pyfile = path.replace('.xml', '.py')
            myfile = open(pyfile, 'w')
            myfile.write(
                        "from vars import *\nprintme('Running: %s')\n"
                        % path[:-3]
            )
            for line in sanitiseAndMerge(path):
                if 'from java' in line:
                    break
                if "#localvar" not in line:
                    myfile.write(line)
            myfile.close()
            printme("Success: %s" % os.path.realpath(pyfile))
        except:
            printme("FAILED: %s" % os.path.realpath(pyfile))


# Offer option of re-creating python files
paths = getContents(path=os.path.dirname(os.path.realpath(__file__)),
                    ext=".pyc")
for path in paths:
    os.remove(path)

ans = userInput(["Do you want to re-generate the Python files from the XMLs?",
                "(Y) Yes", "(N) No"], ['Y', 'N'])
if ans == 'Y':
    generatePy()

temp = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp')
if os.path.exists(temp):
    os.remove(temp)
baseURL = {
    "C": "https://hood-config.ice-technology.com/calcservice/REST/calcs/",
    "L": "https://hood-live.ice-technology.com/calcservice/REST/calcs/",
    "U": "https://hood-uat.ice-technology.com/calcservice/REST/calcs/"}

policyNumber = raw_input(
                        "\nEnter the reference number for the policy you "
                        "want to rate on\nPress ENTER to use the locally "
                        "stored file - response.txt\n")
if policyNumber != '':
    ans = userInput(["Which environment is this in?", "(L) Live",
                    "(C) Config", "(U) UAT"], ['L', 'C','U'])
    import requests
    from xml.sax import saxutils as su
    url = baseURL[ans.upper()]+policyNumber
    r = requests.get(url)
    if r.status_code >= 200 and r.status_code < 400:
        content = su.unescape(r.content)
        myfile = open(temp, 'w')
        myfile.write(content)
        myfile.close()
    else:
        import sys
        sys.exit(1)

from vars import *

imports = getImports()
for item in imports:
    exec("from %s import *" % item)

counter = 1
totalNumberOfPREClaims = 0
TotalSumOfClaimsWithin5Years = 0
TheftClaimCNT = 0
TheftClaimsWithin5Years = 0
ImpactClaimCNT = 0
MDClaimCNT = 0

# Output the results
printme("\n%s - %s - %s" % (calc["calc.SchemeCode"],
        calc["calc.PackageCode"],
        calc['calc.PolicyTransactionType']))
printme("\nClaims:")
if transactionType == 'RENEWAL_INVITE':
    printme("Load to apply: %s" % loadToApply)
    printme("Total number of claims: %s" % totalNumberOfClaims)
    printme("Claims in 1st year: %s" % claimsFirstYear)
    printme("Claims in 2nd year: %s" % claimsSecondYear)
    printme("Claims in 3rd year: %s" % claimsThirdYear)
    printme("Claims in 4th year: %s" % claimsFourthYear)
    printme("Claims in 5th year: %s" % claimsFifthYear)
else:
    printme("Total number of PRE claims: %s" % totalNumberOfPREClaims)
    printme("Total sum of Claims (past 5yrs): %s"
            % TotalSumOfClaimsWithin5Years)
    printme("Claims for theft: %s" % TheftClaimCNT)
    printme("Claims for impact: %s" % ImpactClaimCNT)
    printme("Claims for malicious damage: %s" % MDClaimCNT)
    printme("\nSpecified items:")
    counter = 1
    for item in partsNamed("SpecifiedItems"):
        printme("%s. £%s" % (counter, item["InsuredObjectValue"]))
        counter += 1
printme("\n#####################\n")

# Display all the global values
from inspect import isfunction
skipVars = ["calcResponse", "calcData", "mydict", "params", "baseURL",
            "su", "ET", "isfunction", "content", "onlinePath",
            "path", "os", "partsNamedDict", "part", "child", "imports"]

ans = userInput(["Do you want to see a list of EVERY variable set by this Python script?",
                "(Y) Yes", "(N) No"], ['Y', 'N'])
if ans == 'Y':
    for name, value in globals().items():
        if name not in skipVars and not isfunction(value) and \
            not name.startswith("__"):
            print(name, value)

if os.path.exists(temp):
    os.remove(temp)
paths = getContents(path=os.path.dirname(os.path.realpath(__file__)),
                    ext=".pyc")
for path in paths:
    os.remove(path)
raw_input("\nPress ENTER to exit")
