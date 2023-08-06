#coding:UTF-8
#A:nlvac97
#PN:CIVILMOD
#V:0.92.52A-rel

#FC:main(SECOND)
#PUrl:nlvac97.github.io
import time as sj
import platform as pt
import os as xt
import sys as xt2
import string as zfc
import random as sjs
import os.path as xtbl
import webbrowser as llq
import requests as qq
import json
import tkinter as gui
import tkinter.messagebox as guiMB
import tkinter.filedialog as guiFD

INFOES = {"Project Name":"civilmod",
          "Project Author":"Nlvac97",
          "Project Version":"0.92.52A-rel",
          "Project Offical Website":"nlvac97.github.io"}
__all__ = ("upgrade","visitOurOfficalWebsite","getBMI","translate","donothing","pausePrint","openFolder","CivilmodError","captcha","ask","playMusic")
class CivilmodError(Exception):
    def __init__(self,errorcode):
        self.errorcode=errorcode
    def __str__(self,*args):
        return "[Errno "+self.errorcode+"]"
"""
(F)upgrade
检查civicmod版本，需要联网完成，
未联网情况下将返回CivicmodError
函数错误代码：C97612
"""
def upgrade():
    EC="C97612"
    from bs4 import BeautifulSoup as pc
    v = '0.92.52'
    URL='https://pypi.org/project/civilmod/#history'
    dd = []
    r = (qq.get(URL))
    l = pc(r.text,'lxml')
    #['0', '92', '5'] ['0', '92', '7'] N-C
    d = l.find_all('p',class_='release__version')
    for nn in d:
        ev = nn.text.strip()
        dd.append(ev)
    new = dd[0].split('.')
    cur = v.split('.')
    a1 = int(new[0])
    a2 = int(new[1])
    a3 = int(new[2])
    b1 = int(cur[0])
    b2 = int(cur[1])
    b3 = int(cur[2])
    #OK
    if a1==b1 and a2==b2 and a3==b3:
        print("您正在使用的版本 "+v+"    是最新版本，无需更新")
    #Have-lat
    if a1>b1 or a2>b2 or a3>b3:
        print("截至目前"+dd[0]+'已经发布，请及时更新')
    #Front
    if b1>a1 or b2>a2 or b3>a3:
        print("你正在使用测试版   "+v+"    当前正式版为"+dd[0])
"""
(F)visitOurOfficalWebsite
访问我们的官网
函数错误代码：C82631
"""
def visitOurOfficalWebsite():
    EC="C82631"
    llq.open("https://nlvac97.github.io")
"""
(F)getBMI
获取BMI
函数错误代码：C83523
"""
def getBMI(sg,tz):
    EC='C83523'
    result = {'height':None,'weight':None,'BMIindex':None,'evaluate':None}
    result['height'] = (str(sg)+"m")
    result['weight'] = (str(tz)+"kg")
    #检查：传入值是否为 数字
    if isinstance(tz,int)==False:
        if isinstance(tz,float)==False:
            raise(
                CivilmodError(EC))
    if isinstance(sg,int)==False:
        if isinstance(sg,float)==False:
            raise(
                CivilmodError(EC))
    r = (tz/(sg*sg))
    r = round(r,1)
    result['BMIindex'] = r
    if r <18.5:
        result['evaluate'] = '过轻'
    if r >= 18.5 and r<24.9:
        result['evaluate'] = '正常'
    if r >= 24.9 and r<29.9:
        result['evaluate'] = '过重'
    if r >= 29.9:
        result['evaluate'] = '肥胖'
    return result
"""
(F)captcha
生成一个4位数的验证码
函数错误代码:C68231
"""
def captcha():
    EC="C68231"
    capt = ''
    N = [1,2,3,4,5,6,7,8,9,0,'a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M',
         'n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z']
    for n in range(4):
        capt += str(N[sjs.randint(0,61)])
    return capt
