import os;
import re;
import sys;
sys.path.append("lib");
from multiprocessing import Pool,Manager,Lock
import os, time
from liblinearutil import *
import FilePro as FP
import roc_pro as rp

def decomp_values(a,b):
    print "Start process %s"%(os.getpid())
    filetrain="P/COMP/mxsub%s_%s"%(a,b)
    y,x=svm_read_problem(filetrain)
    
    prob=problem(y,x)
    del x
    del y

    param=parameter('-s 3 -c 5 -q')
           #train
    p_labels,acc,p_values=predict(y2,x2,train(prob,param))
    print 'Start open file'+'MP/Values/v%s_%s'%(a,b)
    f=open('P/Values/v%s_%s'%(a,b),"w")
    #print 'Success open file'+'MP/Values/v%s_%s'%(a,b)
    for v in p_values:
        f.write(str(v[0])+' ')
    f.close()

def init_anay():  
    pool=Pool(2)
    for i in range(4):
        for j in range(12):
            #print "%s %s"%(i,j)
            pool.apply_async(decomp_values,args=(i,j))
    pool.close()
    pool.join()

def anay(a,b,threshold,label):
    fvalue=open("P/Values/v%s_%s"%(a,b),"r")
    temp=fvalue.read().split()
    p_values=[]
    for i in temp:
	p_values+=[float(i)]
    p_labels=rp.predict_threshold(p_values,threshold)
    print "sub process start min: %s"%(os.getpid())
    with lock[a]:
        for i in range(len(p_labels)):
    	    label[a][i]= label[a][i] and p_labels[i]
            
    #print label[a][0:100]
    print "$ ",len(p_labels)," $ ",len(y2)," $ ",len(x2)
    
    
if __name__=='__main__':
    filetest="Data/Utest.txt"
    y2,x2=svm_read_problem(filetest)
    f=open('P/flag','r')
    if len(f.read())== 0:
    	init_anay()
        f.close()
        f=open('P/flag','w')
        f.write('1')
        f.close()
    f.close()
    thresholds=[-8,-4,-2,-1,-0.5,0,0.5,1,2,4,8]
    TPR,FPR,F1=[],[],[]
    for ii in thresholds:
    	labelist=[Manager().list([1 for xx in range(37786)]) for yy in range(4)]
    	lock=[Lock() for xx in range(4)]
    	pool=Pool(4)
    	for i in range(4):
        	for j in range(12):
            		print "%s %s"%(i,j)
            		pool.apply_async(anay,args=(i,j,ii,labelist))
    	pool.close()
    	pool.join()
   	 #print "Total time is ", time.clock()-t," s"
    	result=[]
    	for i in range(37786):
        	result.append(labelist[0][i] or labelist[1][i] or labelist[2][i] or labelist[3][i])
        f=open('P/Results/r%s'%(ii),'w')
        for i in result:
		f.write(str(i)+' ')
    	TPr,FPr,TP,FN,FP,TN=rp.Result_Analy(result,y2)
    	TPR+=[TPr]
    	FPR+=[FPr]
    	
    print TPR,FPR
    
