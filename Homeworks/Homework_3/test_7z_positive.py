from checkout import checkout, getout
import yaml

with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
FOLDER_TST = data["FOLDER_TST"]
FOLDER_OUT = data["FOLDER_OUT"]
FOLDER_folder1 = data["FOLDER_folder1"]
FOLDER_folder2 = data["FOLDER_folder2"]
type = data["type"]

def test_step1(make_folders, clear_folders, make_files):
    # test1

    res1 = checkout("cd {}; 7z a {}/arx2 -t{}".format(FOLDER_TST, FOLDER_OUT, type), "Everything is Ok")
    res2 = checkout("ls {}".format(FOLDER_OUT), "arx2 -t{}".format(type)), "test1 FAIL"
    assert res1 and res2, "test1 FAIL"


def test_step2( make_folders, clear_folders, make_files):
    # test2
    res = []
    res.append(checkout("cd {}; 7z a {}/arx2 -t{}".format(FOLDER_TST, FOLDER_OUT, type), "Everything is Ok"))
    res.append(checkout("cd {}; 7z e arx2.{} -o{} -y".format(FOLDER_OUT, type, FOLDER_folder1), "Everything is Ok"))
    for item in make_files:
        res.append(checkout("ls {}".format(data["FOLDER_folder1"]), item))
    assert all(res)


def test_step3():
    # test3
    assert checkout("cd {}; 7z t arx2.{}".format(FOLDER_OUT, type), "Everything is Ok"), "test3 FAIL"


def test_step4():
    # test4
    assert checkout("cd {}; 7z u arx2.{}".format(FOLDER_OUT, type), "Everything is Ok"), "test4 FAIL"


def test_step5(make_folders, clear_folders, make_files):
    # test5
    res = []
    res.append(checkout("cd {}; 7z a {}/arx2 -t{}".format(FOLDER_TST, FOLDER_OUT, type), "Everything is Ok"))
    for i in make_files:
        res.append(checkout("cd {}; 7z l arx2.{}".format(FOLDER_OUT, type), i))
    assert all(res), "test5 FAIL"


def test_step6(clear_folders, make_files, make_subfolder):
    # test6
    res = []
    res.append(checkout("cd {}; 7z a {}/arx -t{}".format(FOLDER_TST, FOLDER_OUT, type), "Everything is Ok"))
    res.append(
        checkout("cd {}; 7z x arx.{} -o{} -y".format(FOLDER_OUT, type, FOLDER_folder2), "Everything is Ok"))
    for i in make_files:
        res.append(checkout("ls {}".format(FOLDER_folder2), i))
    res.append(checkout("ls {}".format(FOLDER_folder2), make_subfolder[0]))
    res.append(checkout("ls {}/{}".format(FOLDER_folder2, make_subfolder[0]), make_subfolder[1]))
    assert all(res), "test6 FAIL"


def test_step7():
    # test7

    assert checkout("cd {}; 7z d arx2.{}".format(FOLDER_OUT, type), "Everything is Ok"), "test7 FAIL"


def test_step8(clear_folders, make_files):
    # test8
    res = []
    for i in make_files:
        res.append(checkout("cd {}; 7z h {}".format(data["FOLDER_TST"], i), "Everything is Ok"))
        hash = getout("cd {}; crc32 {}".format(data["FOLDER_TST"], i)).upper()
        res.append(checkout("cd {}; 7z h {}".format(data["FOLDER_TST"], i), hash))
    assert all(res), "test8 FAIL"
