##############################################
#              GLOBAL FUNCTIONS              #
##############################################
import os
import re
import datetime
import xml.etree.ElementTree as ET

# HARDCODED (Temp solution for training)
transactionType = "QUOTE"

base = os.path.dirname(os.path.realpath(__file__))
# Add any root items you want added to the calc in here
calcList = ["Policyholder","NamedParty","Building"]

def cleanupString(string):
    if ',' in string:
        if not string.startswith('[') and not string.startswith('{'):
            if string[-3] == '.':
                string = string.replace(',', '')
    try:
        string = int(string)
    except:
        pass
    return string

def info(header, contents):
    printme("%s: %s" % (header, contents))

def error(header, contents):
    printme("%s: %s" % (header, contents))

def lt(x, y):
    return x < y

def gt(x, y):
    return x > y

def ge(x, y):
    return x >= y

def le(x, y):
    return x <= y

def daysBetweenDates(date1, date2, maxDays=10000):
    def isLeapYear(year):
        return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0

    def countDays(year, month, day):
        daysOfMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        daysInMonth = 0
        if isLeapYear(year) and month == 2:
            daysInMonth = daysOfMonths[month - 1] + 1
        else:
            daysInMonth = daysOfMonths[month - 1]

        if lt(day, daysInMonth):
            return year, month, day + 1
        else:
            if month == 12:
                return year + 1, 1, 1
            else:
                return year, month + 1, 1

    def convertDate(mydate):
        monthsOfYear = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        d, m, y, t = mydate.split(' ')
        m = str(monthsOfYear.index(m.lower()) + 1)
        if (len(m) == 1):
            m = '0' + m
        return "/".join([y, m, d])

    date1 = date1.replace('-', '/')
    date2 = date2.replace('-', '/')
    if ('/' not in date1):
        date1 = convertDate(date1)
    if ('/' not in date2):
        date2 = convertDate(date2)
    date1 = date1[:10]
    date2 = date2[:10]
    y1, m1, d1 = map(int, date1.split('/'))
    y2, m2, d2 = map(int, date2.split('/'))

    if gt(int(date1.replace('/', '')), int(date2.replace('/', ''))):
        m1, m2 = m2, m1
        y1, y2 = y2, y1
        d1, d2 = d2, d1
    days = 0
    while (not (m1 == m2 and y1 == y2 and d1 == d2) and lt(days, maxDays)):
        y1, m1, d1 = countDays(y1, m1, d1)
        days += 1
    return int(days)


def partsNamed(part):
    try:
        return partsNamedDict[part]
    except:
        return []

def printme(content):
    try:
        print content
    except:
        print(content)

def age(dob):
    today = datetime.date.today()
    dob = datetime.datetime.strptime(dob, "%Y-%m-%d")
    years = today.year - dob.year
    if lt(today.month, dob.month) or (today.month == dob.month and lt(today.day, dob.day)):
        years -= 1
    printme(years)
    return int(years)

def userInput(question, answers):
    answer = ''
    while not answer.upper() in answers:
        for item in question:
            printme(item)
        answer = raw_input("Choose from %s: " % answers)
    printme("\n")
    return answer.upper()

def getImports():
    global base
    ignoreList = ["- start.py", "vars.py", "runme.py"]
    final_list = []
    files = os.listdir(base)
    for item in files:
        if item.endswith(".py") and not item in ignoreList:
            final_list.append(item[:-3])
    return final_list

#############################################################
# Setup Global variables and dictionaries from raw XML data #
#############################################################

# Sanitise the XML response data
dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(base, "response.txt")
onlinePath = os.path.join(base, "temp")
if os.path.exists(onlinePath):
    if os.path.getmtime(onlinePath) > os.path.getmtime(path):
        path = onlinePath
        printme("Results based on ONLINE data")
    else:
        printme("Results based on LOCAL file data (response.txt)")

with open(path) as f:
    content = f.read()
content = content.replace('\n', '').replace('\r', '').replace('\t', '').replace('&#xD;', '')\
    .replace(u'<?xml version="1.0" encoding="UTF-8"?>','')
regex = "(\<\?xml)(.*?)(\>)"
replacements = re.findall(regex, content)
for item in replacements:
    content = content.replace(''.join(map(str, item)),'')
if u"<calcResponse/>" in content:
    regex = u"<calcData>(.*?)<calcResponse/>"
