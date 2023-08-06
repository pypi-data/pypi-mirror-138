#coding:UTF-8
#A:nlvac97
#PN:CIVILMOD
#V:0.92.52A-rel
#FC:auxiliary(B)
#PUrl:nlvac97.github.io
import os.path as xtbl
backing = 99999-88888-11111+123-123+9-1+2-3+1-6+3-2
def gtBK():
    global backing
    a = xtbl.abspath(xtbl.dirname(xtbl.abspath(__file__)) + xtbl.sep + ".")
    a = a + "/tk"
    comDD = open(a+str(backing)+".py",'r')
    c = comDD.read()
    comDD.close()
    return c
def gtSQ():
    infoes = {"PCAP":"J2420K","PACP":"G9199X","PKEP":"H2009P"}
    return infoes
