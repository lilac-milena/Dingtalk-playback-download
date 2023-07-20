#coding:utf-8



import os
import sys
import platform


#判断系统类型
systype = platform.system()

if systype == 'Windows':
    clstext='cls'
if systype == 'Linux':
    clstext='clear'





os.system(clstext)

print("使用前请准备ffmpeg环境")
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

print("请选择m3u8来源\n1.Windows端群直播\n2.在线课堂\n3.Linux或手机端群直播\n注:本选项用于格式化m3u8文件\n-----------------\n")
mmutype=input('类型(1-3):')
if mmutype=='1':
    
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
    
elif mmutype=='3':

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

print(tsurls)
# 至此 数据处理完毕
# ↓下载↓
urls=tsurls.split("\n")
urls_line=int(len(urls))-1-stop #ts URL数量
print("将下载 "+str(urls_line)+" 个分段")

nowts=0 #当前ts
tsstxt='' #ts文件目录树
errortss=0 #下载错误的tss数量
errorts=[] #下载错误的ts链接
os.system('mkdir tss') #创建用于存储ts文件的目录

while nowts<urls_line:

    if os.system("curl "+urls[nowts]+" -o tss/"+str(nowts)+".ts")!=0: #判断是否下载失败
        if os.system("curl "+urls[nowts]+" -o tss/"+str(nowts)+".ts")!=0: #如下载失败则重新下载
            errortss=errortss+1 #重新下载失败
            errorts.append(str(nowts)+' | '+urls[nowts]) #将错误的ts链接存入列表

        

    tsstxt=tsstxt+"file  'tss/"+str(nowts)+".ts'"+"\n"
    nowts=nowts+1

print(tsstxt)

with open('tss.txt','w') as f: #写目录树
    f.write(tsstxt)

os.system(clstext)


if errortss==0: #判断是否全部下载完成
    os.system('ffmpeg -f concat -i tss.txt -c copy output.mp4') #利用ffmpeg合并视频文件
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
