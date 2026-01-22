import argparse
import re
import enum
import logging
from pathlib import Path
from dataclasses import dataclass
from tabulate import tabulate

# region: Extractor

@dataclass
class ChapterInfo:
    """The class representing chapter info."""

    start_timestamp: str | None
    """The start timestamp of this chapter. None for the start of audio."""
    end_timestamp: str | None
    """The end timestamp of this chapter. None for the end of audio."""
    name: str
    """The name of this chapter."""


class ChapterStyle(enum.StrEnum):
    TIME_RANGE = 'range'
    """The style of chapter info is time range like `00:00:00-00:01:00 name`."""
    TIME_POINT = 'point'
    """The style of chapter info is time point like `00:00:00 name`."""


def extract_chapter_from_range_style(filename: Path) -> list[ChapterInfo]:
    """
    Extract chapter info from a file with chapter style of time range.

    In files with this style, each line should be like `00:00:00-00:01:00 name`.

    :param filename: The path to input file.
    """
    # Prepare return value and Regex for matching
    rv: list[ChapterInfo] = []
    TIMESTAMP_PATTERN: re.Pattern = re.compile("([0-9:]+)-([0-9:]+)")

    # Open file and start to process.
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            # Remove blank line
            line = line.strip()
            if line == "": continue

            # Match timestamp part
            matched_timestamp = TIMESTAMP_PATTERN.match(line)
            if matched_timestamp is None:
                logging.warning(f'Non-blank line found, but not match timestamp pattern: {line}')
                continue
            # Extract timestamp info
            start_timestamp: str = matched_timestamp.group(1)
            end_timestamp: str = matched_timestamp.group(2)

            # Remove timestamp part from line to get
            match_start, match_end = matched_timestamp.span()
            name_part = line[:match_start] + line[match_end:]
            # Strip all blanks
            name_part = name_part.strip()
            if len(name_part) == 0:
                logging.warning(f'Blank name part is not allowed: {line}')

            # Add into result.
            rv.append(ChapterInfo(start_timestamp, end_timestamp, name_part))

    # Return result
    return rv


@dataclass
class PreviousChapterInfo:
    timestamp: str
    """The start timestamp of this chapter."""
    name: str
    """The name of this chapter."""


def extract_chapter_from_point_style(filename: Path) -> list[ChapterInfo]:
    """
    Extract chapter info from a file with chapter style of time point.

    In files with this style, each line should be like `00:00:00 name`.
    And the end timestamp of each chapter is the start timestamp of next chapter.

    :param filename: The path to input file.
    """
    # Prepare return value and Regex for matching
    rv: list[ChapterInfo] = []
    TIMESTAMP_PATTERN: re.Pattern = re.compile("[0-9:]+")

    # Open file and start to process.
    previous_chapter: PreviousChapterInfo | None = None
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            # Remove blank line
            line = line.strip()
            if line == "": continue

            # Match timestamp part
            matched_timestamp = TIMESTAMP_PATTERN.match(line)
            if matched_timestamp is None:
                logging.warning(f'Non-blank line found, but not match timestamp pattern: {line}')
                continue
            # Extract timestamp info
            timestamp_part: str = matched_timestamp.group()

            # Remove timestamp part from line to get
            match_start, match_end = matched_timestamp.span()
            name_part = line[:match_start] + line[match_end:]
            # Strip all blanks
            name_part = name_part.strip()
            if len(name_part) == 0:
                logging.warning(f'Blank name part is not allowed: {line}')

            # Push previous chapter according this chapter if possible
            if previous_chapter is not None:
                rv.append(ChapterInfo(previous_chapter.timestamp, timestamp_part, previous_chapter.name))

            # Push current chapter as previous chapter
            previous_chapter = PreviousChapterInfo(timestamp_part, name_part)
            
    # If there is a previous chapter stored, process it
    if previous_chapter is not None:
        rv.append(ChapterInfo(previous_chapter.timestamp, None, previous_chapter.name))
        previous_chapter = None

    # Return result
    return rv


def extract_chapter(filename: Path, style: ChapterStyle) -> list[ChapterInfo]:
    match style:
        case ChapterStyle.TIME_RANGE:
            return extract_chapter_from_range_style(filename)
        case ChapterStyle.TIME_POINT:
            return extract_chapter_from_point_style(filename)


# endregion

# region: Render

def render_ffmpeg_cmd(chapters: tuple[ChapterInfo, ...]) -> None:
    print('===== FFMPEG Commands =====')
    for chapter in chapters:
        sb: str = "ffmpeg -i audio.m4s "
        if chapter.start_timestamp is not None:
            sb += f'-ss {chapter.start_timestamp} '
        if chapter.end_timestamp is not None:
            sb += f'-to {chapter.end_timestamp} '
        sb += f'-vn "{chapter.name}.m4a"'
        print(sb)

# endregion

# region: Command Line Options

@dataclass
class Options:
    """The class representing accepted command line options."""

    input_file: Path
    """The path to input file."""
    style: ChapterStyle
    """The style of input chapter file."""


def parse() -> Options:
    parser = argparse.ArgumentParser(
        prog="Bilibili Chapter Cutter",
        description="Generate FFMPEG command for cutting chapter one by one from Bilibili audio.",
    )

    parser.add_argument(
        "-i", "--input", required=True, action="store", dest="input",
        help="The path to input file."
    )
    parser.add_argument(
        "-s", "--style", required=True, action="store", dest="style",
        help='''
        The style of input chapter file.
        The valid value is "range" for time range style, or "point" for time point style.
        '''
    )

    args = parser.parse_args()
    return Options(Path(args.input), ChapterStyle(args.style))

# endregion

def main() -> None:
    # parse cli options
    cli = parse()

    # fetch all chapters
    chapters = tuple(extract_chapter(cli.input_file, cli.style))

    # show result in console
    print('===== Found Chapters =====')
    rows: list[list[str]] = []
    headers = ['Start Timestamp', 'End Timestamp', 'Name']
    for chapter in chapters:
        row: list[str] = []
        row.append('<START>' if chapter.start_timestamp is None else chapter.start_timestamp)
        row.append('<END>' if chapter.end_timestamp is None else chapter.end_timestamp)
        row.append(chapter.name)
        rows.append(row)
    print(tabulate(rows, headers=headers, showindex=True))
    print('')

    # render result
    render_ffmpeg_cmd(chapters)


if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)
    main()
