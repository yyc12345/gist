import os
import json
import argparse
import re
import typing

class PartStorage:
    __mRoot: str
    __mPartStorage: list[str]

    def __init__(self, storage_path: str):
        self.__mRoot = storage_path
        self.__mPartStorage = []

    def get_path(self) -> str:
        return self.__mRoot

    def add_to_storage(self, new_part: str) -> None:
        self.__mPartStorage.append(new_part)

    def iterate_storage(self) -> typing.Iterator[str]:
        return iter(self.__mPartStorage)

    def is_single_part(self) -> bool:
        return len(self.__mPartStorage) <= 1

class VideoStorage():
    __mRoot: str
    __mVideoStorage: list[PartStorage]

    def __init__(self, storage_path: str):
        self.__mRoot = storage_path
        self.__mVideoStorage = []

    def get_path(self) -> str:
        return self.__mRoot

    def add_to_storage(self, new_video: PartStorage) -> None:
        self.__mVideoStorage.append(new_video)

    def iterate_storage(self) -> typing.Iterator[PartStorage]:
        return iter(self.__mVideoStorage)

class VideoDescriptor():
    
    cTitleTransTable: typing.ClassVar[dict] = str.maketrans({
        # File system disallowed
        '\\': '', '/': '', ':': '', '*': '', '?': '', '"': '', '<': '', '>': '', '|': ''
    })

    __mRoot: str
    __mSinglePart: bool
    __mDanmakuFile: str
    __mEntryJsonFile: str
    __mDownloadQuality: int
    __mHeight: int
    __mWidth: int
    __mTitle: str
    __mVideoFile: str
    __mAudioFile: str
    __mIsValid: bool

    def __init__(self, video_path: str, is_single_part: bool):
        # set to invalid first
        self.__mIsValid = False
        # set root directory and whether it is single part
        self.__mRoot = video_path
        self.__mSinglePart = is_single_part
        # initialize each parts
        if not self.__init_danmaku_file(): return
        if not self.__init_entry_json_file(): return
        if not self.__init_video_audio_files(): return
        # set to valid
        self.__mIsValid = True

    def __init_danmaku_file(self) -> bool:
        self.__mDanmakuFile = os.path.join(self.__mRoot, 'danmaku.xml')
        return os.path.isfile(self.__mDanmakuFile)

    def __init_entry_json_file(self) -> bool:
        # init path first
        self.__mEntryJsonFile = os.path.join(self.__mRoot, 'entry.json')
        if not os.path.isfile(self.__mEntryJsonFile): return False
        # try to read json data
        try:
            with open(self.__mEntryJsonFile, 'r', encoding='utf-8') as f:
                data: dict[str, typing.Any] = json.load(f)
                # get quality for locating video and audio file
                self.__mDownloadQuality = data['video_quality']

                # get part data
                part_data = self.__get_part_data(data)

                # get width and height for danmaku output
                self.__mWidth = part_data['width']
                self.__mHeight = part_data['height']

                # get main title and part title respectively
                # choose main title if it is single part, otherwise part title
                title: str
                if self.__mSinglePart: title = data['title']
                else: title = self.__get_part_title(part_data)
                self.__mTitle = title.translate(VideoDescriptor.cTitleTransTable)

        except:
        # except Exception as ex:
        #     print(ex.__repr__())
            return False
        
        return True

    def __init_video_audio_files(self) -> bool:
        # init path and check them
        self.__mVideoFile = os.path.join(self.__mRoot, str(self.__mDownloadQuality), 'video.m4s')
        self.__mAudioFile = os.path.join(self.__mRoot, str(self.__mDownloadQuality), 'audio.m4s')
        if not os.path.isfile(self.__mVideoFile): return False
        if not os.path.isfile(self.__mAudioFile): return False
        return True

    def __get_part_data(self, d: dict[str, typing.Any]) -> dict[str, typing.Any]:
        # Normal video and bangumi have different part data field name.
        # We need process them respectively.

        # Preapre return value
        ret: dict[str, typing.Any] | None
        # Test normal video key
        ret = d.get('page_data', None)
        if ret is not None: return ret
        # Test bangumi key
        ret = d.get('ep', None)
        if ret is not None: return ret
        # Error
        raise Exception("Can not find video part data.")

    def __get_part_title(self, d: dict[str, typing.Any]) -> str:
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

    def is_valid(self) -> bool: return self.__mIsValid
    def get_root(self) -> str: return self.__mRoot
    def get_danmaku_file(self) -> str: return self.__mDanmakuFile
    def get_height(self) -> int: return self.__mHeight
    def get_width(self) -> int: return self.__mWidth
    def get_title(self) -> str: return self.__mTitle
    def get_video_file(self) -> str: return self.__mVideoFile
    def get_audio_file(self) -> str: return self.__mAudioFile

