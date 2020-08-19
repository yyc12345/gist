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

fCK2Test=open('CK2Test.txt', 'r', encoding='utf-8')
fCK2TestDemangled=open('CK2TestDemangled.txt', 'r', encoding='utf-8')
fVxMathTest=open('VxMathTest.txt', 'r', encoding='utf-8')
fVxMathTestDemangled=open('VxMathTestDemangled.txt', 'r', encoding='utf-8')

print("Testing no matched CK2")
while True:
    cache=fCK2Test.readline()
    demangled=fCK2TestDemangled.readline()
    if cache == '':
        break
    cache = cache.strip()
    if cache == '':
        continue
    tryGetValue = CK2Dict.get(cache, '')
    if tryGetValue == '':
        print(cache)
        print(demangled.strip())
        print('')

print("Testing no matched VxMath")
while True:
    cache=fVxMathTest.readline()
    demangled=fVxMathTestDemangled.readline()
    if cache == '':
        break
    cache = cache.strip()
    if cache == '':
        continue
    tryGetValue = VxMathDict.get(cache, '')
    if tryGetValue == '':
        print(cache)
        print(demangled.strip())
        print('')

fCK2Test.close()
fCK2TestDemangled.close()
fVxMathTest.close()
fVxMathTestDemangled.close()