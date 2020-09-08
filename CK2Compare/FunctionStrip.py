import sys
fr=open(sys.argv[1], 'r', encoding='utf-8')
fw=open(sys.argv[2], 'w', encoding='utf-8')
while True:
    cache=fr.readline()
    if cache == '':
        break
    if cache.find('?') != -1:
        cacheSp=cache.strip().split(' ')
        fw.write(cacheSp[-1])
        fw.write('\n')

fr.close()
fw.close()
