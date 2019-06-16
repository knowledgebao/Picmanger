import os
import shutil

#功能：删除复制的文件
#输入：目录
#输出: 无
def DelCopyFile(parentDir):
    imgPaths = []
    #遍历目录下所有子目录加入imPaths,包含parentDir目录
    for parent, dirnames, filenames in os.walk(parentDir, followlinks=True):
        for dirname in dirnames:
            print('文件名：%s' % parent + "\\" + dirname)
            imgPaths.append(parent + "\\" + dirname)
    #处理每个目录下的文件，如果是复制的文件，则删除
    #复制文件的标志如下：oldfile.exe->oldfile (num).exe，比如：imgtesp.bmp->imgtesp (1).bmp
    for imgPath in imgPaths:
        if os.path.isdir(imgPath):
            for filename in os.listdir(imgPath):
                shotname, extension = os.path.splitext(filename)#获取文件名及后缀
                splitList = shotname.split('(')#如果存在(
                if len(splitList) > 1:
                    splitList2 = splitList[1].split(')')#如果存在)
                    if len(splitList2) > 0:
                        num = splitList2[0]#获取()内部的数字
                        if num.isdigit():#如果是数字
                            oldFile = splitList[0].strip()+extension
                            if os.path.isfile(imgPath+"\\"+oldFile):#原始文件存在
                                if os.path.getsize(oldFile) == os.path.getsize(imgPath+"\\"+oldFile):
                                    os.remove(imgPath+"\\"+filename)
                                else:
                                    print("not same file")
                            else:
                                print("old file is not exist")
                                shutil.move(filename,oldFile)
                        else:
                            print("()in not find digit")
                    else:
                        print("not find )")
                else:
                    print("not find (")
        else:
            print("path is not exist")

if __name__=="__main__":
    parentDir = "D:\\life\\Photo"