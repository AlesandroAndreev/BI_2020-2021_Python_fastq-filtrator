from sys import argv
import re

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


control_flag = True
massage = "Wrong with {} argument. Please try again!"
output_base_name = ""
file_pattern = re.compile(r'\w+\.fastq')
length_min = 0
keep_filtered_flag = False
gc_maximum = 100
gc_minimum = 0

try:
    output_base_name = file_pattern.search(argv[len(argv) - 1]).group()[0:-6]
except TypeError and AttributeError:
    control_flag = False
    massage.format("input file")

to_write_passed = []
to_write_failed = []

for index, arg in enumerate(argv):
    if arg in ["--min_length"] and len(argv) > index + 1:
       try:
           length_min = int(argv[index + 1])
       except ValueError:
           control_flag = False
           massage.format("min_length")
    elif arg in ["--gc_bounds"] and len(argv) > index + 1:
        try:
            gc_minimum = int(argv[index + 1])
        except ValueError:
            control_flag = False
            massage.format("gc_bounds")
        try:
            gc_maximum = int(argv[index + 2])
            if gc_minimum > gc_maximum:
                control_flag = False
                massage.format("gc_bounds")
        except ValueError:
            gc_maximum = gc_minimum
            gc_minimum = 0
    elif arg in ["--keep_filtered"] and len(argv) > index + 1:
        keep_filtered_flag = True
    elif arg in ["--output_base_name"] and len(argv) > index + 1:
        output_base_name = argv[index + 1]


if control_flag is True:

    input_fastq_file = open(argv[len(argv) - 1], 'r')
    output_fastq_file_passed_reads = open(output_base_name + '__passed.fastq', 'w')

    if keep_filtered_flag is True:
        output_fastq_file_failed_reads = open(output_base_name + '__failed.fastq', 'w')

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
else:
    print(massage)

print(length_min)
print(gc_minimum)
print(gc_maximum)
