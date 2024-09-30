import argparse
import re

class ChapterInfo:
    mStartTimestamp: str
    mEndTimestamp: str
    mName: str

    def __init__(self, start_timestamp: str, end_timestamp: str, name: str) -> None:
        self.mStartTimestamp = start_timestamp
        self.mEndTimestamp = end_timestamp
        self.mName = name

    def __repr__(self) -> str:
        return f'<{self.mStartTimestamp}-{self.mEndTimestamp} {self.mName}>'

def extract_info(filename: str) -> tuple[ChapterInfo, ...]:
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    ret: list[ChapterInfo] = []
    timestamp_pattern: re.Pattern = re.compile('([0-9:]+)-([0-9:]+)')

    for item in data:
        item = item.strip()
        if item == '': continue

        sp = item.split(' ')
        timestamp_part = sp[0]
        name_part = ' '.join(sp[1:])

        matched_timestamp = timestamp_pattern.match(timestamp_part)
        start_timestamp: str = matched_timestamp.group(1)
        end_timestamp: str = matched_timestamp.group(2)

        ret.append(ChapterInfo(start_timestamp, end_timestamp, name_part))

    return tuple(ret)

def generate_command(chapters: tuple[ChapterInfo, ...]) -> str:
    ret: str = 'ffmpeg -i audio.m4s '
    for chapter in chapters:
        ret += f'-ss {chapter.mStartTimestamp} -to {chapter.mEndTimestamp} -vn "{chapter.mName}.m4a" '
    return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str, action='store', dest='input')
    args = parser.parse_args()

    chapters = extract_info(args.input)
    result = generate_command(chapters)
    print(result)