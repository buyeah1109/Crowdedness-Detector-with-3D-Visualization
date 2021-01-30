import time
import numpy as np

class PreProcess():

    def __init__(
        self,
        location='',
        time=time.strftime("%Y%m%d_%H%M%S", time.localtime()),
        image_path="",
    ):
        self._location = location
        self._time = time
        self._image_path = image_path
    
    def save(self):
        dictionary = {
            'loc':self._location,
            'time':self._time,
            'path':self._image_path
        }
        np.save('{}_{}.npy'.format(self._location, self._time), dictionary)

save = PreProcess('test',image_path='./data/images/6_50.jpg')
save.save()
    