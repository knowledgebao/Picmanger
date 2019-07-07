import os
import subprocess
import traceback
import tempfile

FFPROBE = "D:\\code\\Picmanger\\ffprobe"

#获取cmd的执行结果
def getcmdresult(cmd):
    try:
        out_temp = tempfile.SpooledTemporaryFile()
        fileno = out_temp.fileno()
        obj = subprocess.Popen(cmd, stdout=fileno, stderr=fileno, shell=True)
        obj.wait()
        out_temp.seek(0)
        lines = out_temp.readlines()
        # print(lines)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        if out_temp:
            out_temp.close()
    return lines

#输入：文件名(filename)
#输出：文件的拍摄时间:20181207_031034
#失败: 空
def GetVideoTime(fileabspath):
    # cmd = 'ffprobe D:\\life\\Photo\\photo\\100APPLE\\AFJX7823.MP4'  # 可以直接在命令行中执行的命令
    cmd = FFPROBE+' '+fileabspath  # 可以直接在命令行中执行的命令
    # p, f = os.path.split(fileabspath)
    cmdRet = getcmdresult(cmd)
    time = ''
    for line in cmdRet: #按行遍历
        #creation_time   : 2018-09-08T03:50:42.000000Z
        line = line.decode(encoding='gbk').strip()#去除空格已经使用utf-8编码
        if line.find("creation_time") != -1:
            ll = line.split('.')#[creation_time   : 2018-09-08T03:50:42,000000Z]
            if len(ll) > 1:
                ret = ll[0].split(" ") #[creation_time,:,2018-09-08T03:50:42]
                time = ret[-1].replace('-',"").replace('T','_').replace(':',"")#20180908_035042
                break
    return time

if __name__ == "__main__":
    time = GetVideoTime("D:\\life\\Photo\\2019\\01\\20190115_142556_UOQW2161.MP4")
    #time = GetVideoTime("C:\\Users\\jinhan\\Desktop\\photo\\DCIM\\103APPLE\\GRLE0703.MP4")

    print(time)
    print(1)
