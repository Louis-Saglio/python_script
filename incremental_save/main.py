import json
import sys
import os


# CONFIG_FILE = os.path.normpath(os.path.expanduser("~/.pysync"))
CONFIG_FILE = os.path.normpath(os.path.expanduser("~/Cours/Scripting/python_script/incremental_save/config.json"))


def raise_error(message, return_code=1):
    print(message)
    sys.exit(return_code)


def arguments_exists(args):
    return bool(args)


def arguments_are_valid(args):
    return len(args) == 2


def standardize_argument_input(args):
    dest_path, archive_name = os.path.split(args[1])
    return {
        "src_path": os.path.abspath(args[0]) + os.sep,
        "dest_path": os.path.abspath(dest_path + os.sep),
        "archive_name": archive_name
    }


def load_json(json_path):
    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise_error(f"Aucun fichier {json_path} trouvé")
    except json.JSONDecodeError:
        raise_error("Json invalide")


def json_is_valid(json_dict):
    return "src_path" in json_dict and "dest_path" in json_dict


def standardize_json_input(json_dict):
    return standardize_argument_input([json_dict["src_path"], json_dict["dest_path"]])


def input_data_is_valid(input_data):
    return os.path.isdir(input_data["src_path"]) and input_data["archive_name"]


if __name__ == '__main__':

    arguments = sys.argv[1:]

    if arguments:
        if not arguments_are_valid(arguments):
            raise_error("Arguments invalides")
        data = standardize_argument_input(arguments)
    else:
        json_conf = load_json(CONFIG_FILE)
        if not json_is_valid(json_conf):
            raise_error("Json invalide")
        data = standardize_json_input(json_conf)

    if not input_data_is_valid(data):
        raise_error(f"Données invalides\t:\t{data}")
    os.makedirs(data["dest_path"], 0o600, True)
    if not os.path.isdir(data["src_path"]):
        raise_error(f"La source {data['src_path']} n'existe pas ou n'est pas un dossier")
    print("Synchronisation effectuée avec succès !", data)
