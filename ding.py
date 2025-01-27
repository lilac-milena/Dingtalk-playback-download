#coding:utf-8

import os
import sys
import platform
import subprocess

#判断系统类型
systype = platform.system()
for_linux_local_installed_ffmpeg = ""

if systype == 'Windows':
    clstext= 'cls'
elif systype == 'Linux':
    clstext= 'clear'
else:
    clstext= 'clear'

os.system(clstext)

def noFFmpegExit():
    print("""没有检测到 FFmpeg 环境
FFmpeg 是用于合成视频片段的必备运行环境

如果您全量下载了该脚本包，那么您可以在与该脚本同级的目录下找到名为 FFmpeg-Installation-Script-Linux.sh 和 FFmpeg-Installation-Script-Windows.bat 的 FFmpeg 安装脚本。
如您是 Windows 用户，可以运行 FFmpeg-Installation-Script-Windows.bat，如您是 Linux 用户，可以运行 sh FFmpeg-Installation-Script-Linux.sh，脚本会自动为您配置 FFmpeg 环境。


此外，您也可以选择手动安装 FFmpeg 环境，详情见 FFmpeg 官方网站：https://www.ffmpeg.org/
    """)

    sys.exit()

# 判断 ffmpeg 环境
try:
    subprocess.run(["ffmpeg","-version"], check=True)
    os.system(clstext)
    print("FFmpeg 已安装")
except:
    # 对于 Linux 系统
    if systype == 'Linux':
        try:
            subprocess.run(["./ffmpeg","-version"], check=True)
            os.system(clstext)
            for_linux_local_installed_ffmpeg = "./"
            print("FFmpeg 已安装")
        except:
            noFFmpegExit()
    else:
        noFFmpegExit()

    

print("---------------------------")
print("下载通道:\n1.https://dtliving-sz.dingtalk.com/live_hp/\n2.https://dtliving-sh.dingtalk.com/live_hp/\n3.https://dtliving-bj.dingtalk.com/live_hp/\n4.自定义\n---------------\n以上都是钉钉官方的API,钉钉的直播下载url应该是随机的,所以要根据抓包结果选择")
print("---------------------------")
geturl=input("下载域名(1-4):")
if geturl=='1':
    dowurl='https://dtliving-sz.dingtalk.com/live_hp/'
else:
    if geturl=='2':
        dowurl='https://dtliving-sh.dingtalk.com/live_hp/'
    else:
        if geturl=='3':
            dowurl='https://dtliving-bj.dingtalk.com/live_hp/'
        else:
            if geturl=='4':
                dowurl=input("请输入自定义链接(结尾要加/):")
            else:
                print('选择无效')
                sys.exit()

os.system(clstext)


with open('m3u8.txt', 'w') as f: #新建用于存放m3u8内容的txt文件
    f.write('')

print('-------m3u8文件已创建-------')
print('')
print('已在脚本运行目录新建了 m3u8.txt 文件，请您将m3u8内容粘贴在此文件中')
print('')

writetype=input('如已操作完毕，请输入 y : ')

if writetype=='y':
    with open('m3u8.txt','r') as f: #读取m3u8内容
        text=f.read()
else:
    print('选择无效')
    sys.exit()


os.system(clstext)

print("请选择m3u8来源\n1.浏览器调试控制台 或 Linux客户端\n2.在线课堂\n3.Windows端群直播\n注:本选项用于格式化m3u8文件\n-----------------\n")
mmutype=input('类型(1-3):')
if mmutype=='3':
    
    os.system(clstext)


    notdot=text.replace(', ','.,.') #将", "替换为".,."防止将", "中的空格转换为换行
    ntext=notdot.replace(' ','\n') #将" "转换为换行
    stext=ntext.replace('.,.',', ') #将".,."转换回", "
