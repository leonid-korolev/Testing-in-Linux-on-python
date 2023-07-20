'''
Задание 2. (повышенной сложности)

Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
в котором вывод разбивается на слова с удалением всех знаков пунктуации (их можно взять из
списка string.punctuation модуля string). В этом режиме должно проверяться наличие слова в выводе.
'''
import subprocess
import string
import re

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = str((re.sub(r"[_\=\.\:\//]", ' ', result.stdout)).split('\n'))
#    print(out)
    res_out = out.translate(str.maketrans('', '', string.punctuation))
    print(res_out)

    if result.returncode == 0 and text in res_out:
        return True
    else:
        return False

if __name__ == '__main__':
    print(checkout('cat /etc/os-release', 'jammy'))