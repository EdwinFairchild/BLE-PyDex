
def get_uuid_dict(filename):
    """
    Extract service name and hex value from uuid file which then gets added to a dictionary

    :param filename: str, the name of the uuid file

    :return: dict, a dictionary with hex value as the key and service name as the value

    """
    file = open(filename, 'r')
    data = file.readlines()
    uuid_dict = {}
    # this should probably only happen once when the class is instantiated
    for line in data:
        if line != "\n":
            line = line.split()
            if line[1] not in uuid_dict:
                uuid_dict[line[0][2:]] = line[1]
                # for debugging
                # print(f"{line[1][2:]}{line[0]}")

    return uuid_dict
