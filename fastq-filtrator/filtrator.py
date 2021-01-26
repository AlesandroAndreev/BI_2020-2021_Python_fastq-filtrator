#Импорт библиотеки
import re
import os, sys
#_________________________________________________Ввод_переменных______________________________________________________
way_to_read = input("Write the way to read: ")
way_to_write = input("Write the way to write: ")
way_to_error = input("Write the way to error: ")
err_file_flag = input("Do you want file for wrong reads. Write True or False:")
size_param = int(input("Write size: "))


maximum = int(input("Верхняя граница: "))
minimum = int(input("Нижняя граница: "))



to_write = ""
len_of_string = 0
sum_of_all_gc_nucleotides = 0
summarize_length_of_seq = 0
flag_write = True
#_________________________________________________Функции______________________________________________________
def filter_by_length(length_limit, read_header):
    if length_limit < read_header:
        return False
    else:
        return True

def count_gc_content_in_line(seq):

    gc_nucleotides = 0

    for nucleotide in seq:
        if nucleotide in ["G","C"]:
            gc_nucleotides += 1
    return gc_nucleotides, len(seq) - 1


def content_of_gc_nucleotides(all_gc_nucleotides, length_of_seq):
    return (all_gc_nucleotides/length_of_seq)*100


def filter_by_gc_content(content, gc_max=100, gc_min=0):
    if gc_min <= content <= gc_max:
        return True
    else:
        return False
#_________________________________________________Тело_кода_____________________________________________________________


fastq = open(way_to_read , 'r')
file = open(way_to_write + '.fastq', 'w')

if err_file_flag is True:
    file_error = open(way_to_error + '.fastq','w')

for lines in fastq:

    if ("length" in lines) and (len(to_write) > 1):
        if flag_write is True:
            file.write(to_write)
            to_write = ""
            len_of_string = 0
            sum_of_all_gc_nucleotides = 0
            summarize_length_of_seq = 0
        elif (flag_write is False) and (err_file_flag is True):
            file_error.write(to_write)
            to_write = ""
            len_of_string = 0
            sum_of_all_gc_nucleotides = 0
            summarize_length_of_seq = 0
            file_error.close()
        else:
            to_write = ""
            len_of_string = 0
            sum_of_all_gc_nucleotides = 0
            summarize_length_of_seq = 0


    elif re.search(r"^[A|C|T|G|N][A|C|T|G|N]",lines) and "+" not in to_write:
        sum_of_all_gc_nucleotides += count_gc_content_in_line(lines)[0]
        summarize_length_of_seq += count_gc_content_in_line(lines)[1]

    elif re.search(r"^[+]",lines):
        gc_content = content_of_gc_nucleotides( sum_of_all_gc_nucleotides, summarize_length_of_seq)
        flag_write = (filter_by_length(size_param, summarize_length_of_seq) and filter_by_gc_content(gc_content, maximum,minimum))


    to_write += lines



try:
    file_error.close()
except:
    pass

file.close()
fastq.close()



'''

/Users/alexandreev/Desktop/amp_res_1.fastq
/Users/alexandreev/Desktop/ans
/Users/alexandreev/Desktop/ans_err
101
/Users/alexandreev/Desktop/test.fastq
'''
