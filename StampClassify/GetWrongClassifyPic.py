#挑出错误分类图片
import torch
from torchvision import transforms
from torchvision import models
import torch.utils.data as Data
import torch.nn as nn
import torch.optim as optim
import time
import numpy as np
import DataOperation
import cv2
import os
import shutil

def imgClassify(inputImg):
    #加载训练好的模型
    model = torch.load('resnet.pkl')
    #print(model)
    #固定模型参数
    model.eval()

    #输入格式调整
    BATCH_SIZE = 1
    my_data = DataOperation.MyDataset(inputImg, transform=transforms.ToTensor())
    my_loader = DataOperation.Data.DataLoader(dataset=my_data, batch_size=BATCH_SIZE)
    for batch_index, (test_x, test_y) in enumerate(my_loader):
        test_output = model(test_x)
        pred_y = torch.max(test_output, 1)[1].data.numpy()

    classfy = pred_y

    return classfy

#单张
# def main():
#     impath="test.jpg"
#     # im=cv2.imread(impath)
#     predict = imgClassify(impath)
#     print("图片:%s,预测%s"%(impath,predict))

#多张根据预测结果移动图片
# SouceFoloder = "/Users/applezhj/workspace/pycharm/deepLearing/StampDB/SomeBadStamp"
# TargetFolder = "/Users/applezhj/workspace/pycharm/deepLearing/StampDB/SomeBadStamp/Erro"
SouceFoloder = "/Users/applezhj/workspace/pycharm/deepLearing/StampDB/test/0"
TargetFolder = "/Users/applezhj/workspace/pycharm/deepLearing/StampDB/wrongClassify/0"
def findImgIt(filePath):
    fileList = os.listdir(filePath)
    for file in fileList:
        fullFilePath = os.path.join(filePath,file)
        if os.path.isdir(fullFilePath):
            findImgIt(fullFilePath)
        elif file.endswith(".jpg"):
            if not file.startswith("."):
                predict = imgClassify(fullFilePath)
                predict = predict[0]
                if not predict == 0:
                    print(predict)
                    # targetClassFolder = os.path.join(TargetFolder,str(predict))
                    if not os.path.exists(TargetFolder):
                        os.mkdir(TargetFolder)
                    temp = os.listdir(TargetFolder)
                    number = len(temp)
                    newFilename = os.path.join(TargetFolder, str(number)+".jpg")
                    while (os.path.exists(newFilename)):
                        number = number + 1
                        newFilename = os.path.join(TargetFolder, str(number) + ".jpg")
                    shutil.copy(fullFilePath, newFilename)
def main():
    # componyList = os.listdir(SouceFoloder)
    # for cp in componyList:
    #     fullFilePath = os.path.join(SouceFoloder,cp)
        findImgIt(SouceFoloder)

if __name__ == "__main__":
    main()