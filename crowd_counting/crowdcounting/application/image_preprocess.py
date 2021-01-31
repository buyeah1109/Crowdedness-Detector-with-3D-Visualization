import time
import numpy as np

class PreProcess():

    def __init__(
        self,
        location='',
        floor='',
        section='',
        image_path="",
    ):
        self._location = location
        self._floor = floor
        self._section = section
        self._image_path = image_path
    
    def save(self):
        dictionary = {
            'loc':self._location,
            'floor':self._floor,
            'section':self._section,
            'path':self._image_path
        }
        np.save('{}_{}_{}.npy'.format(self._location, self._floor, self._section), dictionary)

save = PreProcess('festivalwalk', '6', '5', image_path='./data/images/6_60.jpg')
save.save()
    