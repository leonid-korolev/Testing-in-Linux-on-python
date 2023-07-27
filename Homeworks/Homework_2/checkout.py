import subprocess

FOLDER_TST = "/home/user/tst"
FOLDER_OUT = "/home/user/out"
FOLDER_BAD = "/home/user/folder_bad_7z"
FOLDER_folder1 = "/home/user/folder1"
FOLDER_folder2 = "/home/user/folder2"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0 or text in result.stderr:
        return True
    else:
        return False


def getout(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
