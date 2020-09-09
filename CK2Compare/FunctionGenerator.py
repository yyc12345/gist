import sys
import jinja2

# ========================= helper

'''
def getCorrectFunctionName(garbageName,fcounter):
    # clean class prefix
    garbageName=garbageName.replace('public:', '').replace('protected:', '').replace('private:', '').strip()

    # is it a field?
    isField = garbageName.find('(')
    if isField != -1:
        # function
        # split parameter and function name
        firstMarco = garbageName.index('(')
        parameterPart = garbageName[firstMarco+1:-1].strip()
        functionNamePart = garbageName[:firstMarco].strip()

        # process method
        if functionNamePart.find("__thiscall") != -1:
            # it a this call, need change
            functionNamePart=functionNamePart.replace("__thiscall", "__stdcall")
            additionalParameter = "void *"
        else:
            additionalParameter = ""
        if parameterPart == 'void':
            parameterPart = ''
        if parameterPart != '':
            if additionalParameter != '':
                parameterPart = additionalParameter + ',' + parameterPart
        else:
            parameterPart = additionalParameter

        parameterPartSp = parameterSpliter(parameterPart)
        parameterPartSpResult = []
        for ind, i in enumerate(parameterPartSp):
            i=i.strip()
            if i.startswith("class"):
                if i.endswith("*"):
                    parameterPartSpResult.append("void* val{}".format(ind))
                else:
                    parameterPartSpResult.append("{} val{}".format(i[5:], ind))
                continue
            if i.startswith("struct"):
                if i.endswith("*"):
                    parameterPartSpResult.append("void* val{}".format(ind))
                else:
                    parameterPartSpResult.append("{} val{}".format(i[6:], ind))
                continue

            if i.startswith("enum"):
                parameterPartSpResult.append("int val{}".format(ind))
                continue

            if i.find('__cdecl') != -1 or i.find('__stdcall') != -1:
                parameterPartSpResult.append("void* val{}".format(ind))
                continue

            if i=='...':
                parameterPartSpResult.append('...')

            # lost match, write it directly
            parameterPartSpResult.append("{} val{}".format(i, ind))

        perfectParameter=', '.join(parameterPartSpResult)
                
    else:
        # field
        functionNamePart = garbageName
        perfectParameter = ''

    # process name
    functionNameHeader = functionNamePart[:-(functionNamePart[::-1]).find(' ')]
    if functionNameHeader.find('__cdecl') != -1:
        functionCall = '__cdecl'
        functionNameHeader = functionNameHeader.replace('__cdecl' ,'')
    elif functionNameHeader.find('__stdcall') != -1:
        functionCall = '__stdcall'
        functionNameHeader = functionNameHeader.replace('__stdcall' ,'')
    else:
        functionCall = ''

    functionNameHeader = functionNameHeader.replace('virtual', '').strip()
    functionNewHeader = ''
    while True:
        functionClipIndex = functionNameHeader.find('class')
        if functionClipIndex != -1:
            if functionNameHeader.endswith('*'):
                functionNewHeader = functionNameHeader[:functionClipIndex] + " void*"
            else:
                functionNewHeader = functionNameHeader[:functionClipIndex] + functionNameHeader[functionClipIndex + 5:]
            break
        functionClipIndex = functionNameHeader.find('struct')
        if functionClipIndex != -1:
            if functionNameHeader.endswith('*'):
                functionNewHeader = functionNameHeader[:functionClipIndex] + " void*"
            else:
                functionNewHeader = functionNameHeader[:functionClipIndex] + functionNameHeader[functionClipIndex + 6:]
            break
        
        functionClipIndex = functionNameHeader.find('enum')
        if functionClipIndex != -1:
            functionNewHeader = functionNameHeader[:functionClipIndex] + " int"
            break

        functionClipIndex = functionNameHeader.find('__cdecl')
        if functionClipIndex != -1:
            functionNewHeader = functionNameHeader[:functionClipIndex] + " void*"
            break
        functionClipIndex = functionNameHeader.find('__stdcall')
        if functionClipIndex != -1:
            functionNewHeader = functionNameHeader[:functionClipIndex] + " void*"
            break

        # fail to match, return default
        functionNewHeader = functionNameHeader
        break

    perfectFunctionName = "func{}".format((str(fcounter)).zfill(180))
    perfectFunctionName = functionNewHeader + " " + functionCall + " " + perfectFunctionName

    return (perfectFunctionName + '(' + perfectParameter + ')', isField == -1)


def parameterSpliter(paramters):
    result = []
    cache=''
    bracketCount = 0
    for i in paramters:
        if i == '(':
            bracketCount+=1
        elif i == ')':
            bracketCount-=1
        elif i == ',':
            if bracketCount == 0:
                result.append(cache)
                cache=''
            else:
                cache+=i
        else:
            cache+=i

    if cache != '':
        result.append(cache)

    return result
'''
def generateFuncName(index):
    return "func{}".format((str(index)).zfill(180))

