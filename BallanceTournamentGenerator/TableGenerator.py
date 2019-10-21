#==========================================================prep
templateF = open("template.html", 'w')
exampleF = open('example.wiki', 'w')

t=True
f=False

def twriteline(strl):
    global templateF
    templateF.write(strl)
    templateF.write('\r')
def ewriteline(strl):
    global exampleF
    exampleF.write(strl)
    exampleF.write('\r')

level = eval(input('Input level: '))
if level < 1 or level > 32:
    exit()

def GetBorder(top, right, bot, left):
    return '<td style="border-width: {} {} {} {};border-style: solid; border-color: black">&nbsp;</td>'.format(('1px' if top else '0'), ('1px' if right else '0'), ('1px' if bot else '0'), ('1px' if left else '0'))

def GetCellHead(index):
    return ('<td bgcolor="#f2f2f2" style="width:150px;border:1px solid #aaaaaa;">{{{{{{{}r}}}}}}</td>' + '\n' + '<td bgcolor="#f2f2f2" style="width:50px;border:1px solid #aaaaaa;text-align:center;" rowspan="2">{{{{{{{}}}}}}}</td>').format(index, index)

def GetCellBot(index):
    return '<td bgcolor="#f2f2f2" style="width:150px;border:1px solid #aaaaaa;">{{{{{{{}b}}}}}}</td>'.format(index)

def GetBlankCell():
    return '<td>&nbsp;</td>'

def GetHeader(index):
    return '<td style="border:1px solid #aaaaaa;text-align:center;" bgcolor="#f2f2f2" colspan="2"><strong>{{{{{{head-{}}}}}}}</strong></td>'.format(index)

def GetChr(offset):
    return chr(ord('a') + offset)

#==========================================================template
# head
twriteline('<table border="0" cellspacing="0">')

# contruct head
twriteline('<tr>')
for i in range(level):
    twriteline(GetHeader(GetChr((level - 1) - i)))
    if i != level - 1:
        twriteline(GetBlankCell())
        twriteline(GetBlankCell())

twriteline('</tr>')

# indert blank line
twriteline('<tr><td>&nbsp;</td></tr>')

# construct chart
remain = []
default = []
counter = []
for i in range(level):
    remain.append(2 ** i - 1)
    default.append(2 ** (i + 1) - 2)
    counter.append(1)

for i in range(2 ** level):
    twriteline('<tr>')
    count = -1
    for j in remain:
        count+=1
        if j == 0:

            #judge border. omit first col
            if count != 0:
                twriteline(GetBorder(f,f,t,t))

            # set cell head
            twriteline(GetCellHead(GetChr(level - count - 1) + str(counter[count])))

            #judge border. omit final col
            if count!=level-1:
                if counter[count]%2 != 0:
                    twriteline(GetBorder(f,f,t,f))
                else:
                    twriteline(GetBorder(f,t,t,f))
            
            remain[count] = -1
        elif j == -1:
            #judge border. omit first col
            if count != 0:
                twriteline(GetBorder(t,f,f,t))

            # set cell bottom
            twriteline(GetCellBot(GetChr(level - count - 1) + str(counter[count])))

            #judge border. omit final col
            if count!=level-1:
                if counter[count]%2 != 0:
                    twriteline(GetBorder(t,t,f,f))
                else:
                    twriteline(GetBorder(t,f,f,f))

            remain[count] = default[count]
            counter[count]+=1
        else:
            #judge border. omit first col
            if count != 0:
                if counter[count-1]%2==0:
                    twriteline(GetBorder(f,f,f,t))
                else:
                    twriteline(GetBlankCell())

            #insert blank cell
            twriteline(GetBlankCell())
            twriteline(GetBlankCell())

            #judge border. omit final col
            if count!=level-1:
                if counter[count]%2==0:
                    twriteline(GetBorder(f,t,f,f))
                else:
                    twriteline(GetBlankCell())

            remain[count]-=1


    twriteline('</tr>')


#foot
twriteline('</table>')

#==========================================================example

ewriteline('== Usage ==')
ewriteline('<pre>')
ewriteline('{{{{{}TeamBracketCompact'.format(2 ** level))

for i in range(level):
    chs=GetChr(level-i-1)
    ewriteline("|head-{}=".format(chs))

for i in range(level):
    chs=GetChr(level-i-1)
    ewriteline('')
    for j in range(2 ** (level - 1 - i)):
        ewriteline("|{}{}r=".format(chs, j + 1))
        ewriteline("|{}{}b=".format(chs, j + 1))
    ewriteline('')
    for j in range(2 ** (level - 1 - i)):
        ewriteline("|{}{}=".format(chs, j + 1))

ewriteline('}}')
ewriteline('</pre>')

#==========================================================end
templateF.close()
exampleF.close()

print('Done')