import struct, os

def write_int(fs,num):
    fs.write(struct.pack("I", num))

def write_3vector(fs, x, y ,z):
    fs.write(struct.pack("fff", x, y ,z))

def write_face(fs, v1, vn1, v2, vn2, v3, vn3):
    fs.write(struct.pack("IIIIII", v1, vn1, v2, vn2, v3, vn3))

v=[]
vn=[]
f=[]

for file in os.listdir("G:\\obj_export_text"):
    if not file.endswith(".obj"):
        continue

    v.clear()
    vn.clear()
    f.clear()

    filename = file.replace(".obj", ".bin")
    fr = open(file, 'r')
    fw = open(filename, 'wb')

    # read
    while True:
        cache = fr.readline()
        cache = cache.strip()
        cacheSp = cache.split(' ')
        if cacheSp[0] == 'g':
            break

        if cacheSp[0] == 'v':
            v.append((float(cacheSp[1]), float(cacheSp[3]), float(cacheSp[2])))
        elif cacheSp[0] == 'vt':
            pass    # ignore vt
        elif cacheSp[0] == 'vn':
            vn.append((float(cacheSp[1]), float(cacheSp[3]), float(cacheSp[2])))

    # write v
    write_int(fw, len(v))
    for item in v:
        write_3vector(fw, *item)
    write_int(fw, len(vn))
    for item in vn:
        write_3vector(fw, *item)

    while True:
        cache = fr.readline()
        cache = cache.strip()
        if cache == "":
            break
        cacheSp = cache.split(' ')
        if cacheSp[0] == 'f':
            cachev1 = cacheSp[1].split('/')
            cachev2 = cacheSp[2].split('/')
            cachev3 = cacheSp[3].split('/')

            f.append((int(cachev3[0]) - 1, int(cachev3[2]) - 1,
                int(cachev2[0]) - 1, int(cachev2[2]) - 1,
                int(cachev1[0]) - 1, int(cachev1[2]) - 1))

    write_int(fw, len(f))
    for item in f:
        write_face(fw, *item)

    fr.close()
    fw.close()

print("Done")
