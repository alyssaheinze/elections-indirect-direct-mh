#!/usr/bin/python3
import os
import sys
import textdistance

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
from src.classes.csv_writer import CsvWriter
from src.utils.helper import Helper
from src.config.blocks import BLOCKS


def read_user_input(number_of_choice):
    value = input(f'Please enter 1 to {number_of_choice + 1}\n')
    try:
        value = int(value)
        if value < 1 or value > number_of_choice + 1:
            raise
    except:
        value = input(f'Please enter 1 to {number_of_choice + 1}\n')
        value = int(value)
        if value < 1 or value > number_of_choice + 1:
            raise Exception('Incorrect input')
    return value - 1


def find_block_name_from_id(block_id):
    for name, id in BLOCKS.items():
        if id == block_id:
            return name
    raise Exception(f'Did not find a match for {block_id}')


def main():
    file_path = 'C:/Data_Perso/elections-indirect-direct-mh/inputs/election_dates_wide.csv'
    lines = CsvWriter.read(file_path)

    date_villages = {}
    for line in lines:
        district = line[1]
        block = line[2]
        panchayat = line[3].lower()

        block_id = BLOCKS.get(f'{district},{block}')
        if block_id is None:
            # print(f'Error no match found for {district},{block}')
            continue

        if date_villages.get(block_id) is None:
            date_villages[block_id] = []
        obj = {
            'name': panchayat,
            'line': line
        }
        date_villages[block_id].append(obj)

    new_lines = []

    file_path = 'C:/Data_Perso/elections-indirect-direct-mh/intermediary_results/Reservation_Sarpanch_Gram_Sevak_Group_Upa_Sarpanch_Election_Date.csv'
    lines = CsvWriter.read(file_path, nb_of_lines_to_be_skipped=0)

    skip_first = True
    for line in lines:
        if skip_first is True:
            skip_first = False
            district_column_pos = Helper.find_column_position(line, 's_q6')
            block_column_pos = Helper.find_column_position(line, 's_q5')
            villagename_column_pos = Helper.find_column_position(line, 's_q1')
            new_first_line = line
            new_lines.append(new_first_line)
            continue
        if len(line) > 1290:
            new_lines.append(line)
            continue
        block_id = int(line[block_column_pos])
        district = line[district_column_pos]
        panchayat = line[villagename_column_pos]
        panchayat = panchayat.lower().replace('grampanchayat', '')

        if block_id not in BLOCKS.values():
            raise Exception(f'Error block {block_id} not found in config')

        potential_matches = date_villages[block_id]
        if panchayat in potential_matches:
            continue

        cmp_results = []
        for village in potential_matches:
            cmp_results.append({
                'score': textdistance.hamming(panchayat, village['name']),
                'match': village['name'],
                'line': village['line']
            })
        cmp_results.sort(key=lambda v: v['score'])
        print(f'{panchayat} to be matched within district {district} block {block_id} == {find_block_name_from_id(block_id)}')
        number_of_choice = 10
        for idx, cmp_result in enumerate(cmp_results[0:number_of_choice]):
            print('{:>2} {}'.format(cmp_result['score'], cmp_result['match']))
        print()
        selected_row = read_user_input(number_of_choice)
        if selected_row < number_of_choice:
            end_of_new_line = cmp_results[selected_row]['line']
        else:
            end_of_new_line = []
        new_line = line + end_of_new_line
        new_lines.append(new_line)

    file_path = 'C:/Data_Perso/elections-indirect-direct-mh/intermediary_results/Reservation_Sarpanch_Gram_Sevak_Group_Upa_Sarpanch_Election_Date.csv'
    CsvWriter.write(file_path, new_lines)


if __name__ == '__main__':
    main()
