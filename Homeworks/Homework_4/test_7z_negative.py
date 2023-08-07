from sshcheckers import ssh_checkout_negative
import yaml

with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

FOLDER_TST = data["FOLDER_TST"]
BAD_7z = data["BAD_7z"]
FOLDER_folder1 = data["FOLDER_folder1"]


def test_step1(make_folders, make_bad_arx):
    # negative_test1
    assert ssh_checkout_negative(data["host"], data["user"], data["password"],
                                 "cd {}; 7z a badarx.7z -o{} -y".format(BAD_7z, FOLDER_folder1),
                                 "Is not archive"), "negative_test1 FAIL"


def test_step2(make_bad_arx):
    # negative_test2
    assert ssh_checkout_negative(data["host"], data["user"], data["password"], "cd {}; 7z t badarx.7z".format(BAD_7z),
                                 "Is not archive"), "negative_test2 FAIL"
