class BLE_UUID():

    file = open("UUIDs.txt",'r')
    data = file.readlines()
    uuid_dict = {}
    #this should probably only happen once when the class is instantiated 
    for line in data:
        line = line.split()
        if line[1] not in uuid_dict:
            uuid_dict[line[2]] = line[1]