elif mmutype=='2':
    text=''
    nowtext=''
    os.system(clstext)

    usetext=text.replace('#',' #')[1:]
    text=usetext

    notdot=text.replace(',','.,.') #将", "替换为".,."防止将", "中的空格转换为换行
    ntext=notdot.replace(' ','\n') #将" "转换为换行
    stext=ntext.replace('.,.',', ') #将".,."转换回", "
    
elif mmutype=='1':

    stext=text.replace(',\n',', ') #将",\n"转换回", "
    
else:
    print('选择无效')
    sys.exit()






# -------
# text        notdot          ntext       stext
# 原m3u8文本  替换, 后的文本   分行后文本    最终可用文本
# -------

list_text=stext.split("\n") #将m3u8内容按回车分割

list_line=int(len(list_text))-2 #ts文件行数

nowline=4 #当前读取到的行数,从4开始,跳过头文件

tss='' #临时存放ts URL(部分)的变量
tsurls='' #存储ts文件url
stop=0 #停止的次数 


print(stext)

with open('m3u8.txt', 'w') as f: #新建用于存放m3u8内容的txt文件
    f.write(stext)

while nowline<=list_line:
    
    nowtext=list_text[nowline]
    nowtext_list=nowtext.split(", ")

    if "#EXT-X-DISCONTINUITY" in nowtext:
        print("出现暂停")
        print(nowline)
        nowline=nowline+1
        stop=stop+1

    else:
        
        if "#EXT-X-ENDLIST" in nowtext:
            print("解析结束")
            break
        
        else:
            print(nowtext)
            tsurls=tsurls+dowurl+nowtext_list[1]+'\n'
            print("ok")
            nowline=nowline+1

print("t:" + tsurls)
# 至此 数据处理完毕
# ↓下载↓
urls=tsurls.split("\n")
urls_line=len(urls)-1
print("将下载 "+str(urls_line)+" 个分段")

nowts=0 #当前ts
tsstxt='' #ts文件目录树
errortss=0 #下载错误的tss数量
errorts=[] #下载错误的ts链接

os.system('mkdir tss') #创建用于存储ts文件的目录

for f in os.listdir("tss"):
    os.remove(os.path.join("tss", f))

while nowts<urls_line:
    
    print(str(nowts)+"/"+str(urls_line))
    
    def download_this_part(this_part_url, this_part_nowts):
        try:
            this_res = subprocess.run(["curl", this_part_url, "-o", "tss/"+str(this_part_nowts)+".ts","-f"], check=True)
            if this_res.returncode == 0:
                return 0
            else:
                return False
        except subprocess.CalledProcessError as e:
            print(e)
            return False
        
    if download_this_part(urls[nowts], nowts)!=0: #判断是否下载失败
        if download_this_part(urls[nowts], nowts)!=0: #如下载失败则重新下载
            errortss=errortss+1 #重新下载失败
            errorts.append(str(nowts)+' | '+urls[nowts]) #将错误的ts链接存入列表

    tsstxt=tsstxt+"file  'tss/"+str(nowts)+".ts'"+"\n"
    nowts=nowts+1

print(tsstxt)

with open('tss.txt','w') as f: #写目录树
    f.write(tsstxt)

os.system(clstext)


if errortss==0: #判断是否全部下载完成
    os.system(for_linux_local_installed_ffmpeg + 'ffmpeg -f concat -i tss.txt -c copy output.mp4') #利用ffmpeg合并视频文件
    print("下载成功，视频文件已保存至 output.mp4")
else:
    
    with open('err.log','w+') as f: #写错误的ts链接
        f.write(str(errorts))

    print('-下载失败-')
    print('已对下载失败的ts文件尝试再次下载，依旧无法下载')
    print('')
    print('ts总数量: '+str(urls_line))
    print('下载失败ts数量: '+str(errortss))
    print('')
    if str(errortss)==str(urls_line):
        print('提示信息：您的ts文件全部下载失败，请检查是否为网络问题或下载地址设置有误')
    print('')
    print('---详细信息已写入 err.log 文件---')