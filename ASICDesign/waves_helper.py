import struct
import os

DBL_EPSILON = 2.2204460492503131e-016

class HspiceColumnType:
    TIME = 0
    FREQUENCY = 1
    VOLTAGE = 2
    CURRENT = 3
    UNKNOW = 4

class HspiceColumn:
    
    def __init__(self, ctype, name):
        self.type = ctype
        self.name = name
        self.data = []

class HspiceData:
    def __init__(self):
        self.columns = []
        self.columns_count = 0
        self.rows_count = 0
        self.search_dict = {}

    def read_column(self, ascii_header):
        col = column_splitter(ascii_header[256:])
        col_len = len(col)

        if col_len % 2 != 1 or col[-1] != "$&%#":
            raise Exception("Column check error")

        col = col[:-1]
        col_len = int((col_len - 1) / 2)
        col_type = col[:col_len]
        col_name = col[col_len:]

        for i in range(col_len):
            ctype = col_type[i]
            if i == 0:
                if ctype == 1:
                    ctype = HspiceColumnType.TIME
                elif ctype == 2:
                    ctype = HspiceColumnType.FREQUENCY
                elif ctype == 3:
                    ctype = HspiceColumnType.VOLTAGE
                else:
                    ctype = HspiceColumnType.UNKNOW
            else:
                if ctype == 1 or ctype == 2:
                    ctype = HspiceColumnType.VOLTAGE
                elif ctype == 8 or ctype == 15:
                    ctype = HspiceColumnType.CURRENT
                else:
                    ctype = HspiceColumnType.UNKNOW

            self.columns.append(HspiceColumn(ctype, col_name[i]))

        self.build_search_sheet()

    def build_search_sheet(self):
        for i in self.columns:
            self.search_dict[i.name] = i

    def pick_column(self, name):
        return self.search_dict[name].data

    def start_push_data(self):
        self.push_col = 0
        self.rows_count = 0
        self.columns_count = len(self.columns)

    def push_data(self, data):
        self.columns[self.push_col].data.append(data)

        self.push_col += 1
        if self.push_col == self.columns_count:
            self.push_col = 0
            self.rows_count += 1

    def end_push_data(self):
        if self.push_col != 0:
            raise Exception("Unfullfilled sheet!")

def convert_hspice_waves(file_path):

    result = HspiceData()

    with open(file_path, 'rb') as fs:
        four_header = read_int(fs, 4)
        if (four_header[0] != 4 or four_header[2] != 4):
            raise Exception("File header check error")

        header_len = four_header[3]
        header = read_string(fs, header_len)
        header_len_confirm = read_int(fs)
        if (header_len != header_len_confirm):
            raise Exception("ASCII header check error")
        result.read_column(header)

        is_over = False
        result.start_push_data()
        while not is_over:
            four_header = read_int(fs, 4)
            if (four_header[0] != 4 or four_header[2] != 4):
                raise Exception("Body header check error")
            body_len = four_header[3]

            for i in range(int(body_len / 4)):
                if peek_float(fs) >= 1e30 - DBL_EPSILON:
                    read_float(fs)
                    is_over = True
                
                if not is_over:
                    result.push_data(read_float(fs))

            body_len_confirm = read_int(fs)
            if (body_len != body_len_confirm):
                raise Exception("Body header re-check error")

        result.end_push_data()

    print("Parsing Hspice file {} done".format(file_path))
    return result

    '''
    with open(csv_path, 'w') as fs:
        fmt = ','.join(["{:.5e}"] * result.columns_count)
        data = [0.0] * result.columns_count

        for i in range(result.rows_count):
            for j in range(result.columns_count):
                data[j] = result.columns[j].data[i]

            fs.write(fmt.format(*data))
            fs.write("\n")
    '''

def column_splitter(strl):
    result = []
    cache = ""

    # 0: waiting for valid str
    # 1: inputing str
    status = 0

    for c in strl:
        if c == ' ' or c == '\t' or c == '\n':
            if status == 0:
                continue
            elif status == 1:
                # stop appending and push into list
                result.append(cache)
                status = 0
        else:
            if status == 0:
                # entering recording mode
                cache = c
                status = 1
            elif status == 1:
                cache += c

    if status == 1:
        # pushing last str
        result.append(cache)

    return result

def peek_float(fs):
    f = read_float(fs)
    fs.seek(-4, os.SEEK_CUR)
    return f

def read_int(fs, count = 1):
    if (count != 1):
        return struct.unpack("i" * count, fs.read(4 * count))
    else:
        return struct.unpack("i", fs.read(4))[0]

def read_float(fs, count = 1):
    if (count != 1):
        return struct.unpack("f" * count, fs.read(4 * count))
    else:
        return struct.unpack("f", fs.read(4))[0]

def read_string(fs, count):
    return fs.read(count).decode("ascii")