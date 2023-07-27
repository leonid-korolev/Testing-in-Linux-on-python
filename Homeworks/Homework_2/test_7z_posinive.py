from checkout import checkout, getout, FOLDER_TST, FOLDER_OUT, FOLDER_folder1, FOLDER_folder2





def test_step1():
    # test1
    res1 = checkout("cd {}; 7z a ../out/arx2".format(FOLDER_TST), "Everything is Ok"), "test1 FAIL"
    res2 = checkout("ls {}".format(FOLDER_OUT), "arx2.7z"), "test1 FAIL"
    assert res1 and res2, "test1 FAIL"


# def test_step2():
#     # test2
#     res1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(FOLDER_OUT, FOLDER_folder1), "Everything is Ok")
#     res2 = checkout(f"ls {FOLDER_folder1}", "text")
#     assert res1 and res2, "test2 FAIL"


# def test_step3():
#     # test3
#     assert checkout("cd {}; 7z t arx2.7z".format(FOLDER_OUT), "Everything is Ok"), "test3 FAIL"


# def test_step4():
#     # test4
#     assert checkout("cd {}; 7z u arx2.7z".format(FOLDER_OUT), "Everything is Ok"), "test4 FAIL"


def test_step5():
    # test5
    res1 = checkout("cd {}; 7z l arx2.7z".format(FOLDER_OUT), "folder_tst")
    res2 = checkout("cd {}; 7z l arx2.7z".format(FOLDER_OUT), "folder_tst/text")
    res3 = checkout("cd {}; 7z l arx2.7z".format(FOLDER_OUT), "folder_tst/text_1")
    res4 = checkout("cd {}; 7z l arx2.7z".format(FOLDER_OUT), "test.sh")
    assert res1 and res2 and res3 and res4, "test5 FAIL"


def test_step6():
    # test6
    res1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(FOLDER_OUT, FOLDER_folder2), "Everything is Ok")
    res2 = checkout("ls {}".format(FOLDER_folder2), "folder_tst")
    res3 = checkout("ls {}/*".format(FOLDER_folder2), "text")
    res4 = checkout("ls {}/*".format(FOLDER_folder2), "text_1")
    res5 = checkout("ls {}".format(FOLDER_folder2), "test.sh")
    assert res1 and res2 and res3 and res4 and res5, "test6 FAIL"


# def test_step7():
#     # test7
#
#     assert checkout("cd {}; 7z d arx2.7z".format(FOLDER_OUT), "Everything is Ok"), "test7 FAIL"


def test_step8():
    # test8
    res1 = checkout("cd {}; 7z h folder_tst".format(FOLDER_TST), "Everything is Ok")
    hash = getout("cd {}; crc32 folder_tst".format(FOLDER_TST)).upper()
    res2 = checkout("cd {}; 7z h folder_tst".format(FOLDER_TST), hash)
    assert res1 and res2, "test8 FAIL"


