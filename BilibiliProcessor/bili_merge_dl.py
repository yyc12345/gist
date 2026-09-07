import json
import argparse
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Iterator, ClassVar, Any
from tabulate import tabulate
from bili_common import safe_wrap_cmd_path, sanitize_name

# region: Video Enumeration

class DownloadDirectory:
    """
    The class representing the download directory of Bilibili
    which contains various downloaded videos.
    """

    __dir_path: Path
    """The path to this directory."""

    def __init__(self, dir_path: Path):
        self.__dir_path = dir_path

    def get_path(self) -> Path:
        """Get the path of this directory."""
        return self.__dir_path

    def enumerate_video(self) -> Iterator['VideoDirectory']:
        # prepare regex pattern for checking dir name
        dir_name_pattern: re.Pattern = re.compile('^[sc_0-9]+$')
        # iterate directory
        for entry in self.get_path().iterdir():
            # if it is dir and its name fit our requirement
            if not entry.is_dir(): continue
            if dir_name_pattern.match(entry.name) is None: continue
            # we return it
            yield VideoDirectory(self, entry.name)

class VideoDirectory:
    
    __download_dir: DownloadDirectory
    """The reference to the download directory."""
    __video_dir_name: str
    """The name of this video directory."""
    __episode_count: Optional[int]
    """
    The count of episode in this video.
    
    This field has cache feature. If it is None, we need compute it first,
    otherwise directly read it.
    """

    def __init__(self, download_dir: DownloadDirectory, video_dir_name: str):
        self.__download_dir = download_dir
        self.__video_dir_name = video_dir_name
        self.__episode_count = None

    def get_path(self) -> Path:
        """Get the path of this directory."""
        return self.__download_dir.get_path() / self.__video_dir_name

    def get_video_dir_name(self) -> str:
        """Get the name of this video directory."""
        return self.__video_dir_name

    def enumerate_episode(self) -> Iterator['EpisodeDirectory']:
        # enumerate all subdir located in this dir
        for entry in self.get_path().iterdir():
            # if it is dir, we return it
            if not entry.is_dir(): continue
            yield EpisodeDirectory(self, entry.name)

    def get_episode_count(self) -> int:
        """Get the number of episode in this video."""
        # If there is no cache, we compute it.
        if self.__episode_count is None:
            # We use map to convert all return value from iterator to a simple bool
            # to reduce the memory usage.
            self.__episode_count = len(list(map(lambda x: True, self.enumerate_episode())))
        return self.__episode_count

    def has_single_episode(self) -> bool:
        """Get whether this video only have one episode."""
        return self.get_episode_count() == 1

class EpisodeDirectory:
    
    __video_dir: VideoDirectory
    """The reference to the video directory."""
    __episode_dir_name: str
    """The name of this episode directory."""

    def __init__(self, video_dir: VideoDirectory, episode_dir_name: str):
        self.__video_dir = video_dir
        self.__episode_dir_name = episode_dir_name

    def get_path(self) -> Path:
        """Get the path of this directory."""
        return self.__video_dir.get_path() / self.__episode_dir_name

    def get_episode_dir_name(self) -> str:
        """Get the name of this episode directory."""
        return self.__episode_dir_name

    def build_episode(self) -> 'Episode':
        return Episode(EpisodeProperties(
            episode_dir = self.get_path(),
            single_part = self.__video_dir.has_single_episode(),
            episode_dir_name = self.get_episode_dir_name(),
            video_dir_name = self.__video_dir.get_video_dir_name()
        ))

# endregion

# region: Video Descriptor

@dataclass
class EpisodeProperties:
    """The properties for building a complete episode."""
    
    episode_dir: Path
    """The path to the directory which storing video and audio."""
    single_part: bool
    """Whether this episode is the only episode of its parent directory."""

    episode_dir_name: str
    """The name of this episode directory."""
    video_dir_name: str
    """The name of this video directory."""

