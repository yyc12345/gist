import argparse
import subprocess

def encoding_audio(src_filename: str, dst_filename: str) -> None:
    # calling ffmpeg to do convertion
    # ffmpeg
    #   -i infile
    #   -ar rate       set audio sampling rate (in Hz)
    #   -ac channels   set number of audio channels
    #   -f fmt         force format
    #   -c codec       codec name
    #   -y             overwrite output files
    proc_ffmpeg = subprocess.run(
        [
            'ffmpeg',
            '-v', '0',
            '-i', src_filename,
            '-ac', '1',
            '-ar', '11025',
            '-f', 's16le',
            '-c:a', 'pcm_s16le',
            '-y',
            dst_filename
        ],
        encoding='utf-8', errors='ignore',
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    proc_ffmpeg.check_returncode()
    print(proc_ffmpeg.stdout)

def patch_mmv(filename: str) -> None:
    # write MMV magic header at the beginning of dest file.
    with open(filename, 'rb+') as fs:
        raw_data = fs.read()
        fs.seek(0)
        fs.write(b'\x55\xaa\x00\x00')
        fs.write(raw_data)

if __name__ == '__main__':
    # Prepare arg parser and do parse
    parser = argparse.ArgumentParser(
        prog='Audio to MMV',
        description='Convert any audio files into MMSSTV specific MMV format.'
    )
    parser.add_argument(
        '-i', '--input', action='store', required=True, dest='input',
        help='The path to source audio file.'
    )
    parser.add_argument(
        '-o', '--output', action='store', required=True, dest='output',
        help='The path to destination MMV file .'
    )
    args = parser.parse_args()

    # do convertion
    encoding_audio(args.input, args.output)
    patch_mmv(args.output)
    print('Convertion Done.')

