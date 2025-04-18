import re
name = input("Enter file:")
if len(name) < 1 : name = "test.txt"
fh = open(name)
newlist = list()
for line in fh :
    line = re.findall('[0-9]+', line)  #finds all numbers '.[0-9]*[0-9]' was before and it missed py4e.com and etx
    for number in line :
        newlist.append(int(number)) # creates newlist with int line values
print(sum(newlist))