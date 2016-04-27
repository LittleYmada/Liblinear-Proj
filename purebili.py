import os,sys,re
sys.path.append("lib");
from liblinearutil import *
import FilePro as FP
import roc_pro as rp
import time
import io
y,x=svm_read_problem("Data/Utrain.txt")
prob=problem(y,x)
del x
del y
s=time.time()
param=parameter('-s 3 -c 5 -q -B 0')
mod=train(prob,param)
print "Train for %s s"%(time.time()-s)
y2,x2=svm_read_problem("Data/Utest.txt")
s=time.time()
p_labels,p_acc,p_vals=predict(y2,x2,mod)
e=time.time()
del x2

print 'predict for %s s'%(e-s)
for i in range(len(p_vals)):
    p_vals[i]=p_vals[i][0]
print p_vals

shold=[-8,-4,-2,-1,-0.5,0,0.5,1,2,4,8]
pl=[]
TPR,FPR,F1=[],[],0
for i in shold:
    pl+=[rp.predict_threshold(p_vals,i)]
for j in pl:
    TP,FP=rp.Result_Analy(j,y2)
    TPR+=[TP]
    FPR+=[FP] 
print  TPR,'\n',FPR




