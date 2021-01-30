import numpy as np
from PIL import Image
import os
import time

rootdir=os.path.join('./data/npy')

def fetchAll(loc, time):

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
    
    if not filelist:
        print('NO RESULTS FOUNG')
    
    return filelist


def fetch(loc, time):

    for (dirpath,dirnames,filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.npy':
                name = os.path.splitext(filename)[0]
                imput = loc + '_' + time
                if imput == name:
                    picpath = './data/npy/' + filename
                    return picpath
    
    print('NO RESULTS FOUNG')


def getCount(loc, time):

    for (dirpath,dirnames,filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.npy':
                name = os.path.splitext(filename)[0]
                imput = loc + '_' + time
                if imput == name:
                    picpath = './data/npy/' + filename
                    pic_info = np.load(picpath, allow_pickle=True)
                    return pic_info.item().get('cnt')
    
    print('NO RESULTS FOUNG')


def getCrowdness(loc, time):

    for (dirpath,dirnames,filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.npy':
                name = os.path.splitext(filename)[0]
                imput = loc + '_' + time
                if imput == name:
                    picpath = './data/npy/' + filename
                    pic_info = np.load(picpath, allow_pickle=True)
                    return pic_info.item().get('cr')
    
    print('NO RESULTS FOUNG')