def enumerate_video(src_path: str) -> VideoStorage:
    # enumerate collection first
    # prepare container and regex for checking
    video_storage: VideoStorage = VideoStorage(src_path)
    dir_name_pattern: re.Pattern = re.compile('^[sc_0-9]+$')
    # iterate source directory
    with os.scandir(src_path) as it:
        for entry in it:
            # if it is dir and its name fit our requirement
            if not entry.is_dir(): continue
            if dir_name_pattern.match(entry.name) is None: continue
            # add it
            video_storage.add_to_storage(PartStorage(os.path.join(src_path, entry.name)))

    # then enumerate video
    # iterate every collection's sub directory
    for parts in video_storage.iterate_storage():
        with os.scandir(parts.get_path()) as it:
            for entry in it:
                # if it is dir, add into result
                if not entry.is_dir(): continue
                parts.add_to_storage(os.path.join(parts.get_path(), entry.name))

    return video_storage

def generate_video_descriptor(video_data: VideoStorage) -> tuple[VideoDescriptor, ...]:
    # create video descriptor from video directory
    video_desc: list[VideoDescriptor] = []
    for vst in video_data.iterate_storage():
        for pst in vst.iterate_storage():
            video_desc.append(VideoDescriptor(pst, vst.is_single_part()))
    # filter result
    filter_video_desc: tuple[VideoDescriptor, ...] = tuple(filter(lambda x: x.is_valid(), video_desc))

    # output result
    print('===== Found Videos Summary =====')
    print(f'{len(video_desc)} videos found. {len(filter_video_desc)} videos after filter.')
    print('Index\tValid\tPath\tTitle')
    for idx, item in enumerate(video_desc):
        if item.is_valid():
            print(f'{idx}\tTrue\t{item.get_root()}\t{item.get_title()}')
        else:
            print(f'{idx}\tFalse\t{item.get_root()}')
    print('')

    # return 
    return filter_video_desc


cCmdPathTransTable: dict = str.maketrans({
    '"': '\\"',     # escape double quote
    '\\': '\\\\'    # escape back slash
})
def safe_cmd_path(val: str) -> str:
    return f'"{val.translate(cCmdPathTransTable)}"'

def generate_ffmpeg_cmd(video_desc: tuple[VideoDescriptor, ...], dst_path: str) -> None:
    print('===== FFMPEG Commands =====')
    for desc in video_desc:
        input_video: str = safe_cmd_path(desc.get_video_file())
        input_audio: str = safe_cmd_path(desc.get_audio_file())
        output_av: str = safe_cmd_path(os.path.join(dst_path, desc.get_title() + '.mp4'))
        print(f'ffmpeg -loglevel warning -hide_banner -i {input_audio} -i {input_video} -c:v copy -c:a copy {output_av}')
    print('')

def generate_audio_only_win_copy(video_desc: tuple[VideoDescriptor, ...], dst_path: str) -> None:
    print('===== Audio-only Windows COPY Commands =====')
    for desc in video_desc:
        input_audio: str = safe_cmd_path(desc.get_audio_file())
        output_a: str = safe_cmd_path(os.path.join(dst_path, desc.get_title() + '.aac'))
        print(f'COPY /Y {input_audio} {output_a}')
    print('')

def generate_audio_only_linux_cp(video_desc: tuple[VideoDescriptor, ...], dst_path: str) -> None:
    print('===== Audio-only Linux CP Commands =====')
    for desc in video_desc:
        input_audio: str = safe_cmd_path(desc.get_audio_file())
        output_a: str = safe_cmd_path(os.path.join(dst_path, desc.get_title() + '.aac'))
        print(f'cp -f {input_audio} {output_a}')
    print('')

def generate_subtitle_cmd(video_desc: tuple[VideoDescriptor, ...], dst_path: str) -> None:
    print('===== Subtitle Commands =====')
    for desc in video_desc:
        input_json: str = safe_cmd_path(desc.get_title() + '.json')
        output_srt: str = safe_cmd_path(os.path.join(dst_path, desc.get_title() + '.srt'))
        print(f'py bili_srt_conv.py -i {input_json} -o {output_srt}')
    print('')

def generate_danmaku_cmd(video_desc: tuple[VideoDescriptor, ...], dst_path: str) -> None:
    print('===== Danmaku Commands =====')
    print('See https://github.com/hihkm/DanmakuFactory for more infomation.')
    for desc in video_desc:
        x: str = str(desc.get_width())
        y: str = str(desc.get_height())
        input_xml: str = safe_cmd_path(desc.get_danmaku_file())
        output_ass: str = safe_cmd_path(os.path.join(dst_path, desc.get_title() + '.ass'))
        print(f'DanmakuFactory -o ass {output_ass} -i xml {input_xml} -x {x} -y {y} --fontsize 38 --fontname "Source Han Sans"')
    print('')

if __name__ == '__main__':
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
    args = parser.parse_args()

    # fetch video data
    video_data: VideoStorage = enumerate_video(args.input)
    # generate video descriptor, filter them and output summary
    video_desc: tuple[VideoDescriptor, ...] = generate_video_descriptor(video_data)
    # output result
    generate_ffmpeg_cmd(video_desc, args.output)
    generate_audio_only_win_copy(video_desc, args.output)
    generate_audio_only_linux_cp(video_desc, args.output)
    generate_subtitle_cmd(video_desc, args.output)
    generate_danmaku_cmd(video_desc, args.output)
