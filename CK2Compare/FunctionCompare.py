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

fCK2Cmp=open('CK2Cmp.txt', 'w', encoding='utf-8')
fVxMathCmp=open('VxMathCmp.txt', 'w', encoding='utf-8')

print("Testing no matched CK2")
counter=0
keep=0
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
        fCK2Cmp.write('modify\n')
        fCK2Cmp.write(cache)
        fCK2Cmp.write('\n')
        fCK2Cmp.write(demangled.strip())
        fCK2Cmp.write('\n?SetDescription@CKObjectDeclaration@@QAEXPAD@Z\n')
    else:
        fCK2Cmp.write('keep\n')
        fCK2Cmp.write(cache)
        fCK2Cmp.write('\n')
        keep+=1
    counter+=1
print("Keep: {} Modify: {}".format(keep, counter-keep))

print("Testing no matched VxMath")
counter=0
keep=0
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
        fVxMathCmp.write('modify\n')
        fVxMathCmp.write(cache)
        fVxMathCmp.write('\n')
        fVxMathCmp.write(demangled.strip())
        fVxMathCmp.write('\n??0XString@@QAE@H@Z\n')
    else:
        fVxMathCmp.write('keep\n')
        fVxMathCmp.write(cache)
        fVxMathCmp.write('\n')
        keep+=1
    counter+=1
print("Keep: {} Modify: {}".format(keep, counter-keep))

fCK2Test.close()
fCK2TestDemangled.close()
fVxMathTest.close()
fVxMathTestDemangled.close()

fCK2Cmp.close()
fVxMathCmp.close()