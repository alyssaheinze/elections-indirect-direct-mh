#!/usr/bin/python3
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
from src.classes.csv_writer import CsvWriter


def main():
    new_lines = []
    file_path = 'C:/Data_Perso/elections-indirect-direct-mh/intermediary_results/Reservation_Sarpanch_Gram_Sevak_Group_Upa_Sarpanch_Election_Date.csv'
    lines = CsvWriter.read(file_path, nb_of_lines_to_be_skipped=0)

    skip_first = True
    for index, line in enumerate(lines):
        if skip_first is True:
            print(f'parsed_dates 1291 {line[1291]}')
            skip_first = False
            new_lines.append(line)
            continue
        if len(line) < 1291:
            new_lines.append(line)
            continue
        parsed_dates = line[1291].split(';')
        dates = line[1292].split(';')
        if len(parsed_dates) > len(dates):
            print('Error for the following cases')
            print(line[1291])
            print(line[1292])
            raise Exception(f'At line {index}: {len(parsed_dates)} != {len(dates)}')
        line.pop()
        line.pop()
        for i, date in enumerate(dates):
            parsed_date = ''
            try:
                parsed_date = parsed_dates[i]
            except IndexError:
                pass
            line.append(parsed_date)
            line.append(date)
        new_lines.append(line)

    file_path = 'C:/Data_Perso/elections-indirect-direct-mh/intermediary_results/Reservation_Sarpanch_Gram_Sevak_Group_Upa_Sarpanch_Election_Date_2.csv'
    CsvWriter.write(file_path, new_lines)


if __name__ == '__main__':
    main()
