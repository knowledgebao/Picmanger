import os
import shutil
from processVideo import *
from processPicture import *

#功能：遍历指定目录下所有的图片文件，返回图片及图片拍摄时间
#输入：图片目录文件
#输出：返回二个列表：文件，文件拍摄时间
def getfiletime(imgpath):
    videolist = ["vob","ifo","mpg","mpeg","dat","mp4","3gp","mov","rm","ram","rmvb","wmv","asf","avi","asx"]
    picturelist = ["bmp","jpg","png","tif","gif","pcx","tga","exif","fpx","svg","psd","cdr","pcd","dxf","ufo","eps","ai","raw","WMF","webp"]
    olds = []
    news = []
    for filename in os.listdir(imgpath):#遍历目录下的所有照片或视频文件
        full_file_name = os.path.join(imgpath, filename)
        if os.path.isfile(full_file_name):#只处理文件，不处理目录
            time="",""
            ext = full_file_name.split(".")[-1].lower()#文件后缀
            if ext in picturelist:#图片文件
                time = GetPictureTime(full_file_name)
                print(full_file_name, ":", time)
                olds.append(filename)
                news.append(time)
            elif ext in videolist:#视频文件
                time = GetVideoTime(full_file_name)
                print(full_file_name, ":", time)
                olds.append(filename)
                news.append(time)
            else:
                print("do not support file type")
    return olds,news

#功能：创建指定目录，如果存在跳过，不存在则创建
#输入：计划创建的目录
def createdir(dir):
    ret = os.path.exists(dir)
    if not ret:
        os.makedirs(dir)
    else:
        pass

#测试执行
if __name__=="__main__":
    dstPath = "D:\\life\\Photo"#相册归档目录
    dstPathTemp = "D:\\life\\Photo\\temp"#无法获取照片或视频时间的归档目录
    processPath = 'C:\\Users\\jinhan\\Desktop\\photo'  #准备归档的目录，支持递归查找

    # dstPath = "D:\\life\\test"
    # processPath = "D:\\life\\大"
    createdir(dstPathTemp)
    imgPaths = []#存放归档文件的所有目录，包含各级子目录
    imgPaths.append(processPath)
    for parent, dirnames, filenames in os.walk(processPath, followlinks=True):
        for dirname in dirnames:
            print('文件名：%s' % parent +"\\"+ dirname)
            imgPaths.append(parent +"\\"+ dirname)
    imgPaths.sort(reverse = True)
    #imgPaths = []
    for imgPath in imgPaths:
        if os.path.isdir(imgPath):#判断目录是否存在
            filelist, timelist = getfiletime(imgPath)#获取目录下所有的照片列表
            for index, fileName in enumerate(filelist):
                if timelist[index] != "":
                    year = timelist[index][0:4]
                    mounth = timelist[index][4:6]
                    newImgPath = dstPath +"\\"+ year + "\\" + mounth
                    createdir(newImgPath)
                    oldAbsFile = imgPath + "\\" + fileName
                    dstAbsFile = newImgPath + "\\" +timelist[index]+"_"+ fileName
                    if imgPath != newImgPath:
                        if os.path.isfile(dstAbsFile):
                            if os.path.getsize(oldAbsFile) == os.path.getsize(dstAbsFile):
                                print("remove++++++++++++++++", oldAbsFile)
                                os.remove(oldAbsFile)
                            else:
                                print("file name same,but not same file")
                                shutil.move(oldAbsFile, newImgPath + "\\" +timelist[index]+"_same"+ fileName)
                        else:
                            shutil.move(oldAbsFile, dstAbsFile)
                    else:
                        print("srcPath == dstPath")
                else:
                    print("not find time",fileName)
                    # oldAbsFile = imgPath + "\\" + fileName
                    # dstAbsFile = dstPathTemp + "\\" + fileName
                    # if imgPath != dstPathTemp:
                    #     if os.path.isfile(dstAbsFile):
                    #         if os.path.getsize(oldAbsFile) == os.path.getsize(dstAbsFile):
                    #             print("remove++++++++++++++++", oldAbsFile)
                    #             os.remove(oldAbsFile)
                    #         else:
                    #             print("file name same,but not same file")
                    #             shutil.move(oldAbsFile, newImgPath + "\\" + timelist[index] + "_same" + fileName)
                    #     else:
                    #         shutil.move(oldAbsFile, dstAbsFile)
                    # else:
                    #     print("imgPath == dstPathTemp")
            if len(os.listdir(imgPath)) == 0:
                print(imgPaths,"dir is empty")
                # os.rmdir(imgPath)
        else:
            print(imgPath,"is not exist\n")