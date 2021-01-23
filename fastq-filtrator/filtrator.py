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

def gc_counter(seq,gc_parametr,flag_write):
    gc_bases = 0

    for nucl in seq:
        if nucl in ["G","C"]:
            gc_bases += 1

    if (len(seq)/gc_bases)*100 > gc_parametr:
        flag_write = 1

    return flag_write


fastq = open(way_to_read , 'r')
file = open(way_to_write + '.fastq', 'w')



for lines in fastq:

    if "length" in lines:
        if filtrator(size_param, seq_size(lines), flag_write) != 1:
            flag_write = filtrator(size_param, seq_size(lines), flag_write)
            file.write(lines + '\n')
    elif r"^[A|C|T|G][A|C|T|G]" in lines:
        pass

        
        if flag_write != 1:
            file.write(lines + '\n')

file.close()
fastq.close()






'''
        
/Users/alexandreev/Desktop/amp_res_1.fastq
/Users/alexandreev/Desktop/ans
101

'''
