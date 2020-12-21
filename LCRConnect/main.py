import math
import struct
import os
import sys

OneComponentList = []
TwoComponentList = []
ThreeComponentList = []

ResultList = []

class OneComponent(object):
    Value1 = 0.0

    Value = 0.0
    def PrintCircuit(self):
        print(OutputAsHuman(self.Value1))

class TwoComponent(object):
    Value1 = 0.0
    Value2 = 0.0
    IsSeries = True

    Value = 0.0
    def PrintCircuit(self):
        print("[{}] ┬ {}".format('S' if self.IsSeries else 'P', OutputAsHuman(self.Value1)))
        print("    └ {}".format(OutputAsHuman(self.Value2)))

class ThreeComponent(object):
    Value1 = 0.0
    Value2 = 0.0
    Value3 = 0.0
    IsSeries1 = True
    IsSeries2 = True

    Value = 0.0
    def PrintCircuit(self):
        print("[{}] ┬ [{}] ┬ {}".format('S' if self.IsSeries2 else 'P', 'S' if self.IsSeries1 else 'P', OutputAsHuman(self.Value1)))
        print("    │     └ {}".format(OutputAsHuman(self.Value2)))
        print("    └ {}".format(OutputAsHuman(self.Value3)))

class ResultStruct(object):
    Subtraction = 0.0
    ComponentCount = 0
    CorrespondingClass = None

def LoadFromFile(name):
    f = open(name, 'r', encoding = 'utf-8')

    # read file to get one elements state
    while True:
        cache = f.readline()
        if cache == '':
            break

        (status, value) = InputAsHuman(cache.strip())
        if status:
            newobj = None
            newobj = OneComponent()
            newobj.Value = value
            newobj.Value1 = value
            OneComponentList.append(newobj)
    
    # construct two component list
    for i in OneComponentList:
        for j in OneComponentList:
            # series
            newobj = TwoComponent()
            newobj.Value1 = i.Value
            newobj.Value2 = j.Value
            newobj.IsSeries = True
            newobj.Value = i.Value + j.Value
            TwoComponentList.append(newobj)

            # parallel
            newobj = TwoComponent()
            newobj.Value1 = i.Value
            newobj.Value2 = j.Value
            newobj.IsSeries = False
            newobj.Value = (i.Value * j.Value) / (i.Value + j.Value)
            TwoComponentList.append(newobj)

    # construct three component list
    for i in OneComponentList:
        for j in TwoComponentList:
            # series
            newobj = ThreeComponent()
            newobj.Value1 = j.Value1
            newobj.Value2 = j.Value2
            newobj.Value3 = i.Value
            newobj.IsSeries1 = j.IsSeries
            newobj.IsSeries2 = True
            newobj.Value = j.Value + i.Value
            ThreeComponentList.append(newobj)

            # parallel
            newobj = ThreeComponent()
            newobj.Value1 = j.Value1
            newobj.Value2 = j.Value2
            newobj.Value3 = i.Value
            newobj.IsSeries1 = j.IsSeries
            newobj.IsSeries2 = False
            newobj.Value = (j.Value * i.Value) / (j.Value + i.Value)
            ThreeComponentList.append(newobj)

    f.close()
    SaveAsCache(name)

def LoadFromCache(name):
    f = open(name + '.cache', 'rb')
    counter = 0
    (counter, ) = struct.unpack("I", f.read(4))
    for i in range(counter):
        newobj = OneComponent()
        (newobj.Value1, newobj.Value) = struct.unpack("dd", f.read(2 * 8))
        OneComponentList.append(newobj)
    (counter, ) = struct.unpack("I", f.read(4))
    for i in range(counter):
        newobj = TwoComponent()
        (newobj.Value1, newobj.Value2, newobj.IsSeries, newobj.Value) = struct.unpack("ddQd", f.read(3 * 8 + 8))
        newobj.IsSeries = newobj.IsSeries == 1
        TwoComponentList.append(newobj)
    (counter, ) = struct.unpack("I", f.read(4))
    for i in range(counter):
        newobj = ThreeComponent()
        (newobj.Value1, newobj.Value2, newobj.Value3, newobj.IsSeries1, newobj.IsSeries2, newobj.Value) = struct.unpack("dddQQd", f.read(4 * 8 + 2 * 8))
        newobj.IsSeries1 = newobj.IsSeries1 == 1
        newobj.IsSeries2 = newobj.IsSeries2 == 1
        ThreeComponentList.append(newobj)

    f.close()

def SaveAsCache(name):
    # in cache, is series should follow resistor mode
    f = open(name + '.cache', 'wb')
    f.write(struct.pack("I", len(OneComponentList)))
    for i in OneComponentList:
        f.write(struct.pack("dd", i.Value1, i.Value))
    f.write(struct.pack("I", len(TwoComponentList)))
    for i in TwoComponentList:
        f.write(struct.pack("ddQd", i.Value1, i.Value2, 1 if i.IsSeries else 0, i.Value))
    f.write(struct.pack("I", len(ThreeComponentList)))
    for i in ThreeComponentList:
        f.write(struct.pack("dddQQd", i.Value1, i.Value2, i.Value3, 1 if i.IsSeries1 else 0, 1 if i.IsSeries2 else 0, i.Value))

    f.close()


