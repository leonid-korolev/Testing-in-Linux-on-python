'''
Задание 2. (повышенной сложности)

Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
в котором вывод разбивается на слова с удалением всех знаков пунктуации (их можно взять из списка
string.punctuation модуля string). В этом режиме должно проверяться наличие слова в выводе.
'''
import string
import subprocess
from string import punctuation
import re

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = str((result.stdout).split('\n'))
#    print(out)
    out_res = re.sub(r'[_\=\.\:\//]',' ', out)
#    print(out_res)
    fin_res = out_res.translate(str.maketrans('', '', string.punctuation))
    print(fin_res)

    if result.returncode == 0 and text in fin_res:
        return True
    else:
        return False

if __name__ == '__main__':
    print(checkout('cat /etc/os-release', 'jammy'))