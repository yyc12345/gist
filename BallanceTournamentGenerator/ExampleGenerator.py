import random as r
import datetime as d
import copy
from functools import reduce
#============================================================utilities
fs = open('result.wiki', 'w')
def fswriteline(strl):
    global fs
    fs.write(strl)
    fs.write('\n')

#=======================recorder
mapList = list(map(lambda x: '测试地图{}'.format(x), range(40)))
compactRecord = []
attachComp = []
class compact(object):
    def __init__(self, date, *participant):
        #generate user
        self.participant = participant
        #generate id
        self.id = '#{}'.format(len(compactRecord) + 1)
        #set date
        self.date = date
        #generate map
        global mapList
        r.shuffle(mapList)
        self.mapList = mapList[0]
        selMap = mapList[1:1 + r.randint(0, len(participant) * 2)]
        if selMap == []:
            self.ban='无'
        else:
            self.ban = reduce(lambda x,y:x + ', ' + y, selMap)
        self.time = generateUnrelatedSequence(len(participant))

    def winner(self):
        return self.time.index(min(self.time))

class attachCompact(object):
    def __init__(self, desc, id):
        self.desc = desc
        self.id = id
        
#=======================assistant
def is2pow(num):
    if num <= 1:
        return False
    while True:
        if num == 1:
            return True
        if num % 2 != 0:
            return False
        else:
            num/=2

def getPower(num):
    power = 1
    tester = 2
    while True:
        if tester == num:
            return power
        power+=1
        tester*=2

def findClose2Pow(num):
    tester = 2
    while True:
        if tester > num:
            return int(tester / 2)
        tester*=2


def swap(left, right):
    storage1 = left[-1]
    storage2 = right[0]
    left[1:] = left[0:-1]
    right[0:-1] = right[1:]
    left[0] = storage2
    right[-1] = storage1
    #swap to keep 0 team
    left[0],left[1] = left[1],left[0]

def generateScheduleAndMark(count):
    a = [''] * count
    b=[]
    for i in range(count):
        b.append(copy.copy(a))
    c = [0] * count
    return b,c


def generateUnrelatedSequence(count):
    res = []
    while True:
        if len(res) == count:
            break
        cache = r.randint(1000,327670)
        if (cache not in res):
            res.append(cache)
    return res

def getChrBasedA(offset):
    return chr(ord('a') + offset)

#=======================datetime
originCur = d.datetime.strptime('2020-01-01','%Y-%m-%d')
cur = d.datetime.strptime('2020-01-01','%Y-%m-%d')

def getDatetime(day):
    global cur
    now = copy.copy(cur)
    dateOffset = d.timedelta(days=day)
    rtstr = now.strftime('%Y{}%m{}%d{}-').format('年', '月', '日')
    rtstr+=(now + dateOffset).strftime('%Y{}%m{}%d{}').format('年', '月', '日')
    return rtstr

def stepDatetime(day):
    global cur
    dateOffset = d.timedelta(days=day)
    cur = cur + dateOffset

def resetDatetime():
    global cur, originCur
    cur = copy.copy(originCur)


#============================================================format generator
def oneCycleCore(schedule, mark, num, playerOffset):
    global compactRecord
    # construct list
    half = int(num / 2) if num % 2 == 0 else int(num / 2) + 1
    left = list(range(half))
    right = list(range(half,half * 2))
    if num % 2 != 0:
        right[-1] = -1
    right = list(reversed(right))

    # start circle
    round = half * 2 - 1
    for i in range(round):
        # get datetime
        compDate = getDatetime(5)
        for j in range(half):
            # skip 0 team
            if left[j] == -1 or right[j] == -1:
                continue
            # add record
            cache = compact(compDate, '菜鸟{}'.format(playerOffset + left[j]), '菜鸟{}'.format(playerOffset + right[j]))
            # set schedule
            schedule[max(right[j], left[j])][min(right[j], left[j])] = cache.id
            # add score
            if (cache.winner() == 0):
                mark[left[j]]+=1
            else:
                mark[right[j]]+=1
            # add record in list
            compactRecord.append(cache)
        # make next circle
        swap(left, right)
        # step datetime
        stepDatetime(7)

def markJudgement(mark, desc, playerOffset):
    # detect attached comp
    if (mark.count(max(mark)) != 1):
        # more than 1 winner
        compDate = getDatetime(5)
        # add record
        cache = compact(compDate, *(list(map(lambda y:'菜鸟{}'.format(y + playerOffset), filter(lambda x:mark[x] == max(mark), range(len(mark)))))))
        compactRecord.append(cache)
        # add attach record
        cache2 = attachCompact(desc, cache.id)
        attachComp.append(cache2)
        # return winner
        return playerOffset + cache.winner()
    else:
        return mark.index(max(mark)) + playerOffset

def oneCycle(num, playerOffset):
    # generate schedule
    schedule, mark = generateScheduleAndMark(num)
    oneCycleCore(schedule, mark, num, playerOffset)

    res = markJudgement(mark, '单循环加赛', playerOffset)
    resetDatetime()
    return schedule, res

def twoCycle(num, playerOffset):
    # generate schedule
    schedule, mark = generateScheduleAndMark(num)
    oneCycleCore(schedule, mark, num, playerOffset)

    # reverse schedule
    for i in range(1, num):
        for j in range(i):
            schedule[j][i] = schedule[i][j]
            schedule[i][j] = ''

    # one cycle again
    oneCycleCore(schedule, mark, num, playerOffset)

    res = markJudgement(mark, '双循环加赛',playerOffset)
    resetDatetime()
    return schedule, res

