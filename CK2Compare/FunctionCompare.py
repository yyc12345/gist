import sys
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

class DefineItem(object):
    def __init__(self):
        self.decoratedName = ""
        self.belongto=""
        self.mode=""
        self.demangledName = ""


# read custom document
finalDocument = sys.argv[1]
neededDocument = int(sys.argv[2])
resultCK2Dict = {}
resultVxMathDict = {}

def analyseFile(decoratedFile, demangledFile, matchDict, resultDict, belongtodll):
    fDec = open(decoratedFile, 'r', encoding='utf-8')
    fDem = open(demangledFile, 'r', encoding='utf-8')

    while True:
        dec=fDec.readline()
        dem=fDem.readline()
        if dec == '':
            break

        dec=dec.strip()
        dem=dem.strip()
        tryGetValue = resultDict.get(dec, None)
        if tryGetValue is not None:
            # exist
            continue

        tryGetValue = matchDict.get(dec, '')
        addedItem = DefineItem()
        addedItem.decoratedName = dec
        addedItem.demangledName = dem
        addedItem.belongto = belongtodll
        if tryGetValue == '':
            # modify
            addedItem.mode = 'modify'
        else:
            # keep
            addedItem.mode = 'keep'

        resultDict[dec] = addedItem


    fDec.close()
    fDem.close()

for i in range(neededDocument):
    analyseFile('ck2Test_'+str(i+1)+'.txt', 'deck2_'+str(i+1)+'.txt', CK2Dict, resultCK2Dict, 'ck2')
    analyseFile('vxmathTest_'+str(i+1)+'.txt', 'devxmath_'+str(i+1)+'.txt', VxMathDict, resultVxMathDict, 'vxmath')

# write final doc
allCount = 0
modifyCount = 0
fRes = open(finalDocument, 'w', encoding='utf-8')
iterList = list(x[1] for x in resultCK2Dict.items()) + list(x[1] for x in resultVxMathDict.items())
allCount = len(iterList)
for i in iterList:
    fRes.write(i.mode)
    fRes.write('\n')
    fRes.write(i.belongto)
    fRes.write('\n')
    fRes.write(i.decoratedName)
    fRes.write('\n')
    if i.mode == 'modify':
        fRes.write(i.demangledName)
        fRes.write('\n')
        fRes.write('\n')
        modifyCount+=1

fRes.close()

print("All: {} Keep: {} Modify: {}".format(allCount, allCount - modifyCount, modifyCount))