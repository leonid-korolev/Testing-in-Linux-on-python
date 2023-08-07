import pytest
from checkout import checkout, getout
from sshcheckers import ssh_checkout, ssh_getout
import random, string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout(data["host"], data["user"], data["password"],
                        "mkdir {} {} {} {}".format(data["FOLDER_TST"], data["FOLDER_OUT"], data["FOLDER_folder1"],
                                                   data["FOLDER_folder2"]), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(data["host"], data["user"], data["password"],
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["FOLDER_TST"], data["FOLDER_OUT"],
                                                            data["FOLDER_folder1"], data["FOLDER_folder2"]), "")


@pytest.fixture()
def make_files():
    list_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["FOLDER_TST"],
                                                                                        filename, data["size"]),""):
            list_files.append(filename)
    return list_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; mkdir {}".format(data["FOLDER_TST"], subfoldername), ""):
        return None, None
    if not ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["FOLDER_TST"],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx(make_folders, clear_folders, make_files):
    ssh_checkout(data["host"], data["user"], data["password"],
                 "cd {}; 7z a {}/badarx.7z".format(data["FOLDER_TST"], data["BAD_7z"]), "Everything is Ok")
    yield ssh_checkout(data["host"], data["user"], data["password"],
                       "truncate -s 1 {}/badarx.7z".format(data["BAD_7z"]), ""), "test1 FAIL"


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout("cat /proc/loadavg")
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"), \
                                                                            data["count"], data["size"], stat), "")


@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