class Episode():
    """The class representing a complete episode."""

    __properties: EpisodeProperties
    """The properties of this video delivered by enumerator."""
    __danmaku_file: Optional[Path]
    """The path to the danmaku file. None if there is no danmaku file."""
    __entry_json_file: Path
    """The path to the entry json file."""
    __video_file: Path
    """The path to the video file."""
    __audio_file: Path
    """The path to the audio file."""
    __is_valid: bool
    """Whether this video is valid."""

    __download_quality: int
    """The download quality of this episode."""
    __height: int
    """The height of this episode."""
    __width: int
    """The width of this episode."""
    __video_title: str
    """The title of this video."""
    __episode_title: str
    """The title of this episode."""

    def __init__(self, properties: EpisodeProperties):
        # set to invalid first
        self.__is_valid = False
        # set delivered properties
        self.__properties = properties
        # initialize each parts and check failure
        self.__init_danmaku_file()
        if not self.__init_entry_json_file(): return
        if not self.__init_video_audio_files(): return
        # everything is okey. set to valid
        self.__is_valid = True

    def __init_danmaku_file(self) -> None:
        # YYC MARK: Danmaku is optional if there is no danmaku.
        danmaku_file = self.__properties.episode_dir / 'danmaku.xml'
        if danmaku_file.is_file():
            self.__danmaku_file = danmaku_file
        else:
            self.__danmaku_file = None

    def __init_entry_json_file(self) -> bool:
        # init path first
        self.__entry_json_file = self.__properties.episode_dir / 'entry.json'
        if not self.__entry_json_file.is_file(): return False
        # try to read json data
        try:
            with open(self.__entry_json_file, 'r', encoding='utf-8') as f:
                data: dict[str, Any] = json.load(f)
                # get quality for locating video and audio file
                self.__download_quality = data['video_quality']
                # get video title
                video_title: str = data['title']
                self.__video_title = sanitize_name(video_title)

                # get part data
                part_data = self.__get_part_data(data)
                # get width and height for danmaku output
                self.__width = part_data['width']
                self.__height = part_data['height']
                # get episode title
                episode_title = self.__get_part_title(part_data)
                self.__episode_title = sanitize_name(episode_title)

        # YYC MARK: Comment for developer checking exception
        except:
            return False
        # except Exception as ex:
        #     print(ex.__repr__())
        
        return True

    def __init_video_audio_files(self) -> bool:
        # init path and check them
        self.__video_file = self.__properties.episode_dir / str(self.__download_quality) / 'video.m4s'
        self.__audio_file = self.__properties.episode_dir / str(self.__download_quality) / 'audio.m4s'
        if not self.__video_file.is_file(): return False
        if not self.__audio_file.is_file(): return False
        return True

    def __get_part_data(self, d: dict[str, Any]) -> dict[str, Any]:
        # Normal video and bangumi have different part data field name.
        # We need process them respectively.

        # Preapre return value
        ret: dict[str, Any] | None
        # Test normal video key
        ret = d.get('page_data', None)
        if ret is not None: return ret
        # Test bangumi key
        ret = d.get('ep', None)
        if ret is not None: return ret
        # Error
        raise Exception("Can not find video part data.")

    def __get_part_title(self, d: dict[str, Any]) -> str:
        # Same like part data, we need find it respectively

        # Prepare return value
        ret: str | None
        # Test normal video
        ret = d.get('part', None)
        if ret is not None: return ret
        # Test bangumi key
        ret = d.get('index_title', None)
        if ret is not None: return ret
        # Error
        raise Exception("Can not find video part title.")

    def is_valid(self) -> bool:
        """Check whether this video is valid."""
        return self.__is_valid
    def get_path(self) -> Path:
        """Get the root directory path of this video."""
        return self.__properties.episode_dir
    def has_danmaku_file(self) -> bool:
        """Check whether this video has danmaku file."""
        return self.__danmaku_file is not None
    def get_danmaku_file(self) -> Path:
        """Get the path to the danmaku file."""
        if self.__danmaku_file is None: raise RuntimeError("there is no danmaku file")
        else: return self.__danmaku_file
    def get_height(self) -> int:
        return self.__height
    def get_width(self) -> int:
        """Get the width of this episode."""
        return self.__width
    def get_id_prefix(self) -> str:
        """Get the id prefix of this episode if user enabled it."""
        # if it is the only episode, we use video id,
        # otherwise we output the combination of video and episode id.
        if self.__properties.single_part: return self.__properties.video_dir_name
        else: return f'{self.__properties.video_dir_name}-{self.__properties.episode_dir_name}'
    def get_title(self) -> str:
        """Get the title of this episode."""
        # choose main title if it is single part, otherwise part title
        if self.__properties.single_part: return self.__video_title
        else: return self.__episode_title
    def build_filename_title(self, id_prefix: bool) -> str:
        """Build final output filename used title."""
        if id_prefix: return f'{self.get_id_prefix()}-{self.get_title()}'
        else: return self.get_title()
    def get_video_file(self) -> Path:
        """Get the path to the video file."""
        return self.__video_file
    def get_audio_file(self) -> Path:
        """Get the path to the audio file."""
        return self.__audio_file

# endregion

# region: Render

