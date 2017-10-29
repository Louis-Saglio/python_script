__author__ = "Louis Saglio"
__date__ = "29/10/2017"

import sys
import os
import json
import tarfile
import time
import shutil
import signal
import paramiko


def raise_error(message, return_code=1):
    sys.stdout.buffer.write(bytes(message + '\n', encoding="utf-8"))
    sys.exit(return_code)


if sys.version_info.major < 3 or sys.version_info.minor < 6:
    raise_error("Vous devez utiliser Python 3.6 au plus pour pouvoir lancer ce script", 1)


CONFIG_FILE = os.path.normpath(os.path.expanduser("config.json"))


def get_help():
    return """    Python 3.6 est nécessaire pour lancer ce script !
    Usage :
    pyrsync src dest [ip_ssh login_ssh password_ssh dir_where_to_save_on_ssh]
    pyrsync (without arguments) : will use ./config.json to choose arguments (for ssh, must provide cli arguments)
    If you want to provide an other path for config.json, fill the CONFIG_FILE global variable at line 14 in pyrsync file
    If no config.json file is found, it will be created
    Exemples:
    pyrsync /home/user/folder /home/user/save_here/archive.tar.gz
    pyrsync
    pyrsync /home/user/folder /home/user/save_here/archive.tar.gz 192.168.10.10 admin Passw0rd
    """


def get_or_create_conf_file(path):
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            json.dump({
                "last_save_date": 0,
                "src_path": os.path.expanduser("~"),
                "dest_path": os.path.join(os.path.expanduser("~"), "save.tar.gz"),
                "last_save_timestamp": 0
            }, f)


def handle_ssh_args(args):
    if len(args) <= 2:
        return None, args, None
    try:
        server, login, password, remote_dest = args[2], args[3], args[4], args[5]
        ssh = paramiko.SSHClient()
        ssh.connect(server, username=login, password=password)
        return ssh.open_sftp(), args[:2], remote_dest
    except IndexError:
        raise_error("Arguments ssh invalides")
    except:
        raise_error("Imossible de se connecter au serveur SSH.")


def arguments_are_valid(args):
    return len(args) == 2


def standardize_argument_input(args):
    dest_path, archive_name = os.path.split(args[1])
    return {
        "src_path": os.path.abspath(args[0]) + os.sep,
        "dest_path": os.path.abspath(dest_path) + os.sep,
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


def get_last_save_timestamp(json_data):
    try:
        timestamp = json_data["last_save_timestamp"]
        return timestamp
    except:
        raise_error("Impossible de trouver la date de la dernière sauvegarde")


def rlistdir(path='.'):
    files_list = []
    for directory, sub_dir, files in os.walk(path):
        for file in files:
            files_list.append(os.path.join(directory, file))
    return files_list


def sync_json_conf_file(json_path, new_data):
    new_data["last_save_timestamp"] = time.time()
    with open(json_path, 'w') as f:
        json.dump(new_data, f, indent=4)


def safe_extract_targz(dest_path, archive_name, src_path):
    """
    Extrait l'archive <archive_name> du dossier <dest_path> et renvoi le path du dossier ainsi poduit.
    Si l'archive n'existe pas, renvoi fait comme si l'archive ne contenait qu'un dossier vide
    """
    basename = src_path.split(os.sep)[-2]
    if os.path.isfile(dest_path + archive_name):
        try:
            with tarfile.open(dest_path + archive_name, "r:gz") as archive:
                archive.extractall(dest_path)
                basename = os.path.commonpath(archive.getnames())
        except tarfile.ReadError:
            pass
        os.remove(os.path.join(dest_path, archive_name))
    else:
        os.makedirs(os.path.join(dest_path, basename), 0o700, True)
    return os.path.join(dest_path, basename)


def get_dest_path_by_src_path(src_file_path, src_path, dest_path):
    return os.path.join(dest_path, src_file_path[len(src_path):])


def create_targz(dest_path, archive_name):
    archive = tarfile.open(os.path.join(dest_path, archive_name), 'w:gz')
    for file in rlistdir(dest_path):
        if file != os.path.join(dest_path, archive_name):
            print(file)
            archive.add(file, arcname=get_dest_path_by_src_path(file, dest_path, ''))


def main():
    if '--help' in sys.argv:
        raise_error(get_help(), 1)

    get_or_create_conf_file(CONFIG_FILE)

    arguments = sys.argv[1:]
    json_conf = load_json(CONFIG_FILE)

    ssh, arguments, remote_dest = handle_ssh_args(arguments)

    if arguments:
        if not arguments_are_valid(arguments):
            raise_error("Arguments invalides")
        data = standardize_argument_input(arguments)
    else:
        if not json_is_valid(json_conf):
            raise_error("Json invalide")
        data = standardize_json_input(json_conf)

    if not input_data_is_valid(data):
        raise_error(f"Données invalides\t:\t{data}")

    last_save_timestamp = get_last_save_timestamp(json_conf)
    src_files = rlistdir(data["src_path"])

    modified_files = []
    for src_file in src_files:
        if os.path.getmtime(src_file) > last_save_timestamp:
            modified_files.append(src_file)

    dest_dir = safe_extract_targz(**data) + os.sep

    for modified_file in modified_files:
        created_file = get_dest_path_by_src_path(modified_file, data["src_path"], dest_dir)
        if not os.path.isdir(os.path.split(created_file)[0]):
            os.makedirs(os.path.split(created_file)[0])
        shutil.copyfile(modified_file, created_file)

    create_targz(data["dest_path"], data["archive_name"])

    if ssh:
        ssh.put(os.path.join(data["dest_path"], data["archive_name"]), remote_dest)

    shutil.rmtree(dest_dir, True)

    sync_json_conf_file(CONFIG_FILE, json_conf)


def signal_handler(sig, frame):
    data = load_json(CONFIG_FILE)
    folder = os.path.join(os.sep.join(data["dest_path"].split(os.sep)[:-1]), data["src_path"].split(os.sep)[-2])
    if os.path.isdir(folder):
        shutil.rmtree(os.path.join(folder))
    raise_error(f"Processus interompu. Une archive probablement incomplète ou corrompue a potentiellement été crée "
                f"à l'emplacement suivant : {data['dest_path']}.")


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    debut = time.time()
    try:
        main()
    except PermissionError:
        raise_error("Vous n'avez pas les droits suffisants.")
    except Exception as e:
        print(e)
        raise_error("Une erreur inconnue s'est produite")
    else:
        raise_error(f"L'opération a été effectuée sans problème en {round(time.time() - debut, 3)} seconde(s)", 0)
