
def get_measure_data(meas_path):
    with open(meas_path, 'r') as fs:

        # useless lines
        fs.readline()
        fs.readline()

        value = []
        while True:
            ln = fs.readline()
            if ln == '':
                break

            ln = ln.strip()
            column_splitter(value, ln)

        len_v = len(value)
        if len_v % 2 != 0:
            raise Exception("Invalid meas file")

        len_v = int(len_v / 2)
        result_dict = {}
        for i in range(len_v):
            if value[len_v + i] == 'failed':
                result_dict[value[i]] = 0
            else:
                result_dict[value[i]] = float(value[len_v + i])

        return result_dict

def column_splitter(result, strl):
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