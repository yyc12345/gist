import icalendar

def DumpComponentHeader(file, component):
    fields = []
    inclusiveUnitCounter = 0
    fields += map(lambda x: x + ' - required', component.required)
    fields += map(lambda x: x + ' - singletons', component.singletons)
    for units in component.inclusive:
        fields += map(lambda x: x + ' - inclusive{}'.format(inclusiveUnitCounter), units)
        inclusiveUnitCounter += 1
    fields += ('exclusive - name', 'exclusive - data')
    fields += ('multiple', )
    file.write(','.join(fields))
    file.write('\n')

def DumpComponentData(file, component):
    data = []
    gotten_instance = None

    for item in component.required:
        gotten_instance = component.get(item)
        if gotten_instance is not None:
            data.append(AdvancedFormater(gotten_instance))
        else:
            data.append('')
    for item in component.singletons:
        gotten_instance = component.get(item)
        if gotten_instance is not None:
            data.append(AdvancedFormater(gotten_instance))
        else:
            data.append('')
    for units in component.inclusive:
        for item in units:
            gotten_instance = component.get(item)
            if gotten_instance is not None:
                data.append(AdvancedFormater(gotten_instance))
            else:
                data.append('')

    gotten_name = ""
    gotten_data = ""
    for item in component.exclusive:
        gotten_instance = component.get(item)
        if gotten_instance is not None:
            gotten_name = item
            gotten_data = AdvancedFormater(gotten_instance)
            break
    data.append(gotten_name)
    data.append(gotten_data)

    for item in component.multiple:
        gotten_instance = component.get(item)
        if gotten_instance is not None:
            data.append('- {} -'.format(item))
            data.append(AdvancedFormater(gotten_instance))
        else:
            data.append('')

    file.write(','.join(data))
    file.write('\n')

def AdvancedFormater(data):
    if isinstance(data, icalendar.prop.vDDDTypes):
        return str(data.dt)
    else:
        return str(data)

# read file
icsFile = open('test.ics', 'rb')
cal = icalendar.Calendar.from_ical(icsFile.read())
icsFile.close()

# analyse file
csvEvent = open('event.csv', 'w')
csvEventHeader = False
csvAlarm = open('alarm.csv', 'w')
csvAlarmHeader = False

eventCount = 0
alarmCount = 0
miscCount = 0
for component in cal.walk():
    if component.name == 'VEVENT':
        eventCount += 1
        if not csvEventHeader:
            DumpComponentHeader(csvEvent, component)
            csvEventHeader = True
        DumpComponentData(csvEvent, component)
    elif component.name == 'VALARM':
        alarmCount += 1
        if not csvAlarmHeader:
            DumpComponentHeader(csvAlarm, component)
            csvAlarmHeader = True
        DumpComponentData(csvAlarm, component)
    else:
        miscCount += 1
    
        
csvEvent.close()
csvAlarm.close()
print('Event count: {}\nAlarm count: {}\nMisc count: {}'.format(eventCount, alarmCount, miscCount))