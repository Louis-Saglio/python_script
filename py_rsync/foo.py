import tarfile
with tarfile.open('archive.tar.gz', 'w:gz') as f:
    f.add('config.json')