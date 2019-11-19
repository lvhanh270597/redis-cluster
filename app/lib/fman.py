import subprocess
import os

def create_path(fpath):
    if not os.path.exists(fpath):
        os.makedirs(fpath)
        print("Made avaliable path '%s' successfully!" % fpath)
    else:
        print("'%s' existed!" % fpath)

def create_file(fpath):
    subprocess.call(["touch", fpath])

def search_replace(fpath, rep, newfpath):
    text = open(fpath).read()
    for _from, _to in rep.items():
        text = text.replace(_from, _to)
    fdata = open(newfpath, "w")
    fdata.write(text)
    fdata.close()