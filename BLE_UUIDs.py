
file = open("UUIDs.txt",'r')
data = file.readlines()
info_dict = {}
for line in data:
    line = line.split()
    if line[1] not in info_dict:
        info_dict[line[2]] = line[1]