import json
import random
import os


class FunFactJson():

    # Method is the method top open the file

    def get_json():
        directory = os.path.dirname(__file__)
        path_to_file = os.path.join(directory, "data", "funfact.json")
        return path_to_file

    # language should only take one param: "en" or "fr" and nothing else to defined the language of the funfact

    def get_random_fact(langage):
        path_to_file = FunFactJson.get_json()
        with open(path_to_file) as j:
            data = json.load(j)
        funfact_list = data['funFactList']
        rand = random.randint(0, len(funfact_list)-1)
        return funfact_list[rand][langage]

    # Method set_fact should take as param a dict
    def set_fact(funfact_dict):
        path_to_file = FunFactJson.get_json()
        with open(path_to_file, "r") as j:
            data = json.load(j)
        data['funFactList'].append(funfact_dict)
        with open(path_to_file, "w") as j:
            json.dump(data, j)
