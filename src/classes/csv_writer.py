import csv
import re


class CsvWriter:

    @staticmethod
    def write(file_path, lines, delimiter=','):
        file_path = re.sub(r'[#%&{}<>*?$!\'"@+`|=]', '', file_path)
        with open(file_path, 'w', newline='', encoding='utf8') as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter)
            for line_array in lines:
                writer.writerow(line_array)

    @staticmethod
    def read(file_path, nb_of_lines_to_be_skipped=1, delimiter=','):
        with open(file_path, 'r', encoding='utf8') as original:
            lines = csv.reader(original, delimiter=delimiter)
            all_lines = []
            for idx, line in enumerate(lines):
                for i, column in enumerate(line):
                    line[i] = column.strip()
                all_lines.append(line)
            return all_lines[nb_of_lines_to_be_skipped:]
