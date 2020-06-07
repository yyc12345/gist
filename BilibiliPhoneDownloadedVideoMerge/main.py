import os
import json

# ========================================global var

bad_filename_filter = str.maketrans({'|': '', '\\': '', '?': '', '*': '', '<': '', '"': '', ':': '', '>': '', '+': '', '[': '', ']': '', '/': '', '\'': ''})
cd_fixer = str.maketrans({'\\': '\\\\'})
global_prefix = "{} - "

# ========================================func

# for video and subvideo search
def getSubFolderList(path):
    result = []
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)):
            result.append(i)
    return result

def getVideoSegmentList(path):
    target = ""
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)):
            target = os.path.join(path, i)
            break

    result=0
    for j in video_seg_assist():
        if os.path.exists(os.path.join(target, j)):
            result+=1
        else:
            break
        
    return (target, result)

def video_seg_assist():
    x=0;
    while True:
        yield "{}.blv".format(x)
        x+=1

def getSubVideoTitle(path):
    f=open(os.path.join(path, "entry.json"), 'r', encoding = "utf-8")
    data = json.load(f)
    f.close()    
    try:
        result = data['ep']['index_title'].translate(bad_filename_filter)
    except:
        result = ""

    return result

# ========================================main

# command file
curPath = os.getcwd()
fbat = open(os.path.join(curPath, "merge.bat"), "w")
# expand video list
for videos in getSubFolderList(curPath):
    # expand subvideos list
    path1 = os.path.join(curPath, videos)
    subvideoIndex = 1;
    for subvideos in getSubFolderList(path1):
        path2 = os.path.join(path1, subvideos)
        (targetFolder, segCount) = getVideoSegmentList(path2)
        # create merge video list file
        fffmpeg = open(os.path.join(targetFolder, "merge.txt"), 'w', encoding = "utf-8")
        fbat.write('cd /d "{}"\n'.format(targetFolder.translate(cd_fixer)))
        for segCounter in range(segCount):
            fffmpeg.write("file {}.flv\n".format(segCounter))
            fbat.write('ren {}.blv {}.flv\n'.format(segCounter , segCounter))
        fffmpeg.close()
        fbat.write('ffmpeg -f concat -i merge.txt -c copy "../../{}.flv"\n'.format(global_prefix.format(subvideoIndex) + getSubVideoTitle(path2)))
        
        subvideoIndex += 1

    subvideoIndex = 0

fbat.close()