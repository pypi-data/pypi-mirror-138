#coding:UTF-8
#A:nlvac97
#PN:CIVILMOD
#V:0.92.52A-rel
#FC:auxiliary(A)
#PUrl:nlvac97.github.io
from . import cm as civilmod
from . import TKOperation as lpys

class fort():
    def __init__(self,lp):
        EC="C99137"
        """
        (C-F)init
        函数错误代码：C99137
        """
        if lp != lpys.gtBK() and lp != lpys.gtSQ()['PKEP']:
            raise civilmod.CivilmodError(EC)
    def run(self):
        EC="C54182"
        #Q1
        a = civilmod.ask("小虎帅不帅？",'yn')
        if a or a==None:raise civilmod.CivilmodError(EC)
        else:
            b = civilmod.ask("小虎厉害吗？",'yn')#Q2
            if b or b==None:raise civilmod.CivilmodError(EC)
            else:
                c = civilmod.ask("小虎是UT？","tf")#Q3
                if c:
                    d = civilmod.ask("小虎会被撕票吗？","yn")#Q4
                    if d:return True
                    else:raise civilmod.CivilmodError(EC)
                else:raise civilmod.CivilmodError(EC)
