import typing
import json
import argparse
import math

class SrtEntry:
    __mStartTimestamp: float
    __mEndTimestamp: float
    __mContent: str

    def __init__(self, start_timestamp: float, end_timestamp: float, content: str):
        self.__mStartTimestamp = start_timestamp
        self.__mEndTimestamp = end_timestamp
        self.__mContent = content

    # def __fix_content(self, content: str) -> str:
    #     return content.encode('iso8859-1', errors='ignore').decode('utf-8', errors='ignore')

    def __conv_to_srt_timestamp(self, sec: float) -> str:
        decimal_milliseconds, decimal_seconds = math.modf(sec)
        milliseconds = int(decimal_milliseconds * 1000)
        decimal_minutes, seconds = divmod(int(decimal_seconds), 60)
        hours, minutes = divmod(decimal_minutes, 60)
        return f'{hours:0>2d}:{minutes:0>2d}:{seconds:0>2d},{milliseconds:0>3d}'

    def get_start_timestamp(self) -> str:
        return self.__conv_to_srt_timestamp(self.__mStartTimestamp)
    
    def get_end_timestamp(self) -> str:
        return self.__conv_to_srt_timestamp(self.__mEndTimestamp)
    
    def get_content(self) -> str:
        # return self.__fix_content(self.__mContent)
        return self.__mContent

def enumerate_srt_entry(filename: str) -> typing.Iterator[SrtEntry]:
    with open(filename, 'r', encoding='utf-8') as fs:
        data = json.load(fs)
        for entry in data['body']:
            yield SrtEntry(entry['from'], entry['to'], entry['content'])

def write_srt_entry(filename: str, entries: typing.Iterator[SrtEntry]) -> None:
    with open(filename, 'w', encoding='utf-8') as fs:
        for idx, entry in enumerate(entries):
            fs.write(f'{idx + 1}\n')
            fs.write(f'{entry.get_start_timestamp()} --> {entry.get_end_timestamp()}\n')
            fs.write(entry.get_content())
            fs.write('\n\n')


if __name__ == '__main__':
    # Prepare arg parser and do parse
    parser = argparse.ArgumentParser(
        prog='Bilibili Subtitle To SRT',
        description='Convert Bilibili specific subtitle into universal SRT format.'
    )
    parser.add_argument(
        '-i', '--input', action='store', required=True, dest='input',
        help='''
        The path to the JSON file which store Bilibili subtitle JSON.
        It usually is fetched from "aisubtitle.hdslb.com" domain by browser.
        '''
    )
    parser.add_argument(
        '-o', '--output', action='store', required=True, dest='output',
        help='The destination file storing SRT subtitle.'
    )
    args = parser.parse_args()

    # convert bilibili subtitle to srt subtitle
    write_srt_entry(args.output, enumerate_srt_entry(args.input))
    print('Convertion Done.')
