import numpy as np
from PIL import Image
import os

# 地址是存贮npy文件的位置
rootdir=os.path.join('./data/npy')

# 输入想要的地点和时间
# 地点是准确搜索
# 时间是yyyymmdd_hhmmss，从左往右输入，可以输不全，会fetch出所有满足输入事件的npy文件
def fetch(loc, time):

    filelist = []

    for (dirpath,dirnames,filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.npy':
                picpath = './data/npy/' + filename
                pic_info = np.load(picpath, allow_pickle=True)
                loclength = len(loc)
                if pic_info.item().get('loc')[0:loclength] == loc:
                    timelength = len(time)
                    if pic_info.item().get('time')[0:timelength] == time:
                        img = Image.open(pic_info.item().get('path'))
                        filelist.append(picpath)
                        # print(pic_info.item().get('cnt'))
                        # print(pic_info.item().get('cr'))
                        # img.show()
    
    if not filelist:
        print('NO RESULTS FOUNG')
    
    return filelist


def getCount(loc, time):

    for (dirpath,dirnames,filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.npy':
                picpath = './data/npy/' + filename
                pic_info = np.load(picpath, allow_pickle=True)
                if pic_info.item().get('loc') == loc:
                    if pic_info.item().get('time') == time:
                        return pic_info.item().get('cnt')
    
    print('NO RESULTS FOUNG')


def getCrowdness(loc, time):

    for (dirpath,dirnames,filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.npy':
                picpath = './data/npy/' + filename
                pic_info = np.load(picpath, allow_pickle=True)
                if pic_info.item().get('loc') == loc:
                    if pic_info.item().get('time') == time:
                        return pic_info.item().get('cr')
    
    print('NO RESULTS FOUNG')
