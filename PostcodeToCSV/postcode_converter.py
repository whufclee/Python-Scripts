import glob
import os
origFile = "./orig.xml"
newfile = "./postcodes_converted_1.csv"
writefile = open(newfile,"w+")
counter = 0
fullcount = 0
writefile.write("POSTCODE, B_AD, B_STD_AGGREGATE, C_AD, C_STD_AGGREGATE, PP, B_TA, C_TA, MSS, FLOOD, SUBS\n")
print "CONVERSION IN PROGRESS, PLEASE WAIT (THIS MAY TAKE A WHILE)..."
with open(origFile) as f:
    for line in f:
        if "POSTCODE" in line:
            a = line.split('>')[1].split('<')[0]
        if "B_AD" in line:
            b = line.split('>')[1].split('<')[0]
        if "B_STD_AGGREGATE" in line:
            c = line.split('>')[1].split('<')[0]
        if "C_AD" in line:
            d = line.split('>')[1].split('<')[0]
        if "C_STD_AGGREGATE" in line:
            e = line.split('>')[1].split('<')[0]
        if "PP" in line:
            f = line.split('>')[1].split('<')[0]
        if "B_TA" in line:
            g = line.split('>')[1].split('<')[0]
        if "C_TA" in line:
            h = line.split('>')[1].split('<')[0]
        if "MSS" in line:
            i = line.split('>')[1].split('<')[0]
        if "FLOOD" in line:
            j = line.split('>')[1].split('<')[0]
        if "SUBS" in line:
            k = line.split('>')[1].split('<')[0]
            writefile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (a, b, c, d, e, f, g, h, i, j, k))
            counter += 1
            fullcount += 1
            print "POSTCODES ADDED: %d" % fullcount
        if counter == 1048575:
            writefile.close()
            counter = 0
            currentVersion = int(newfile[-5])
            newfile = "%s%s.csv" % (newfile[:-5], str(currentVersion + 1))
            writefile = open(newfile, "w+")
            writefile.write("POSTCODE, B_AD, B_STD_AGGREGATE, C_AD, C_STD_AGGREGATE, PP, B_TA, C_TA, MSS, FLOOD, SUBS\n")
print "WOOHOO - FINALLY COMPLETE!\n"
print "You can find the converted file here:"

files = glob.glob("./postcodes_converted*")
for item in files:
    print os.path.abspath(item)
ans = raw_input("Press ENTER to quit")