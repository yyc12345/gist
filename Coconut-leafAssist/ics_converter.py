import icalendar
import sys
import os
import database
import json
import datetime
import dt as localdt

def AdvancedDatetTimeGet(dt, isStartDateTime):
    if isinstance(dt, datetime.datetime):
        gottenDatetime = int(dt.timestamp() / 60)
    elif isinstance(dt, datetime.date):
        gottenDatetime = int(datetime.datetime(
            dt.year,
            dt.month,
            dt.day,
            0 if isStartDateTime else 23, 
            0 if isStartDateTime else 59,
            0 if isStartDateTime else 59,
            0, tzinfo=LOCAL_TZ
        ).timestamp() / 60)
    else:
        raise Exception('Unexpected data')

    timezoneOffset = LOCAL_UTC_OFFSET
    return (gottenDatetime, timezoneOffset)

def AdvancedDateTimeAnalyser(component):
    startDatetimeRef = component.get('DTSTART').dt
    (startDatetime, timezoneOffset) = AdvancedDatetTimeGet(startDatetimeRef, True)

    if component.get('DTEND') is not None:
        (endDatetime, _) = AdvancedDatetTimeGet(startDatetimeRef, False)
    elif component.get('DURATION') is not None:
        endDurationRef = component.get('DURATION').dt
        if isinstance(endDurationRef, datetime.timedelta):
            endDatetime = startDatetime + int(endDurationRef.total_seconds() / 60)
        else:
            raise Exception('Unexpected data')
    else:
        raise Exception('Unexpected data')

    return (startDatetime, endDatetime, timezoneOffset)

def LoopRulesConverter(component):
    jsonData = component.get('RRULE')
    if jsonData is None:
        return ""

    loopRules = ""
    loopStopRules = ""
    freq = jsonData.get('FREQ')[0]
    if freq == 'MONTHLY':
        loopRules = 'MSA{}'.format(str(jsonData.get('INTERVAL')[0]))
    elif freq == 'WEEKLY':
        occupiedWeek = [False, ] * 7
        for item in jsonData.get('BYDAY'):
            occupiedWeek[WEEK_DICT[item]] = True
        loopRules = 'W{}{}'.format(
            ''.join(map(lambda x: 'T' if x else 'F', occupiedWeek)),
            str(jsonData.get('INTERVAL')[0])
        )
    elif freq == 'YEARLY':
        loopRules = 'YS{}'.format(str(jsonData.get('INTERVAL')[0]))
    else:
        raise Exception('Unexpected data')

    if jsonData.get('COUNT') is not None:
        loopStopRules = 'T{}'.format(str(jsonData.get('COUNT')[0]))
    else:
        loopStopRules = 'F'

    return loopRules + '-' + loopStopRules

# ============================ read args
icsFilePath = sys.argv[1]
if not os.path.isfile(icsFilePath):
    print('Fail to load ics file')
    sys.exit(1)

# read file
icsFile = open(icsFilePath, 'rb')
cal = icalendar.Calendar.from_ical(icsFile.read())
icsFile.close()

#  ============================ init const
utfOffset = float(input('Input this ics file\'s utc offset (time unit: hour)>'))
LOCAL_UTC_OFFSET = int(utfOffset * 60)
LOCAL_TZ = localdt.UTCTimezone(LOCAL_UTC_OFFSET)
WEEK_DICT = {
    "SU": 6, "MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5,
}

# ============================ pick database

db = database.CalendarDatabase()
db.open()
username = input('Input username >')
password = input('Input password >')
(status, error, token) = db.common_webLogin(username, password, 'Python backend', '127.0.0.1')
if not status:
    print('Fail to login.')
    sys.exit(1)
(status, error, collectionList) = db.collection_getFullOwn(token)
if not status:
    print('Database return an error')
    sys.exit(1)
print('Pick a collection to insert imported events')
counter = 0
for i in collectionList:
    print('{}\t{}'.format(counter, i[1]))
    counter += 1
pickedIndex = int(input())
collectionUuid = collectionList[pickedIndex][0]

# ============================ analyse file
eventCount = 0
allCount = 0
for component in cal.walk():
    allCount += 1
    # only import event chunk
    if component.name == 'VEVENT':
        eventCount += 1
        title = str(component.get('SUMMARY'))
        descriptionPrototype = {
            'color': '#1e90ff',
            'description': None
        }
        descriptionList = []
        if component.get('DESCRIPTION') is not None and str(component.get('DESCRIPTION')) != '':
            descriptionList.append(component.get('DESCRIPTION'))
        if component.get('LOCATION') is not None and str(component.get('LOCATION')) != '':
            descriptionList.append(component.get('LOCATION'))
        descriptionPrototype['description'] = '\n'.join(descriptionList)
        description = json.dumps(descriptionPrototype)
    
        (eventDateTimeStart, eventDateTimeEnd, timezoneOffset) = AdvancedDateTimeAnalyser(component)
        loopRules = LoopRulesConverter(component)

        (status, _, _) = db.calendar_add(
            token,
            collectionUuid,
            title,
            description,
            eventDateTimeStart,
            eventDateTimeEnd,
            loopRules,
            timezoneOffset
        )
        if not status:
            print('Database return an error')
            sys.exit(1)
        
db.common_logout(token)
db.close()
print('All chunk: {}\nEvent count: {}'.format(allCount, eventCount))