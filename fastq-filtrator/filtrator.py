import re

way_to_read = input("Write the way to read: ")
way_to_write = input("Write the way to write: ")
size_param = int(input("Write size: "))
flag_write = 0

def filtrator(size_param, contig_size, flag_write):

    if contig_size < size_param:
        flag_write = 1

    return flag_write

def seq_size(first_string):
    size_string = re.search(r"length=[-+]?\d+",first_string)[0]

    return int(re.search(r"[-+]?\d+",size_string)[0])




with open(way_to_read,"r") as fastq:

    for lines in fastq:

        print(lines)

        if "length" in lines:
            flag_write =  filtrator(size_param, seq_size(lines),flag_write)

        if flag_write != 1:

            with open(way_to_write,"a") as fastq_sort:
                fastq_sort.write(lines)






#/Users/alexandreev/Desktop/amp_res_1.fastq
#/Users/alexandreev/Desktop/ans.fastq
#100
