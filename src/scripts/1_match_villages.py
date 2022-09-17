#!/usr/bin/python3
import os
import sys
import textdistance

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
from src.classes.csv_writer import CsvWriter
from src.utils.helper import Helper
from src.config.blocks import BLOCKS


def read_user_input():
    value = input('Please enter 1 to 5\n')
    try:
        value = int(value)
        if value < 1 or value > 5:
            raise
    except:
        value = input('Please enter 1 to 5\n')
        value = int(value)
        if value < 1 or value > 5:
            raise Exception('Incorrect input')
    return value


def main():
    file_path = 'C:/Data_Perso/elections-indirect-direct-mh/inputs/election_dates_wide.csv'
    lines = CsvWriter.read(file_path)

    date_villages = {}
    for line in lines:
        district = line[1]
        block = line[2]
        panchayat = line[3]

        block_id = BLOCKS.get(f'{district},{block}')
        if block_id is None:
            # print(f'Error no match found for {district},{block}')
            continue

        if date_villages.get(block_id) is None:
            date_villages[block_id] = []
        date_villages[block_id].append(panchayat)

    file_path = 'C:/Data_Perso/elections-indirect-direct-mh/inputs/Reservation_Sarpanch_Gram_Sevak_Group_Upa_Sarpanch.csv'
    lines = CsvWriter.read(file_path, nb_of_lines_to_be_skipped=0)

    sarpanch_villages = {}

    skip_first = True
    # district_column_pos = None
    villageid_column_pos = None
    villagename_column_pos = None
    for line in lines:
        if skip_first is True:
            skip_first = False
            # district_column_pos = Helper.find_column_position(line, 's_q6')
            block_column_pos = Helper.find_column_position(line, 's_q5')
            villageid_column_pos = Helper.find_column_position(line, 's_villageid')
            villagename_column_pos = Helper.find_column_position(line, 's_q1')
            continue
        # district_id = line[district_column_pos]
        block_id = int(line[block_column_pos])
        panchayat = line[villagename_column_pos]
        village_id = line[villageid_column_pos]

        if block_id not in BLOCKS.values():
            print(f'Error block {block_id} not found in config')
            continue

        if sarpanch_villages.get(block_id) is None:
            sarpanch_villages[block_id] = []
        village = {
            'id': village_id,
            'name': panchayat
        }
        sarpanch_villages[block_id].append(village)

    for block_id, villages_to_match in date_villages.items():
        potential_matches = sarpanch_villages[block_id]
        for date_village in villages_to_match:
            if date_village in potential_matches:
                continue

            cmp_results = []
            for village in potential_matches:
                cmp_results.append({
                    'score': textdistance.hamming(date_village, village['name']),
                    'match': village['name'],
                    'id': village['id'],
                    # 'line': village['line']
                })
            cmp_results.sort(key=lambda v: v['score'])
            print(f'{date_village} vs {cmp_results[0]["match"]} = {cmp_results[0]["score"]}')
            if cmp_results[0]['score'] > 10:
                for idx, cmp_result in enumerate(cmp_results[0:4]):
                    print('{:>2} {}'.format(cmp_result['score'], cmp_result['match']))
                print()
                # selected_row = read_user_input() - 1
                # if selected_row < 4:
                #     line = cmp_results[selected_row]['line']
                # elif selected_row == 4:
                #     line = []


    #
    # for line in lines:
    #     res = Helper.find_column_position(line, 's_q5')
    #     res = Helper.find_column_position(line, 's_q6')
    #
    #     division = line[0]
    #     district = line[1]
    #     block = line[2]
    #     panchayat = line[3]
    #
    # final_file_path = f'C:/Data_PoloFr/scrap-maharashtra-gp/results/election_dates_wide.csv'
    # with open(final_file_path, 'w', newline='', encoding='utf8') as csv_file:
    #     csv_file.writelines(lines)


if __name__ == '__main__':
    main()
