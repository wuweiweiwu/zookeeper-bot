from sklearn import svm
from sklearn.externals import joblib
from PIL import Image
import os
import numpy


class Recognizer:
    def __init__(self):
        self.data = []
        self.values = []
        self.svc = svm.SVC(gamma=0.001, kernel='linear', C=100)
        self.downscale_size = (32, 32)

    def _load(self, path, value):
        images = os.listdir(path)
        for filename in images:
            img = Image.open(path+'/'+filename)
            img = img.resize(self.downscale_size, Image.BILINEAR)
            self.data.append(numpy.array(img.getdata()).flatten().reshape((1, -1)))
            self.values.append(value)

    def load(self):
        self._load('training-images/bunny', 0)
        self._load('training-images/elephant', 1)
        self._load('training-images/frog', 2)
        self._load('training-images/giraffe', 3)
        self._load('training-images/hippo', 4)
        self._load('training-images/lion', 5)
        self._load('training-images/monkey', 6)
        self._load('training-images/panda', 7)

    def train(self):
        if os.path.isfile('trained.dat'):
            self.svc = joblib.load('trained.dat')
        else:
            self.load()
            np_data = numpy.array(self.data)
            np_values = numpy.array(self.values)
            self.svc.fit(np_data, np_values)
            joblib.dump(self.svc, 'trained.dat', compress=9)

    def predict(self, image):
        image = image.resize(self.downscale_size, Image.BILINEAR)
        input_image = numpy.array(image.getdata()).flatten().reshape((1, -1))
        return int(self.svc.predict(input_image))
