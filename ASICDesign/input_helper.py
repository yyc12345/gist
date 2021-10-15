
class HspiceInputIterator:
    
    def __init__(self, argv):
        self.param = {}

        # check param
        # only 1 list or all static vvalue
        list_count = 0
        for k, v in argv.items():
            parsed = eval(v)
            self.param[k] = parsed

            if isinstance(parsed, list) or isinstance(parsed, tuple):
                list_count += 1

        if list_count == 1:
            self.mode = 1
            self.counter = 0
        elif list_count == 0:
            self.mode = 0
        else:
            raise Exception()

    def give(self):
        if self.mode == 0:
            print("Given data:")
            print(self.param)
            yield self.param
        elif self.mode == 1:
            rtval = {}
            list_key = None
            list_value = None

            for k, v in self.param.items():
                if isinstance(v, list) or isinstance(v, tuple):
                    list_key = k
                    list_value = v
                else:
                    rtval[k] = v
            
            for item in list_value:
                rtval[list_key] = item

                print("Given data:")
                print(rtval)

                yield rtval