class Render:
    """The class render how we manipulate downloaded files"""

    __episodes: tuple[Episode, ...]
    """All videos to be rendered"""
    __out_dir: Path
    """The output directory of rendered videos"""
    __id_prefix: bool
    """Whether to add index prefix to video title"""

    def __init__(self, episodes: tuple[Episode, ...], out_dir: Path, id_prefix: bool):
        self.__episodes = episodes
        self.__out_dir = out_dir
        self.__id_prefix = id_prefix

    def __build_episode_title(self, episode: Episode) -> str:
        return episode.build_filename_title(self.__id_prefix)

    def generate_ffmpeg_cmd(self) -> None:
        print('===== FFMPEG Commands =====')
        for episode in self.__episodes:
            input_video: str = safe_wrap_cmd_path(episode.get_video_file())
            input_audio: str = safe_wrap_cmd_path(episode.get_audio_file())
            output_av: str = safe_wrap_cmd_path(self.__out_dir / f'{self.__build_episode_title(episode)}.mp4')
            print(f'ffmpeg -loglevel warning -hide_banner -i {input_audio} -i {input_video} -c:v copy -c:a copy {output_av}')
        print('')

    def generate_audio_only_win_copy(self) -> None:
        print('===== Audio-only Windows COPY Commands =====')
        for episode in self.__episodes:
            input_audio: str = safe_wrap_cmd_path(episode.get_audio_file())
            output_a: str = safe_wrap_cmd_path(self.__out_dir / f'{self.__build_episode_title(episode)}.aac')
            print(f'COPY /Y {input_audio} {output_a}')
        print('')

    def generate_audio_only_linux_cp(self) -> None:
        print('===== Audio-only Linux CP Commands =====')
        for episode in self.__episodes:
            input_audio: str = safe_wrap_cmd_path(episode.get_audio_file())
            output_a: str = safe_wrap_cmd_path(self.__out_dir / f'{self.__build_episode_title(episode)}.aac')
            print(f'cp -f {input_audio} {output_a}')
        print('')

    def generate_subtitle_cmd(self) -> None:
        print('===== Subtitle Commands =====')
        for episode in self.__episodes:
            input_json: str = safe_wrap_cmd_path(Path(f'{episode.get_title()}.json'))
            output_srt: str = safe_wrap_cmd_path(self.__out_dir / f'{self.__build_episode_title(episode)}.srt')
            print(f'py bili_srt_conv.py -i {input_json} -o {output_srt}')
        print('')

    def generate_danmaku_cmd(self) -> None:
        print('===== Danmaku Commands =====')
        print('See https://github.com/hihkm/DanmakuFactory for more infomation.')
        for episode in filter(lambda i: i.has_danmaku_file(), self.__episodes):
            x: str = str(episode.get_width())
            y: str = str(episode.get_height())
            input_xml: str = safe_wrap_cmd_path(episode.get_danmaku_file())
            output_ass: str = safe_wrap_cmd_path(self.__out_dir / f'{self.__build_episode_title(episode)}.ass')
            print(f'DanmakuFactory -o ass {output_ass} -i xml {input_xml} -x {x} -y {y} --fontsize 38 --fontname "Source Han Sans"')
        print('')


# endregion

# region: Command Line Options

@dataclass
class Options:
    """The class representing accepted command line options."""

    input_dir: Path
    """The path to input directory."""
    output_dir: Path
    """The path to output directory."""
    id_prefix: bool
    """Whether adding ID prefix at the head of output file."""

def parse() -> Options:
    # Prepare arg parser and do parse
    parser = argparse.ArgumentParser(
        prog='Bilibili Downloaded Video Merger',
        description='Enumerate downloaded bilibili videos and generate FFMPEG script for merging downloaded videos.'
    )
    parser.add_argument(
        '-i', '--input', action='store', required=True, dest='input',
        help='''
        The path to the root of Bilibili download directory.
        It usually is /Android/data/tv.danmaku.app/download
        '''
    )
    parser.add_argument(
        '-o', '--output', action='store', required=True, dest='output',
        help='The destination directory storing video result.'
    )
    parser.add_argument(
        '--id', action='store_true', dest='id',
        help='Set it to add ID prefix at the begin of output file names to avoid possible duplicated name.'
    )

    args = parser.parse_args()
    return Options(
        Path(args.input).resolve(), Path(args.output).resolve(), bool(args.id)
    )

# endregion

def main() -> None:
    # parse cli options
    cli = parse()

    # iterate all episodes
    episodes: list[Episode] = []
    download_dir = DownloadDirectory(cli.input_dir)
    for video_dir in download_dir.enumerate_video():
        for episode_dir in video_dir.enumerate_episode():
            episodes.append(episode_dir.build_episode())
    # filter them
    valid_episodes: tuple[Episode, ...] = tuple(filter(lambda x: x.is_valid(), episodes))

    # show result in console
    print('===== Found Videos Summary =====')
    print(f'{len(episodes)} videos found. {len(valid_episodes)} videos after filter.')
    rows: list[list[str]] = []
    headers = ['Valid', 'Path', 'Title']
    for episode in episodes:
        row: list[str] = []
        row.append('True' if episode.is_valid() else 'False')
        row.append(str(episode.get_path()))
        row.append(episode.build_filename_title(cli.id_prefix) if episode.is_valid() else '')
        rows.append(row)
    print(tabulate(rows, headers=headers, showindex=True))
    print('')

    # render result
    render = Render(valid_episodes, cli.output_dir, cli.id_prefix)
    render.generate_ffmpeg_cmd()
    render.generate_audio_only_win_copy()
    render.generate_audio_only_linux_cp()
    render.generate_subtitle_cmd()
    render.generate_danmaku_cmd()

if __name__ == '__main__':
    main()
