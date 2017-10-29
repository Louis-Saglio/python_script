import filecmp
import os


def rlistdir(path='.'):
    for directory, sub_dir, files in os.walk(path):
        for file in files:
            yield os.path.join(directory, file)


if __name__ == '__main__':
    for i in rlistdir('/usr'):
        print(i)
