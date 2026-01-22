import typing
import json
import argparse
import math
from dataclasses import dataclass
from pathlib import Path

# region: Loader and Saver


class SrtEntry:
    __start_timestamp: float
    __end_timestamp: float
    __content: str

    def __init__(self, start_timestamp: float, end_timestamp: float, content: str):
        self.__start_timestamp = start_timestamp
        self.__end_timestamp = end_timestamp
        self.__content = content

    def __conv_to_srt_timestamp(self, sec: float) -> str:
        decimal_milliseconds, decimal_seconds = math.modf(sec)
        milliseconds = int(decimal_milliseconds * 1000)
        decimal_minutes, seconds = divmod(int(decimal_seconds), 60)
        hours, minutes = divmod(decimal_minutes, 60)
        return f'{hours:0>2d}:{minutes:0>2d}:{seconds:0>2d},{milliseconds:0>3d}'

    def get_start_timestamp(self) -> str:
        return self.__conv_to_srt_timestamp(self.__start_timestamp)
    
    def get_end_timestamp(self) -> str:
        return self.__conv_to_srt_timestamp(self.__end_timestamp)
    
    # def __fix_content(self, content: str) -> str:
    #     return content.encode('iso8859-1', errors='ignore').decode('utf-8', errors='ignore')

    def get_content(self) -> str:
        # return self.__fix_content(self.__mContent)
        return self.__content


def load_bili_srt(filename: Path) -> typing.Iterator[SrtEntry]:
    with open(filename, 'r', encoding='utf-8') as fs:
        data = json.load(fs)
        for entry in data['body']:
            yield SrtEntry(entry['from'], entry['to'], entry['content'])


def save_standard_srt(filename: Path, entries: typing.Iterator[SrtEntry]) -> None:
    with open(filename, 'w', encoding='utf-8') as fs:
        for idx, entry in enumerate(entries):
            fs.write(f'{idx + 1}\n')
            fs.write(f'{entry.get_start_timestamp()} --> {entry.get_end_timestamp()}\n')
            fs.write(entry.get_content())
            fs.write('\n\n')

# endregion

# region: Command Line Options


@dataclass
class Options:
    """The class representing accepted command line options."""

    input: Path
    """The path to input Bilibili subtitle file."""
    output: Path
    """The path to output SRT file."""


def parse() -> Options:
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
    return Options(
        Path(args.input).resolve(), Path(args.output).resolve()
    )

# endregion


def main():
    # parse cli options
    cli = parse()

    # convert bilibili subtitle to srt subtitle
    save_standard_srt(cli.output, load_bili_srt(cli.input))
    print('Convertion Done.')


if __name__ == '__main__':
    main()
