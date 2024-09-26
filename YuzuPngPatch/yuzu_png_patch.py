import argparse
import os

def patch_png_file(file: str) -> None:
    # IDK why Python need "r+b" mode to modify file.
    # If I use "w+b", it will wipe out the whole file.
    # If I use "a+b", it only write data at the tail of file, even if I setup seek().
    with open(file, 'r+b') as f:
        f.seek(0, os.SEEK_SET)
        f.write(b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a')

def patch_png_files(files: tuple[str, ...]) -> None:
    failed: int = 0
    for file in files:
        print(f'Patching "{file}"...')
        try:
            patch_png_file(file)
        except:
            failed += 1
            print('Failed!')
        else:
            print('OK!')

    print(f'Total {len(files)} files, {failed} failed.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Yuzu PNG Patcher',
        description='The patcher for Yuzusoft PNG files with bad PNG header.'
    )
    parser.add_argument(
        '-f', '--files', required=True, nargs='+', dest='files',
        help='''
        The PNG file list. It should have at least one file.
        '''
    )
    args = parser.parse_args()
    patch_png_files(args.files)
    print('Patch Done.')
