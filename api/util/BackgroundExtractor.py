import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import cv2
import uuid
import os
import imutils
import urllib.request

from model import U2NET
from torch.autograd import Variable
from skimage import io, transform
from PIL import Image


class BackgroundExtractor:
    def __init__(self):
        #self.currentDir = 'C:\\Users\\Kirill\\PycharmProjects\\EchisProject'
        self.currentDir = 'C:\\Users\\kgavr\\PycharmProjects\\EchisProject'
        # ------- Load Trained Model --------
        model_name = 'u2net'
        model_dir = os.path.join(self.currentDir, 'saved_models',
                                 model_name, model_name + '.pth')
        self.net = U2NET(3, 1)
        if torch.cuda.is_available():
            self.net.load_state_dict(torch.load(model_dir))
            self.net.cuda()
        else:
            self.net.load_state_dict(torch.load(model_dir, map_location='cpu'))
        # ------- Load Trained Model --------

    def save_output(self, image_name, output_name, pred, d_dir, type):
        predict = pred
        predict = predict.squeeze()
        predict_np = predict.cpu().data.numpy()
        predict_np = predict_np * 255
        if type == 'background':
            predict_np = 255 - predict_np

        im = Image.fromarray(predict_np).convert('RGB')
        image = io.imread(image_name)
        imo = im.resize((image.shape[1], image.shape[0]))
        pb_np = np.array(imo)

        if type == 'image' or type == 'background':
            # Make and apply mask
            mask = pb_np[:, :, 0]
            mask = np.expand_dims(mask, axis=2)
            imo = np.concatenate((image, mask), axis=2)
            imo = Image.fromarray(imo, 'RGBA')

        imo.save(d_dir + output_name)
        return imo

    def removeBg(self, imagePath):
        inputs_dir = os.path.join(self.currentDir, 'static/inputs/')
        results_dir = os.path.join(self.currentDir, 'static/results/')
        masks_dir = os.path.join(self.currentDir, 'static/masks/')
        backgrounds_dir = os.path.join(self.currentDir, 'static/backgrounds/')

        with urllib.request.urlopen(imagePath) as url:
            with open('temp.jpg', 'wb') as f:
                f = url.read()
                img = bytearray(f)


        # convert string of image data to uint8
        # with open(imagePath, "rb") as image:
        #    f = image.read()
        #    img = bytearray(f)

        nparr = np.frombuffer(img, np.uint8)

        if len(nparr) == 0:
            return '---Empty image---'

        # decode image
        try:
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        except:
            # build a response dict to send back to client
            return "---Empty image---"

        # save image to inputs
        unique_filename = str(uuid.uuid4())
        cv2.imwrite(inputs_dir + unique_filename + '.jpg', img)

        # processing
        image = transform.resize(img, (320, 320), mode='constant')

        tmpImg = np.zeros((image.shape[0], image.shape[1], 3))

        tmpImg[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
        tmpImg[:, :, 1] = (image[:, :, 1] - 0.456) / 0.224
        tmpImg[:, :, 2] = (image[:, :, 2] - 0.406) / 0.225

        tmpImg = tmpImg.transpose((2, 0, 1))
        tmpImg = np.expand_dims(tmpImg, 0)
        image = torch.from_numpy(tmpImg)

        image = image.type(torch.FloatTensor)
        image = Variable(image)

        d1, d2, d3, d4, d5, d6, d7 = self.net(image)
        pred = d1[:, 0, :, :]
        ma = torch.max(pred)
        mi = torch.min(pred)
        dn = (pred - mi) / (ma - mi)
        pred = dn

        frontground = self.save_output(inputs_dir + unique_filename + '.jpg', unique_filename +
                                       '.png', pred, results_dir, 'image')
        mask = self.save_output(inputs_dir + unique_filename + '.jpg', unique_filename +
                                '.png', pred, masks_dir, 'mask')
        background = self.save_output(inputs_dir + unique_filename + '.jpg', unique_filename +
                                      '.png', pred, backgrounds_dir, 'background')


        #return PIL.Image.Image instances

        return frontground,background
