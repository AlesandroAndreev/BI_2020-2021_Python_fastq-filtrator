#Импорт библиотеки
import re
import os, sys
#_________________________________________________Ввод_переменных______________________________________________________
way_to_read = input("Write the way to read: ")
way_to_write = input("Write the way to write: ")
size_param = int(input("Write size: "))


maximum = int(input("Верхняя граница: "))
minimum = int(input("Нижняя граница: "))


flag_write = 0
to_write = ""
len_of_string = 0
#_________________________________________________Функции______________________________________________________


def filtrator(size_param, contig_size): #Функция фильтрует по размеру

    flag = 0

    if contig_size < size_param:
        flag = 1

    return flag


def seq_size(first_string): #Функция узнает какой размер у фрагмента
    size_string = re.search(r"length=[-+]?\d+",first_string)[0]
    return int(re.search(r"[-+]?\d+",size_string)[0])


def gc_counter(seq, gc_max=100, gc_min=0): #Функция определяет gc состав

    gc_bases = 0

    for nucl in seq:
        if nucl in ["G","C"]:
            gc_bases += 1

    if gc_min <= (gc_bases/len(seq))*100 <= gc_max:
        flag = 0
    else:
        flag = 1

    return flag

#_________________________________________________Тело_кода_____________________________________________________________


fastq = open(way_to_read , 'r')
file = open(way_to_write + '.fastq', 'w')

for lines in fastq:

    if "length" in lines:
        flag_write = filtrator(size_param, seq_size(lines))
        len_of_string = len(lines)

    elif re.search(r"^[A|C|T|G|N][A|C|T|G|N]",lines):
        flag_write = gc_counter(lines, maximum, minimum)

        if flag_write == 1:
            to_write = to_write[0:len(to_write) - len_of_string ]

    if flag_write != 1:
        to_write = to_write + lines
        if re.search(r"^@", lines) and "length" not in lines:
            file.write(to_write)
            to_write = ""

file.close()
fastq.close()






'''
        
/Users/alexandreev/Desktop/amp_res_1.fastq
/Users/alexandreev/Desktop/ans
101
/Users/alexandreev/Desktop/test.fastq
'''