"""
(F)translate
翻译（仅支持中英互译）需要联网完成
函数错误代码：C61377
"""
def translate(string):
    EC="C61377"
    URL = "https://fanyi.youdao.com/translate"
    pr = {'doctype':'json', 'type':'AUTO', 'i':str(string)}
    r = (qq.get(URL,params=pr))
    r2c = r.json()
    re = r2c['translateResult'][0][0]["tgt"]
    return [string,re]
"""
(F)ask
判断
函数错误代码：C46302
"""
def ask(content,classes):
    EC="C46302"
    attribute = ['yn','tf']
    if classes not in attribute:
        raise CivilmodError(EC)
    if classes == 'yn':
        ace = input(content+'(Y/N):')
        if ace == 'Y' or ace == "y":
            return True
        elif ace == 'N' or ace == "n":
            return False
        else:
            return None
    if classes == 'tf':
        ace = input(content+'(T/F):')
        ace = ace.upper()
        if ace == 'T' or ace == "t":
            return True
        elif ace == 'F' or ace == "f":
            return False
        else:
            return None
"""
(F)verbatimPrint
按照时间逐字打印
函数错误代码：C81812
"""
def verbatimPrint(*content,space=False,pause=0.2):
    EC="C81812"
    if isinstance(pause,float)==False and isinstance(pause,int)==False:
        raise CivilmodError(EC)
    for tex in content:
        for prin in str(tex):
            print(prin,end=' ' if space else '',flush=True)
            sj.sleep(pause)
        print(" ",flush=True,end="")
    print("\n",flush=True,end="")
"""
(F)openFolder
（本函数部分代码参考于xes[学而思]库）
打开文件夹，如指定fileName且fileName不存在Desktop将自动创建（限Windows，由于我没有Linux MacOS，如有问题请联系，谢谢合作！）
函数错误代码：C19463
"""
def openFolder(fileName=None,returnPath=False):
    EC="C19463"
    def platformCheck():
        if pt.system() == "Darwin":
            return xtbl.expanduser("~/Desktop/")
        elif pt.system() == "Windows":
            import winreg as sczcb
            keyn = sczcb.OpenKey(sczcb.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
            return sczcb.QueryValueEx(keyn, "Desktop")[0] + "/"
        else:
            return xtbl.expanduser("~/Desktop/")
    if fileName:
        newPath = platformCheck() + fileName
        if not xtbl.exists(newPath):
            xt.mkdir(newPath)
    else:
        newPath = xt.getcwd()
    if pt.system() == "Windows":
        xt.startfile(newPath)
    elif pt.system() == "Darwin":
        import subprocess as zlc
        zlc.Popen(["open", newPath])
    else:
        import subprocess as zlc
        zlc.Popen(["xdg-open", newPath])
    if returnPath:
        return newPath + "/"
"""
(F)playMusic
播放音乐
utkf = Using TKinter Find使用TKinter寻找
函数错误代码：C97103,C97104,C97105
"""
def playMusic(path=None,utkf=True,stop=None):
    EC="C97103"
    EC2="C97104"
    EC3="C97105"
    import pygame as pyyx
    if isinstance(stop,int)==False and isinstance(stop,float)==False and stop!=None:
        raise CivilmodError(EC)
    if path!=None:
        if xtbl.isfile(path)==False:
            raise CivilmodError(EC2)
    if utkf:
        a = gui.Tk()
        a.withdraw()
        path = guiFD.askopenfilename()
        if path=='':
            raise CivilmodError(EC3)
    pyyx.mixer.init()
    t = pyyx.mixer.music.load(path)
    pyyx.mixer.music.play()
    if stop!=None:
        sj.sleep(stop)
        pyyx.mixer.music.pause()
    if stop==None:
        ok = True
        while ok:
            if ask("现在暂停？",'yn'):
                ok=False
                pyyx.mixer.music.pause()

"""
(F)donothing
空翻译都知道的。。。
函数错误代码：C00016
"""
def donothing():
    EC="C00016"
    pass
"""
(C)CivilmodError
Civilmod错误
"""
class CivilmodError(Exception):
    def __init__(self,errorcode):
        self.errorcode=errorcode
    def __str__(self,*args):
        return "[Errno "+self.errorcode+"]"
