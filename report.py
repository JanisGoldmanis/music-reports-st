import csv

import pandas as pd
from helpers import get_seconds_from_timecode
from read_songs_csv import get_song_dictionary
from storyblocks_api import get_api_info
import streamlit as st


def format_song_name(song_name: str) -> str:
    modified_song_name = song_name
    return modified_song_name


def add_song_to_db(file: str, song: dict):

    # Name,Composer,Musician,Producer,Record Company

    with open(file, 'a', newline='') as csvfile:
        line = [song['name'],song['composer'],song['musician'],song['producer'],song['record_company']]
        writer = csv.writer(csvfile)

        writer.writerow(line)

        return True



def get_music_info_from_input(input_rows: list[str]) -> list[str]:

    # Remove header
    lines = input_rows[2:]

    while len(lines) > 0:

        # Remove empty blank row
        if len(lines[0].strip()) == 0:
            lines.pop(0)

        # All rows processed
        if len(lines) == 0:
            break

        first_line = lines.pop(0).strip()
        second_line = lines.pop(0).strip()

        # Song timestamps
        first_line_items = [x for x in first_line.split(" ") if len(x) > 0]

        duration = get_seconds_from_timecode(first_line_items[7]) - get_seconds_from_timecode(first_line_items[6])

        # st.write(first_line_items)
        # st.write(duration)

        song = second_line.split(":")[-1].strip().replace('-', ' ')[:-4]

        # st.write(song)

    return lines


def get_report(input_report: list[str]) -> pd.DataFrame:
    lines = input_report[2:] # remove header

    song_lines = get_music_info_from_input(input_report)

    song_data = get_song_dictionary('data/songs.csv')

    song_duration = {}
    song_count = {}

    previous = []

    print(f"Duration | Song")
    while len(lines) > 0:

        # Remove empty
        if len(lines[0].strip()) == 0:
            lines.pop(0)

        if len(lines) == 0:
            break

        first = lines.pop(0).strip()
        second = lines.pop(0).strip()

        # Song timestamps
        first = [x for x in first.split(" ") if len(x) > 0]
        try:
            duration = get_seconds_from_timecode(first[7]) - get_seconds_from_timecode(first[6])
            duration2 = get_seconds_from_timecode(first[5]) - get_seconds_from_timecode(first[4])
            if duration < 0:
                print('CHECK ERROR 2')
                # if duration != duration2:
                # print('CHECK ERROR 3')
        except:
            print('CHECK ERROR 1')
        song = second.split(":")[-1].strip().replace('-', ' ')[:-4]

        if song not in song_duration:
            song_duration[song] = 0
            song_count[song] = 0

        song_duration[song] += duration
        song_count[song] += 1

        if song_count[song] >= 2:
            previous_end = previous[0][7]
            current_start = first[6]
            if previous_end == current_start:
                previous_song = previous[1].split(":")[-1].strip()
                if song == previous_song:
                    song_count[song] -= 1

        print(f"{duration:>8} | {song}")
        if len(lines) == 0:
            break

        previous = [first, second]

        # Remove AUD
        if lines[0][:3] == 'AUD':
            lines.pop(0)

    print()

    known_songs = []
    unknown_songs = []

    for song in song_duration:
        if song not in song_data:
            last_part_of_song_name = song.split(' ')[-1]
            SBA_id = ''

            if last_part_of_song_name.isnumeric():
                SBA_id = int(last_part_of_song_name)

            unknown_songs.append({'name': song,
                                  'producer': '',
                                  'musician': '',
                                  'composer': '',
                                  'record_company': '',
                                  'sba': SBA_id})
        else:
            known_songs.append(song)


    for song in unknown_songs:
        print(f'Working Song: {song}')

        st.write(f'Getting song {song}')

        sba = str(song['sba'])

        st.write(sba)

        if len(sba) == 0:
            st.write(f'Song {song} has no SBA!')
            continue

        api_info = get_api_info(f'{song["sba"]}')

        if not api_info:
            st.write(f'Song {song} has no API!')
            continue

        st.write(f"{api_info}")

        if len(api_info) > 0:
            song['producer'] = api_info['producer']
            song['musician'] = api_info['musician']
            song['producer'] = api_info['producer']
            song['composer'] = api_info['composer']
            song['record_company'] = api_info['record_company']

        st.write('Added to db')
        st.write(song)

        add_song_to_db('data/songs.csv', song)

    # result = {}
    #
    # for song in song_duration:
    #     try:
    #         result[song] = {'name': song, 'duration': song_duration[song], 'count': song_count[song],
    #                         'musician': song_data[song].musician,
    #                         'composer': song_data[song].composer,
    #                         'producer': song_data[song].producer,
    #                         'record_company': song_data[song].record_company,
    #                         'sba': song_data[song].sba}
    #     except:
    #         st.write('No data for song', song)

    result = {}

    for song in song_duration:
        try:
            result[song] = {
                'Episode Nr': '',
                'Song Name': song,
                'Fonogram ISRC': '',
                'CAE/IPI': '',
                'Year': '',
                'Album': '',
                'Digital Music Bank': 'https://www.storyblocks.com/',
                'Composer': song_data[song].composer,
                'Text Author': '',
                'Arranger': '',
                'Musician': song_data[song].musician,
                'Producer': song_data[song].producer,
                'Record Label': song_data[song].record_company,
                'Fonogramma vai Live': 'Fonogramma',
                'Quantity': song_count[song],
                'Duration': song_duration[song],
            }
        except:
            st.write('No data for song', song)

    # result['Episode Nr'] = ''
    # result['Fonogram ISRC'] = ''

    return pd.DataFrame(result.values())



