import array

def convert_binary_to_csv(src_file: str, dst_file: str, is_rot: bool):
    buffer: array.array = array.array('f')
    with open(src_file, 'rb') as f:
        buffer.frombytes(f.read())

    if is_rot:
        generator = zip(buffer[0::5], buffer[1::5], buffer[2::5], buffer[3::5], buffer[4::5])
    else:
        generator = zip(buffer[0::4], buffer[1::4], buffer[2::4], buffer[3::4])

    with open(dst_file, 'w', encoding='utf-8') as f:
        if is_rot: f.write('time,x,y,z,w\n')
        else: f.write('time,x,y,z\n')
        for item in generator:
            f.write(','.join(map(lambda x: str(x), item)))
            f.write('\n')

if __name__ == '__main__':
    convert_binary_to_csv('stone_ball_pos.bin', 'stone_ball_pos.csv', False)
    convert_binary_to_csv('stone_ball_rot.bin', 'stone_ball_rot.csv', True)
    convert_binary_to_csv('stone_ball_scale.bin', 'stone_ball_scale.csv', False)
