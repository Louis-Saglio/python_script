import os


src = [
    '/home/louis/file1',
    '/home/louis/file2',
    '/home/louis/file3',
    '/home/louis/file8',
    '/home/louis/file5',
    '/home/louis/file6',
    '/home/louis/file9',
]

dest = [
    '/home/dest/file1',
    '/home/dest/file2',
    '/home/dest/file3',
    '/home/dest/file6',
    '/home/dest/file4',
    '/home/dest/file5',
]


def del_root(path, root):
    # print(path, root)
    path = os.path.normpath(path)
    root = os.path.normpath(root) + os.sep
    assert root in path
    assert root[-1] == os.sep
    rep = path[len(root):]
    # print(root + rep)
    # print(path)
    assert root + rep == path
    return rep


def move_item_in_list(liste: list, obj, index):
    liste.remove(obj)
    liste.insert(index, obj)
    return liste


def zip_file_list(src_files, dest_files, src_path, untared_root):
    rep = {"src_files": src_files, "dest_files": dest_files}
    for i in range(max(len(src_files), len(dest_files))):
        src_file = del_root(src_files[i], src_path)
        dest_file = del_root(dest_files[i], untared_root)
        if src_file != dest_file:
            # si src_files[i] n'existe pas on le créé à None
            if i >= len(src_files):
                src_files.append(None)
                continue
            # si src_file in dest_files on déplace dest_file correspondant à l'index de src_file
            if os.path.join(untared_root, src_file) in dest_files:
                dest_files = move_item_in_list(dest_files, os.path.join(untared_root, src_file), i)
            # sinon on insère None dans dest_file à i
            else:
                dest_files.insert(i, None)
        print(src_files[i])
        print(dest_files[i])
        input()
    return rep["src_files"], rep["dest_files"]


if __name__ == '__main__':
    zip_file_list(src, dest, '/home/louis', '/home/dest')
