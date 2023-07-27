from checkout import checkout, FOLDER_BAD, FOLDER_folder1


def test_step1():
    # negative_test1
    assert checkout("cd {}; 7z e bad.7z -o{} -y".format(FOLDER_BAD, FOLDER_folder1), "Is not archive"), \
                                                                                          "negative_test1 FAIL"


def test_step2():
    # negative_test2
    assert checkout("cd {}; 7z t bad.7z".format(FOLDER_BAD), "Is not archive"), "negative_test2 FAIL"
