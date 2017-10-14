import json
import sys
import os


def arguments_exists(args):
    return bool(args)


def arguments_are_valid(args):
    if len(args) == 2:
        return True
    elif args[1][-1] == os.sep:
        print("Nom d'archive invalide")
        sys.exit(1)
    else:
        print("Arguments invalides")
        sys.exit(1)


def standardize_argument_input(args):
    list_dest_path = args[1].split(os.sep)
    return {
        "src_path": os.path.normpath(args[0]) + os.sep,
        "dest_path": os.path.join(*list_dest_path[:-1]) + os.sep,
        "archive_name": list_dest_path[-1]
    }


def load_json(json_path):
    with open(json_path, "r") as f:
        return json.load(f)


def json_is_valid(json_dict):
    return "src_path" in json_dict and "dest_path" in json_dict


def standardize_json_input(json_dict):
    return standardize_argument_input([json_dict["src_path"], json_dict["dest_path"]])


def input_data_is_valid(input_data):
    return os.path.isdir(input_data["src_path"])


if __name__ == '__main__':
    arguments = sys.argv[1:]
    json_conf = load_json('./config.json')
    if arguments_exists(arguments) and arguments_are_valid(arguments):
        data = standardize_argument_input(arguments)
    elif json_is_valid(json_conf):
        data = standardize_json_input(json_conf)
    else:
        print("Aucune donnée valide trouvée")
        sys.exit(1)
    if not input_data_is_valid(data):
        print(data)
        print("Données invalides")
        sys.exit(1)
    input(data)
    os.makedirs(data["dest_path"], 600, True)
