import os


def move_item_in_list(liste: list, obj, index):
    liste.remove(obj)
    liste.insert(index, obj)
    return liste


def del_root(path, root):
    path = os.path.normpath(path)
    root = os.path.normpath(root) + os.sep
    print(path, root)
    assert root in path
    assert root[-1] == os.sep
    rep = path[len(root):]
    # print(root + rep)
    # print(path)
    assert root + rep == path
    return rep


def rlistdir(path='.'):
    files_list = []
    for directory, sub_dir, files in os.walk(path):
        for file in files:
            files_list.append(os.path.join(directory, file))
    return files_list


def zip_file_list(source_files, destination_files, src_path, untared_root):
    for i in range(max(len(source_files), len(destination_files))):
        if i >= len(source_files):
            source_files.append(None)
            continue
        if i >= len(destination_files):
            destination_files.append(None)
            continue
        src_file = del_root(source_files[i], src_path)
        print(destination_files[i], untared_root)
        dest_file = del_root(destination_files[i], untared_root)
        if src_file != dest_file:
            if os.path.join(untared_root, src_file) in destination_files:
                destination_files = move_item_in_list(destination_files, os.path.join(untared_root, src_file), i)
            else:
                destination_files.insert(i, None)
    return source_files, destination_files


if __name__ == '__main__':
    # Lister les fichiers du dossiers source
    src_files = rlistdir('/home/louis/fake_data/data')
    # Lister les fichiers du dossiers destination
    dest_files = rlistdir('/home/louis/fake_data/data')
    # Mettre en relation les listes
    src_files, dest_files = zip_file_list(src_files, dest_files, '/home/louis/fake_data/data/', '/home/louis/fake_data/save_here/data')
    # Récupérer les fichiers modifiés
    # Les écraser
    # Récupérer les fichiers ajoutés
    # Les ajouter
    # achicompresser