# ========================= read dict
# read base document
fCK2=open('CK2_ExportFunc.txt', 'r', encoding='utf-8')
fCK2Demangled=open('CK2_DemangledExportFunc.txt', 'r', encoding='utf-8')
fVxMath=open('VxMath_ExportFunc.txt', 'r', encoding='utf-8')
fVxMathDemangled=open('VxMath_DemangledExportFunc.txt', 'r', encoding='utf-8')

CK2Dict= {}
VxMathDict = {}

while True:
    cache = fCK2.readline()
    if cache == '':
        break
    cache = cache.strip()
    if cache == '':
        continue
    CK2Dict[cache] = fCK2Demangled.readline().strip()
while True:
    cache = fVxMath.readline()
    if cache == '':
        break
    cache = cache.strip()
    if cache == '':
        continue
    VxMathDict[cache] = fVxMathDemangled.readline().strip()

fCK2.close()
fCK2Demangled.close()
fVxMath.close()
fVxMathDemangled.close()

# ========================= process
fCmp = open('result.txt', 'r', encoding='utf-8')
renderData = []
cffData = []
counter=0
while True:
    cache=fCmp.readline()
    if cache == '':
        break
    cache=cache.strip()
    if cache == '':
        continue
    sectorType=cache
    moduleName = "CK2" if fCmp.readline().strip() == 'ck2' else "VxMath"
    decoratedName = fCmp.readline().strip()
    functionName = generateFuncName(counter)
    cffData.append("{{ {}, 0x00 }}".format(', '.join(map(lambda x: '0x' + ('{:x}'.format(ord(x)).upper()), decoratedName))))

    if sectorType == 'keep':
        renderData.append((2, moduleName, functionName, decoratedName, (CK2Dict if moduleName == 'CK2' else VxMathDict)[decoratedName]))
    elif sectorType == 'modify':
        targetDemangledName = fCmp.readline().strip()
        pointToDecoratedName = fCmp.readline().strip()

        pointToDemangledName = ''
        if pointToDecoratedName != '':
            pointToDemangledName = (CK2Dict if moduleName == 'CK2' else VxMathDict)[pointToDecoratedName]
        renderData.append((0, moduleName, functionName, decoratedName, targetDemangledName, pointToDecoratedName, pointToDemangledName))
    else:   # hand
        targetDemangledName = fCmp.readline().strip()
        pointToDecoratedName = fCmp.readline().strip()

        pointToDemangledName = ''
        if pointToDecoratedName != '':
            pointToDemangledName = (CK2Dict if moduleName == 'CK2' else VxMathDict)[pointToDecoratedName]
        renderData.append((1, moduleName, functionName, decoratedName, targetDemangledName, pointToDecoratedName, pointToDemangledName))
    counter+=1
        
fCmp.close()
# ========================= render

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./', encoding='utf-8', followlinks=False),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)
template = env.get_template('Template.cpp')
fResult = open('VirtoolsFsck.cpp', 'w', encoding='utf-8')
fResult.write(template.render(renderData = renderData))
fResult.close()

template = env.get_template('Template.cff')
fResult = open('VirtoolsFsckModify.cff', 'w', encoding='utf-8')
fResult.write(template.render(cffData = cffData,
                                dataLength = len(cffData) + 1))
fResult.close()