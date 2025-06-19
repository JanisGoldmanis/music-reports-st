def get_seconds_from_timecode(timecode):
    timecode_list = timecode.split(":")
    seconds = 0
    for value in timecode_list[:-1]:
        seconds = seconds * 60 + int(value)
    return seconds