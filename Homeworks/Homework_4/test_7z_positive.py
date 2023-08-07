import yaml
from deploy import upload_files
from  sshcheckers import ssh_checkout, ssh_getout
from checkout import checkout, getout

with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
FOLDER_TST = data["FOLDER_TST"]
FOLDER_OUT = data["FOLDER_OUT"]
FOLDER_folder1 = data["FOLDER_folder1"]
FOLDER_folder2 = data["FOLDER_folder2"]
TYPE = data["type"]


def safe_log(start_time, name):
    with open(name, "w", encoding="utf-8") as f:
        f.write(''.join(getout(f"journalctl --since '{start_time}'")))

def test_step1(start_time):
    res = []
    upload_files(data["host"], data["user"], data["password"], data["local_path"], data["remote_path"])
    res.append(ssh_checkout(data["host"], data["user"], data["password"], f"echo {data['password']}| \
                                    sudo -S dpkg -i {data['remote_path']}", "Настраивается пакет"))

    res.append(ssh_checkout(data["host"], data["user"], data["password"], f"echo {data['password']} | \
                                sudo -S dpkg -s {data['pkgname']}", "Status: install ok installed"))
    safe_log(start_time,"log_test1")
    assert all(res), "test1 FAIL"


def test_step2(make_folders, clear_folders, make_files, start_time):
    # test2

    res1 = ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z a {}/arx2 ".
                        format(FOLDER_TST, FOLDER_OUT), "Everything is Ok")
    res2 = ssh_checkout(data["host"], data["user"], data["password"], "ls {}".format(FOLDER_OUT),
                         "arx2.7z")
    safe_log(start_time, "log_test2")
    assert res1 and res2, "test2 FAIL"


def test_step3( make_folders, clear_folders, make_files, start_time):
    # test3
    res = []
    res.append(ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z a {}/arx2 -t{}".
                            format(FOLDER_TST, FOLDER_OUT, TYPE), "Everything is Ok"))
    res.append(ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z e arx2.{} -o{} -y".
                            format(FOLDER_OUT, TYPE, FOLDER_folder1), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(data["host"], data["user"], data["password"], "ls {}".
                                format(data["FOLDER_folder1"]), item))
    safe_log(start_time, "log_test3")
    assert all(res)


def test_step4(start_time):
    # test4
    safe_log(start_time, "log_test4")
    assert ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z t arx2.{}".
                        format(FOLDER_OUT, TYPE), "Everything is Ok"), "test4 FAIL"


def test_step5(start_time):
    # test5
    safe_log(start_time, "log_test5")
    assert ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z u arx2.{}".
                        format(FOLDER_OUT, TYPE), "Everything is Ok"), "test5 FAIL"


def test_step6(make_folders, clear_folders, make_files, start_time):
    # test6
    res = []
    res.append(ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z a {}/arx2 -t{}".
                            format(FOLDER_TST, FOLDER_OUT, TYPE), "Everything is Ok"))
    for i in make_files:
        res.append(ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z l arx2.{}".
                                format(FOLDER_OUT, TYPE), i))
    safe_log(start_time, "log_test6")
    assert all(res), "test6 FAIL"


def test_step7(clear_folders, make_files, make_subfolder, start_time):
    # test7
    res = []
    res.append(ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z a {}/arx".
                            format(FOLDER_TST, FOLDER_OUT), "Everything is Ok"))
    res.append(ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z x arx.{} -o{} -y".
                            format(FOLDER_OUT, TYPE, FOLDER_folder2), "Everything is Ok"))
    for i in make_files:
        res.append(ssh_checkout(data["host"], data["user"], data["password"], "ls {}".format(FOLDER_folder2), i))
        res.append(ssh_checkout(data["host"], data["user"], data["password"], "ls {}".format(FOLDER_folder2),
                                make_subfolder[0]))
        res.append(ssh_checkout(data["host"], data["user"], data["password"], "ls {}/{}".format(FOLDER_folder2,
                                                                            make_subfolder[0]), make_subfolder[1]))
    safe_log(start_time, "log_test7")
    assert all(res), "test7 FAIL"


def test_step8(start_time):
    # test8
    safe_log(start_time, "log_test8")
    assert ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z d arx2.{}".format(FOLDER_OUT,
                                                                        TYPE), "Everything is Ok"), "test8 FAIL"


def test_step9(clear_folders, make_files, start_time):
    # test9
    res = []
    for i in make_files:
        res.append(ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z h {}".
                                format(data["FOLDER_TST"], i), "Everything is Ok"))
        hash = ssh_getout(data["host"], data["user"], data["password"], "cd {}; crc32 {}".
                                format(data["FOLDER_TST"], i)).upper()
        res.append(ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z h {}".
                                format(data["FOLDER_TST"], i), hash))
    safe_log(start_time, "log_test9")
    assert all(res), "test9 FAIL"
