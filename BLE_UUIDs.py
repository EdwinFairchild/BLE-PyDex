import json


def get_uuid_dict(filename,user=False):
    """
    Extract service name and hex value from JSON file

    :param filename: str, the name of the JSON file

    :param user: bool, determines if the file passed is user defined

    :return: dict, a dictionary with hex value as the key and service name as the value

    """

    with open(filename,'r') as file:
        data = json.load(file)
        if user:
            user_dict = {}
            for key,value in data.items():
                if value[0] == True:
                    # The key is in big endian so convert to little endian
                    i = 0
                    new_key = ""
                    while i <= len(key)-2:
                        new_key = key[i:i+2] + new_key
                        i+= 2
                    user_dict[new_key.lower()] = value[1]
                else:
                    user_dict[key.lower()] = value[1]
            return user_dict
  
    return data