import sys
import jinja2

# ========================= helper

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

# ========================= read dict
fDict=open(sys.argv[3], 'r', encoding='utf-8')
fDictDemangled=open(sys.argv[4], 'r', encoding='utf-8')

dllDict= {}

while True:
    cache = fDict.readline()
    if cache == '':
        break
    cache = cache.strip()
    if cache == '':
        continue
    dllDict[cache] = fDictDemangled.readline().strip()

fDict.close()
fDictDemangled.close()

# ========================= process
fCmp = open(sys.argv[1], 'r', encoding='utf-8')
renderData = []
counter = 0
while True:
    cache=fCmp.readline()
    if cache == '':
        break
    cache=cache.strip()
    if cache == '':
        continue
    sectorType=cache
    if sectorType == 'keep':
        decoratedName = fCmp.readline().strip()
        demangledName = dllDict[decoratedName]
        
        (correctFunctionName, isField) = getCorrectFunctionName(demangledName, counter)

        if isField:
            renderData.append((2, correctFunctionName, demangledName))
        else:
            renderData.append((1, correctFunctionName, decoratedName, demangledName))
    else:
        decoratedName = fCmp.readline().strip()
        demangledName = fCmp.readline().strip()
        point2DecoratedName = fCmp.readline().strip()
        point2DemangledName = dllDict[point2DecoratedName]

        (correctFunctionName, isField) = getCorrectFunctionName(demangledName, counter)

        if isField:
            renderData.append((2, correctFunctionName, demangledName))
        else:
            renderData.append((0, correctFunctionName, point2DecoratedName, demangledName, point2DemangledName))

    counter+=1
        
fCmp.close()
# ========================= render

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./', encoding='utf-8', followlinks=False),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)
template = env.get_template('Template.cpp')
fResult = open(sys.argv[2], 'w', encoding='utf-8')
fResult.write(template.render(funcCount = counter,
                                renderData = renderData,
                                dllName = sys.argv[5]))
fResult.close()

