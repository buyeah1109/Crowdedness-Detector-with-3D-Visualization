import numpy as np
from PIL import Image
import os

rootdir = os.path.join('./data/npy')

def fetch(loc, floor, section):
    
    for (dirpath,dirnames,filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.npy':
                name = os.path.splitext(filename)[0]
                imput = loc + '_' + floor + '_' + section
                if imput == name:
                    picpath = './data/npy/' + filename
                    return picpath
    
    print('NO RESULTS FOUNG')


def getCount(loc, floor, section):

    for (dirpath,dirnames,filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.npy':
                name = os.path.splitext(filename)[0]
                imput = loc + '_' + floor + '_' + section
                if imput == name:
                    picpath = './data/npy/' + filename
                    pic_info = np.load(picpath, allow_pickle=True)
                    return pic_info.item().get('cnt')
    
    print('NO RESULTS FOUNG')


def getCrowdness(loc, floor, section):

    for (dirpath,dirnames,filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.npy':
                name = os.path.splitext(filename)[0]
                imput = loc + '_' + floor + '_' + section
                if imput == name:
                    picpath = './data/npy/' + filename
                    pic_info = np.load(picpath, allow_pickle=True)
                    return pic_info.item().get('cr')
    
    print('NO RESULTS FOUNG')


def fetchAll(loc, floor, section):

    filelist = []

    for (dirpath,dirnames,filenames) in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.npy':
                picpath = './data/npy/' + filename
                pic_info = np.load(picpath, allow_pickle=True)
                loclength = len(loc)
                if pic_info.item().get('loc')[0:loclength] == loc:
                    floorlength = len(floor)
                    if pic_info.item().get('floor')[0:floorlength] == floor:
                        seclength = len(section)
                        if pic_info.item().get('section')[0:seclength] == section:
                            img = Image.open(pic_info.item().get('path'))
                            filelist.append(picpath)
    
    if not filelist:
        print('NO RESULTS FOUNG')
    
    return filelist