else:
    regex = u"<calcData>(.*?)</calcResponse>"

rawXml = re.findall(regex,content)
try:
    calcData, calcResponse = rawXml[0].split(u'<calcResponse>')
except:
    calcData = rawXml[0]
    calcResponse = u"<calcResponse/>"
calcData = calcData.replace(u"</calcData></calcData>",u"</calcData>").encode('utf-8')
root = ET.fromstring(calcData)
calc = {}
partsNamedDict = {}

def populate_calc(root, path=None):
    if path is None:
        path = ["calc"]

    for child in root:
        if child.text != None:
            text = child.text.strip()
            try:
                exec (child.tag + ' = int(' + child.text + ')')
            except:
                try:
                    exec (child.tag + ' = ' + child.text)
                except:
                    exec (child.tag + " = '%s'" % child.text)
        else:
            text = ''
        new_path = path[:]
        if child.tag == "part":
            new_path.append(child.attrib["partname"])
        else:
            new_path.append(child.tag)
        if text != '':
            calc['.'.join(new_path)] = cleanupString(text)
        populate_calc(child, new_path)

populate_calc(root)
for part in root.findall('part'):
    partsNamedDict[part.attrib["partname"]] = []
# Parse the data from calcData to relevant dictionaries
# Build the partsNamed dictionary
for part in root.findall('part'):
    mydict = {}
    for child in part:
        if child.text != None:
            try:
                exec (child.tag + ' = ' + child.text)
            except:
                exec (child.tag + " = '%s'" % child.text)
            mydict[child.tag] = child.text
            if part.attrib["partname"] in calcList:
                calc["calc.%s.%s" % (part.attrib["partname"],child.tag)] = child.text
            if part.attrib["partname"] == "Claim" and child.tag == "IncidentDate":
                y,m,d = child.text.split('-')
                d = d.split('T')[0]
                x = datetime.datetime(int(y), int(m), int(d))
                formattedIncDate = x.strftime("%d %b %Y 12:00:00")
                mydict["formattedIncDate"] = formattedIncDate
    partsNamedDict[part.attrib["partname"]].append(mydict)

# Parse the data from calcResponse and set as global variables
root = ET.fromstring(calcResponse)
for part in root.findall('calcElement'):
    for section in part:
        if "partname" in section.attrib:
            if section.attrib["partname"] in calcList:
                for child in section:
                    if child.tag != "calcElement":
                        if child.text == None:
                            printme("WARNING: Failed to set %s to %s" % (child2.tag, cleanText))
                        else:
                            calc["calc.%s.%s" % (section.attrib["partname"], child.tag)] = child.text
                            cleanText = cleanupString(child.text)
                            try:
                                exec(child.tag + ' = ' + cleanText)
                            except (NameError,SyntaxError):
                                exec (child.tag + " = '%s'" % cleanText)
                            except Exception as e:
                                printme("WARNING: Failed to set %s to %s" % (child.tag, cleanText))
                            printme("Set %s to %s (%s)" % (child.tag, cleanText, type(eval(child.tag))))
                    else:
                        for child2 in child:
                            if child2 != "calcElement":
                                if child2.text == None:
                                    printme("WARNING: Failed to set %s to %s" % (child2.tag, cleanText))
                                else:
                                    calc["calc.%s.%s" % (section.attrib["partname"], child2.tag)] = child2.text
                                    cleanText = cleanupString(child2.text)
                                    try:
                                        exec(child2.tag + ' = ' + cleanText)
                                    except (NameError, SyntaxError):
                                        exec (child2.tag + " = '%s'" % cleanText)
                                    except Exception as e:
                                        printme("WARNING: Failed to set %s to %s" % (child2.tag, cleanText))
                                    printme("Set %s to %s (%s)" % (child2.tag,cleanText,type(eval(child2.tag))))
        else:
            cleanText = cleanupString(section.text)
            try:
                exec (section.tag + ' = ' + cleanText)
            except (NameError, SyntaxError):
                exec (section.tag + " = '%s'" % cleanText)
            except Exception as e:
                printme("WARNING: Failed to set %s to %s" % (section.tag, cleanText))

            if section.text != None:
                calc["calc.%s" % section.tag] = cleanText
            printme("Set %s to %s (%s)" % (section.tag, cleanText, type(eval(section.tag))))
printme("\nMESSAGES: ")