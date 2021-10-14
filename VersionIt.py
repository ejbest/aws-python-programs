import re

f = open("/vol1/bastion/index.html", "r+")
lines = f.readlines()
f.seek(0)

for line in lines:
    if re.match('^<pre>', line):
        print("******************************")
        print("** Found a match *************")
        print("******************************")

        number = re.findall("[0-9.]+", line)[0]
        number_parts = number.split('.')

        number_parts = [ int(x) for x in number_parts]

        length = len(number_parts)

        number_parts[length-1] += 1

        index = length - 1
        while(number_parts[index] > 9 and index > 0):
            number_parts[index] = 0
            number_parts[index-1] += 1
            index -= 1

        number_parts = [ str(x) for x in number_parts]

        number = '.'.join(number_parts)
        line = re.sub("[0-9.]+", number, line)

    #print(line)
    f.write(line)

f.truncate()
f.close()
