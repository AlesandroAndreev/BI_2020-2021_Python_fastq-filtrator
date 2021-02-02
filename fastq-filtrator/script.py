import sys
import re

path_to_input_fastq_file = input("Write path to input reads: ")
path_to_output_fastq_file = input("Write path to output reads: ")

keep_filtered_flag = bool(input("Indicate filtered reads to be saved in a separate file (True or False): "))

length_min = int(input("Indicate min read length: "))

gc_maximum = int(input("Indicate upper GC bound: "))
gc_minimum = int(input("Indicate lower GC bound: "))


def get_read_length(read_header):
    read_length = re.search(r"length=[-+]?\d+", read_header)[0]
    return int(re.search(r"[-+]?\d+", read_length)[0])


def filter_by_length(length_min, read_header):
    local_flag_to_write = False
    if get_read_length(read_header) >= length_min:
        local_flag_to_write = True
    return local_flag_to_write


def count_gc_content(sequence):
    gc_nucleotides = 0
    for nucleotide in sequence:
        if nucleotide in ["G", "C"]:
            gc_nucleotides += 1
    return round((gc_nucleotides / len(sequence)) * 100)


def filter_by_gc_content(gc_maximum, gc_minimum, sequence):
    local_flag_to_write = False
    if gc_minimum - 1 < count_gc_content(sequence) < gc_maximum:
        local_flag_to_write = True
    return local_flag_to_write


to_write_passed = []
to_write_failed = []

input_fastq_file = open(path_to_input_fastq_file, 'r')
output_fastq_file_passed_reads = open(path_to_output_fastq_file + '__passed.fastq', 'w')
if keep_filtered_flag is True:
    output_fastq_file_failed_reads = open(path_to_output_fastq_file + '__failed.fastq', 'w')

for line in input_fastq_file:

    if len(to_write_passed) == 0:

        if "length" in line:

            if filter_by_length(length_min, line) is True:
                to_write_passed.append(line)

            elif filter_by_length(length_min, line) is False:
                to_write_failed.append(line)
        else:
            to_write_failed.append(line)

    elif len(to_write_passed) == 1:

        if filter_by_gc_content(gc_maximum, gc_minimum, line) is True:
            to_write_passed.append(line)

        else:
            to_write_failed.append(to_write_passed[0])
            to_write_failed.append(line)
            to_write_passed = []

    elif len(to_write_passed) == 2:
        to_write_passed.append(line)

    elif len(to_write_passed) == 3:
        to_write_passed.append(line)

        for passed_line in to_write_passed:
            output_fastq_file_passed_reads.write(passed_line)

        to_write_passed = []

    if keep_filtered_flag is True:
        for failed_line in to_write_failed:
            output_fastq_file_failed_reads.write(failed_line)
        to_write_failed = []

if keep_filtered_flag is True:
    output_fastq_file_failed_reads.close()

output_fastq_file_passed_reads.close()
input_fastq_file.close()

'''
import sys
import re

path_to_input_fastq_file = input("Write path to input reads: ")
path_to_output_fastq_file = input("Write path to output reads: ")

keep_filtered_flag = input("Indicate filtered reads to be saved in a separate file (True or False): ")
if keep_filtered_flag == "True":
    keep_filtered_flag = True
else:
    keep_filtered_flag = False

length_min = int(input("Indicate min read length: "))

gc_maximum = int(input("Indicate upper GC bound: "))
gc_minimum = int(input("Indicate lower GC bound: "))


def get_read_length(read_header):
    read_length = re.search(r"length=[-+]?\d+", read_header)[0]
    return int(re.search(r"[-+]?\d+", read_length)[0])

def filter_by_length(length_min, read_header):
    local_flag_to_write = False
    if get_read_length(read_header) >= length_min:
        local_flag_to_write = True
    return local_flag_to_write

def count_gc_content(sequence):
    gc_nucleotides = 0
    for nucleotide in sequence:
        if nucleotide in ["G", "C"]:
            gc_nucleotides += 1
    return round((gc_nucleotides / len(sequence)) * 100)

def filter_by_gc_content(gc_maximum, gc_minimum, sequence):
    local_flag_to_write = False
    if gc_minimum - 1 < count_gc_content(sequence) < gc_maximum:
        local_flag_to_write = True
    return local_flag_to_write


to_write_passed = []
to_write_failed = []

input_fastq_file = open(path_to_input_fastq_file, 'r')
output_fastq_file_passed_reads = open(path_to_output_fastq_file + '__passed.fastq', 'w')
if keep_filtered_flag:
    output_fastq_file_failed_reads = open(path_to_output_fastq_file + '__failed.fastq', 'w')


for line in input_fastq_file:

    if len(to_write_passed) == 0:

        if "length" in line:

            if filter_by_length(length_min, line):
                to_write_passed.append(line)

            else:
                to_write_failed.append(line)

        else:
            to_write_failed.append(line)

    elif len(to_write_passed) == 1:

        if filter_by_gc_content(gc_maximum, gc_minimum, line):
            to_write_passed.append(line)

        else:
            to_write_passed = []
            to_write_failed.append(line)

    elif len(to_write_passed) == 2:
        to_write_passed.append(line)

    elif len(to_write_passed) == 3:
        to_write_passed.append(line)

        for passed_line in to_write_passed:
            output_fastq_file_passed_reads.write(passed_line)

        to_write_passed = []


    if keep_filtered_flag and to_write_failed:
        for failed_line in to_write_failed:
            output_fastq_file_failed_reads.write(failed_line)
        to_write_failed = []


if keep_filtered_flag:
    output_fastq_file_failed_reads.close()

output_fastq_file_passed_reads.close()
input_fastq_file.close()

'''