def OutputAsHuman(v):
    if v / 1e-12 < 1e3:
        return "{:e} n".format(v / 1e-12)
    if v / 1e-9 < 1e3:
        return "{:.4f} p".format(v / 1e-9)
    if v / 1e-6 < 1e3:
        return "{:.4f} u".format(v / 1e-6)
    if v / 1e-3 < 1e3:
        return "{:.4f} m".format(v / 1e-3)
    if v < 1e3:
        return "{:.4f}".format(v)
    if v / 1e3 < 1e3:
        return "{:.4f} k".format(v / 1e3)
    if v / 1e6 < 1e3:
        return "{:.4f} M".format(v / 1e6)

    return "{:e}".format(v)

def InputAsHuman(strl):
    try:
        if strl.endswith('n'):
            return (True, float(strl[0:-1]) * 1e-12)
        if strl.endswith('p'):
            return (True, float(strl[0:-1]) * 1e-9)
        if strl.endswith('u'):
            return (True, float(strl[0:-1]) * 1e-6)
        if strl.endswith('m'):
            return (True, float(strl[0:-1]) * 1e-3)
        if strl.endswith('k'):
            return (True, float(strl[0:-1]) * 1e3)
        if strl.endswith('M'):
            return (True, float(strl[0:-1]) * 1e6)
        return (True, float(strl))
    except:
        return (False, 0.0)

def ValidCommandInput(valid_list):
    while True:
        cache = input()
        if cache not in valid_list:
            print('Wrong command, please input again.')
        else:
            return cache

def ValidNumberInput():
    while True:
        cache = input()
        (status, num) = InputAsHuman(cache)
        if not status:
            print('Wrong number, please input again.')
        else:
            return num

def DoQuery():
    # get config

    print('What are you connecting?')
    print('r: resistor')
    print('l: inductor')
    print('c: capacitor')
    mode = ValidCommandInput(['c', 'l', 'r'])
    is_resistor_mode = mode != 'c'

    print('Your target value?')
    target = ValidNumberInput()

    print('Your tolerance?')
    target_tolerance = ValidNumberInput()

    print('How to sort result?')
    print('l: less component')
    print('a: more accuracy')
    sort_mode = ValidCommandInput(['l', 'a'])

    # start computing
    print('Collecting and sorting data...')
    ResultList.clear()
    for i in OneComponentList:
        cache = i.Value - target
        if abs(cache) < target_tolerance:
            newobj = ResultStruct()
            newobj.Subtraction = cache
            newobj.ComponentCount = 1
            newobj.CorrespondingClass = i
            ResultList.append(newobj)
    for i in TwoComponentList:
        cache = i.Value - target
        if abs(cache) < target_tolerance:
            newobj = ResultStruct()
            newobj.Subtraction = cache
            newobj.ComponentCount = 2
            newobj.CorrespondingClass = i
            ResultList.append(newobj)
    for i in ThreeComponentList:
        cache = i.Value - target
        if abs(cache) < target_tolerance:
            newobj = ResultStruct()
            newobj.Subtraction = cache
            newobj.ComponentCount = 3
            newobj.CorrespondingClass = i
            ResultList.append(newobj)

    if sort_mode == 'l':
        ResultList.sort(key = lambda x: (x.ComponentCount, abs(x.Subtraction)))
    else:
        ResultList.sort(key = lambda x: abs(x.Subtraction))

    # display result
    if len(ResultList) == 0:
        print('Sorry, no result!')
        return

    count = len(ResultList)
    all_page = int(count / 10)
    current_page = 0
    while current_page <= all_page:
        for i in range(9):
            picked_index = current_page * 9 + i
            if (picked_index < count):
                picked_item = ResultList[picked_index]
                print("Plan {}\t{}\t{:.2%}".format(picked_index + 1, OutputAsHuman(picked_item.CorrespondingClass.Value), picked_item.Subtraction / target))
                picked_item.CorrespondingClass.PrintCircuit()
    
        print('')
        print("Page {} of {}. p: next page. q: exit".format(current_page + 1, all_page + 1))
        command = ValidCommandInput(['p', 'q'])
        if command == 'p':
            current_page += 1
        elif command == 'q':
            break

def DoHelp():
    print('LCR Connect Help:')
    print('')
    print('query: do a query immediately. following the guider and find the result.')
    print('help: print this')
    print('exit: exit this app')

# ===================================================== program start

print('LCR Connect')

# loading file
print('Input the component value list file name:')
filename = input()
if not os.path.isfile(filename + '.cache'):
    LoadFromFile(filename)
else:
    LoadFromCache(filename)

# ready for command
while True:
    sys.stdout.write('> ')
    sys.stdout.flush() 
    cmd = ValidCommandInput(['exit', 'query', 'help'])
    if cmd == 'exit':
        break
    elif cmd == 'query':
        DoQuery()
    elif cmd == 'help':
        DoHelp()