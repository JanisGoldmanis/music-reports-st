from models.song import Song
import csv
from typing import Dict


def get_song_dictionary(filepath: str) -> Dict[str, Song]:
    song_dictionary = {}

    with open(filepath, newline='', encoding='latin1') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()
        for row in reader:
            name = row[0]

            if name in song_dictionary:
                continue

            composer = row[1]
            musician = row[2]
            producer = row[3]
            record_company = row[4]

            song_dictionary[name] = Song(name, composer, musician, producer, record_company)

    return song_dictionary