def kickOff(players):
    round = getPower(len(players))
    res = [players]
    rank = []
    ecache = []
    rcache = []
    for i in range(round):
        compDate = getDatetime(5)
        # filter compact
        left = res[len(res) - 1][0::2]
        right = res[len(res) - 1][1::2]
        for j in range(int(len(res[len(res) - 1]) / 2)):
            cache = compact(compDate, left[j], right[j])
            compactRecord.append(cache)
            if cache.winner() == 0:
                ecache.append(left[j])
            else:
                ecache.append(right[j])
            #record id
            rcache.append(cache.id)
        # step date
        stepDatetime(7)
        # push data
        res.append(copy.copy(ecache))
        ecache = []
        rank.append(copy.copy(rcache))
        rcache = []

    # make 3rd competition
    if len(res) > 2:
        cache = list(filter(lambda x:x not in res[-2], res[-3]))
        # back to final. sync run
        stepDatetime(-7)
        compDate = getDatetime(5)
        newComp = compact(compDate, *(cache))
        compactRecord.append(newComp)
        cache2 = attachCompact("第三名决出赛", newComp.id)
        attachComp.append(cache2)

    return res, rank

#============================================================output
def writeCycle(args, playerOffset):
    count = len(args)
    #header
    fswriteline('{| class="wikitable"')
    fswriteline('|-')
    fswriteline('! scope="col"| ')
    for j in range(count):
        fswriteline('! scope="col"| 菜鸟{}'.format(playerOffset + j))
    #body
    for i in range(count):
        fswriteline('|-')
        fswriteline('! scope="row"| 菜鸟{}'.format(playerOffset + i))
        for j in range(count):
            if args[i][j] == '':
                fswriteline('| -')
            else:
                fswriteline('| 比赛场次：<nowiki>{}</nowiki>'.format(args[i][j]))

    #foot
    fswriteline('|}')

def writeAddition():
    fswriteline('{| class="wikitable"')
    fswriteline('|-')
    fswriteline('! 比赛加赛原因 !! 加赛ID')
    for i in attachComp:
        fswriteline('|-')
        fswriteline('| {} || <nowiki>{}</nowiki> '.format(i.desc, i.id))
    if(len(attachComp)==0):
        fswriteline('|-')
        fswriteline('| - || - ')
    fswriteline('|}')

def writeKickoff(data, rank):
    round = len(data) - 1
    count = 2 ** round
    fswriteline("{{{{{}TeamBracketCompact".format(count))
    for i in range(round):
        fswriteline('|head-{}=淘汰赛第{}轮'.format(getChrBasedA(round - 1 - i), i + 1))
    for i in range(round):
        symbol = getChrBasedA(round - 1 - i)
        for j in range(len(data[i])):
            fswriteline('|{}{}{}={}'.format(symbol,
                                            int(j / 2) + 1,
                                            'r' if j % 2 == 0 else 'b',
                                            data[i][j]))
        for j in range(len(rank[i])):
            fswriteline('|{}{}={}'.format(symbol, j + 1, rank[i][j]))
    fswriteline('}}')

def writeRecorder():
    fswriteline('{| class="wikitable"')
    fswriteline('|-')
    fswriteline('! ID !! style="min-width: 4em" | 比赛人员 !! 各自成绩 !! style="min-width: 4em" | 胜者 !! style="min-width: 6em" | 比赛地图 !! style="min-width: 6em" | Ban图 !! 当前状态 !! style="min-width: 6em" | 比赛时间')
    for i in compactRecord:
        fswriteline('|-')
        fswriteline("| <nowiki>{}</nowiki> || {} || {} || {} || {} || {} || {} || {} ".format(i.id,
                                                                                        reduce(lambda x,y: x + ', ' + y, i.participant),
                                                                                        reduce(lambda x,y: x + ', ' + y, map(lambda x: '{}:{:0>2d}.{:0>3d}'.format(int(x / 1000 / 60), int((x % 1000) / 60), x % 1000), i.time)),
                                                                                        i.participant[i.winner()],
                                                                                        i.mapList,
                                                                                        i.ban,
                                                                                        '已结束',
                                                                                        i.date))
    fswriteline('|}')


#============================================================main
people = eval(input('Input people count: '))

if people < 4:
    schedule, sel = twoCycle(people, 0)
    fswriteline('== 双循环赛赛程 ==')
    writeCycle(schedule, 0)
elif people < 8:
    schedule, sel = oneCycle(people, 0)
    fswriteline('== 单循环赛赛程 ==')
    writeCycle(schedule, 0)
elif is2pow(people):
    generatedPeople = list(map(lambda x:'菜鸟{}'.format(x), range(people)))
    res, rank = kickOff(generatedPeople)
    fswriteline('== 淘汰赛赛程 ==')
    writeKickoff(res, rank)
else:
    # grouping
    groups = findClose2Pow(int(people / 4))
    realDistribute = [0] * groups
    index = 0
    for i in range(people):
        if index == groups:
            index = 0
        realDistribute[index]+=1
        index+=1
    # do each 1 cycle
    fswriteline('== 单循环赛赛程 ==')
    selPeople = []
    for i in range(groups):
        offset = sum(realDistribute[0:i])
        schedule, sel = oneCycle(realDistribute[i], offset)
        selPeople.append(sel)
        writeCycle(schedule, offset)

    # process sel people
    selPeople = list(map(lambda x:'菜鸟{}'.format(x), selPeople))
    # calc datetime and set datetime
    ccache = max(realDistribute)
    for i in range(ccache + 1 if groups % 2 != 0 else ccache):
        stepDatetime(7)
    if (len(attachComp) != 0):
        stepDatetime(7)

    fswriteline('== 淘汰赛赛程 ==')
    res, rank = kickOff(selPeople)
    writeKickoff(res, rank)


fswriteline('== 加赛赛程 ==')
writeAddition()

fswriteline('== 比赛记录 ==')
writeRecorder()

fs.close()