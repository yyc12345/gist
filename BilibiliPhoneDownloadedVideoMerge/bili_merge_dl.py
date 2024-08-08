import os
import json
import argparse
import re
import typing

class VideoDescriptor():
    
    cTitleTransTable: typing.ClassVar[dict] = str.maketrans({
        # File system disallowed
        '\\': '', '/': '', ':': '', '*': '', '?': '', '"': '', '<': '', '>': '', '|': ''
    })

    __mRoot: str
    __mDanmakuFile: str
    __mEntryJsonFile: str
    __mDownloadQuality: int
    __mHeight: int
    __mWidth: int
    __mTitle: str
    __mVideoFile: str
    __mAudioFile: str
    __mIsValid: bool

    def __init__(self, video_path: str):
        # set to invalid first
        self.__mIsValid = False
        # set root directory
        self.__mRoot = video_path
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
                data = json.load(f)
                # get quality for locating video and audio file
                self.__mDownloadQuality = data['video_quality']
                # get width and height for danmaku output
                self.__mWidth = data['page_data']['width']
                self.__mHeight = data['page_data']['height']
                # get video title used as final output file
                title: str = data['page_data']['part']
                self.__mTitle = title.translate(VideoDescriptor.cTitleTransTable)
        except:
            return False
        
        return True

    def __init_video_audio_files(self) -> bool:
        # init path and check them
        self.__mVideoFile = os.path.join(self.__mRoot, str(self.__mDownloadQuality), 'video.m4s')
        self.__mAudioFile = os.path.join(self.__mRoot, str(self.__mDownloadQuality), 'audio.m4s')
        if not os.path.isfile(self.__mVideoFile): return False
        if not os.path.isfile(self.__mAudioFile): return False
        return True

    def is_valid(self) -> bool: return self.__mIsValid
    def get_root(self) -> str: return self.__mRoot
    def get_danmaku_file(self) -> str: return self.__mDanmakuFile
    def get_height(self) -> int: return self.__mHeight
    def get_width(self) -> int: return self.__mWidth
    def get_title(self) -> str: return self.__mTitle
    def get_video_file(self) -> str: return self.__mVideoFile
    def get_audio_file(self) -> str: return self.__mAudioFile

def enumerate_video(src_path: str) -> tuple[str, ...]:
    # enumerate collection first
    # prepare container and regex for checking
    collection_data: list[str] = []
    dir_name_pattern: re.Pattern = re.compile('^[0-9]+$')
    # iterate source directory
    with os.scandir(src_path) as it:
        for entry in it:
            # if it is dir and its name fit our requirement
            if not entry.is_dir(): continue
            if dir_name_pattern.match(entry.name) is None: continue
            # add it
            collection_data.append(os.path.join(src_path, entry.name))

    # then enumerate video
    # prepare container
    video_data: list[str] = []
    # iterate every collection's sub directory
    for coll in collection_data:
        with os.scandir(coll) as it:
            for entry in it:
                # if it is dir, add into result
                if not entry.is_dir(): continue
                video_data.append(os.path.join(coll, entry.name))

    return tuple(video_data)

def generate_video_descriptor(video_data: tuple[str, ...]) -> tuple[VideoDescriptor, ...]:
    # create video descriptor from video directory
    video_desc: list[VideoDescriptor] = []
    for item in video_data:
        video_desc.append(VideoDescriptor(item))
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
        print(f'ffmpeg -i {input_audio} -i {input_video} -c:v copy -c:a copy {output_av}')

def generate_danmaku_cmd(video_desc: tuple[VideoDescriptor, ...], dst_path: str) -> None:
    print('===== Danmaku Commands =====')
    print('See https://github.com/hihkm/DanmakuFactory for more infomation.')
    for desc in video_desc:
        x: str = str(desc.get_width())
        y: str = str(desc.get_height())
        input_xml: str = safe_cmd_path(desc.get_danmaku_file())
        output_ass: str = safe_cmd_path(os.path.join(dst_path, desc.get_title() + '.ass'))
        print(f'DanmakuFactory -o ass {output_ass} -i xml {input_xml} -x {x} -y {y} --fontsize 38 --fontname "Source Han Sans"')

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
    video_data: tuple[str, ...] = enumerate_video(args.input)
    # generate video descriptor, filter them and output summary
    video_desc: tuple[VideoDescriptor, ...] = generate_video_descriptor(video_data)
    # output result
    generate_ffmpeg_cmd(video_desc, args.output)
    generate_danmaku_cmd(video_desc, args.output)
