from __future__ import division
import time
import torch 
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import cv2 
from yolo.util import *
from yolo.darknet import Darknet
from yolo.preprocess import prep_image, inp_to_image
import pandas as pd
import random 
import argparse
import pickle as pkl

class Yolo:

    def __init__(self):
        # set args
        self.args = self.arg_parse()
        self.confidence = float(self.args.confidence)
        self.nms_thesh = float(self.args.nms_thresh)


        # load file
        self.cfgfile = "yolo/cfg/yolov3.cfg"
        self.weightsfile = "yolo/yolov3.weights"
        self.classes = load_classes('yolo/data/coco.names')
        self.colors = pkl.load(open("yolo/pallete", "rb"))

        # set model
        self.num_classes = 80
        self.bbox_attrs = 5 + self.num_classes
        
        self.model = Darknet(self.cfgfile)
        self.model.load_weights(self.weightsfile)
        
        self.model.net_info["height"] = self.args.reso
        self.inp_dim = int(self.model.net_info["height"])
        
        self.model.eval()

    def arg_parse(self):    
    
        parser = argparse.ArgumentParser(description='YOLO v3 Cam Demo')
        parser.add_argument("--confidence", dest = "confidence", help = "Object Confidence to filter predictions", default = 0.25)
        parser.add_argument("--nms_thresh", dest = "nms_thresh", help = "NMS Threshhold", default = 0.4)
        parser.add_argument("--reso", dest = 'reso', help = 
                            "Input resolution of the network. Increase to increase accuracy. Decrease to increase speed",
                            default = "160", type = str)
        return parser.parse_args()

    def prep_image(self,img, inp_dim):
        orig_im = img
        dim = orig_im.shape[1], orig_im.shape[0]
        img = cv2.resize(orig_im, (inp_dim, inp_dim))
        img_ = img[:,:,::-1].transpose((2,0,1)).copy()
        img_ = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)
        return img_, orig_im, dim

    def write(self, x, img):
        c1 = tuple(x[1:3].int())
        c2 = tuple(x[3:5].int())
        cls = int(x[-1])
        label = "{0}".format(self.classes[cls])
        color = random.choice(self.colors)
        cv2.rectangle(img, (int(c1[0]),int(c1[1])), (int(c2[0]),int(c2[1])),color, 1)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
        c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
        cv2.rectangle(img, (int(c1[0]),int(c1[1])), (int(c2[0]),int(c2[1])),color, -1)
        cv2.putText(img, label, (int(c1[0]), int(c1[1]) + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1);
        # print("[*] label:{} c1x:{} c1y:{} c2x:{} c2y:{}".format(label, c1[0], c1[1], c2[0], c2[1]))
        
        return [label, c1[0].numpy(), c1[1].numpy(), c2[0].numpy(), c2[1].numpy()]

    def detect_bbox(self,frame, imshow=True):

        img, orig_im, dim = self.prep_image(frame, self.inp_dim)
        
        CUDA = False # torch.cuda.is_available()
        output = self.model(Variable(img), CUDA)
        output = write_results(output, self.confidence, self.num_classes, nms = True, nms_conf = self.nms_thesh)

                
        output[:,1:5] = torch.clamp(output[:,1:5], 0.0, float(self.inp_dim))/self.inp_dim

        output[:,[1,3]] *= frame.shape[1]
        output[:,[2,4]] *= frame.shape[0]

        
        bbox = list(map(lambda x: self.write(x, orig_im), output))
        
        if imshow:
            cv2.imshow("frame", orig_im)
            key = cv2.waitKey(3*1000) # wait and show msec   
        
        return bbox