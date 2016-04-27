import sys,os,re
sys.path.append("lib");
from multiprocessing import Pool,Manager,Lock
import os, time
from liblinearutil import *
import FilePro as FP
import roc_pro as rp

def decomp_train(a,b):
    print "Start process %s"%(os.getpid())
    filetrain="MP/M/mxsub%s_%s"%(a,b)
    y,x=svm_read_problem(filetrain)
    prob=problem(y,x)
    del x
    del y

    param=parameter('-s 3 -c 5 -q')
    mod=train(prob,param)
    save_model('MP/Mod/mod%s_%s'%(a,b),mod)

def decomp_predict(a,b,label):
    mod=load_model('MP/Mod/mod%s_%s'%(a,b))
    p_labels,acc,p_values=predict(y2,x2,mod)
    
    print "sub process start min: %s"%(os.getpid())
    with lock[a]:
        for i in range(len(p_labels)):
    	    label[a][i]= label[a][i] and p_labels[i]
            i+=1
    #print label[a][0:100]
    print "$ ",len(p_labels)," $ ",len(y2)," $ ",len(x2)
    #return p_labels

if __name__=='__main__':

    labelist=[Manager().list([1 for xx in range(37786)]) for yy in range(3)]
    lock=[Lock() for xx in range(3)]
    filetest="Data/Utest.txt"
    y2,x2=svm_read_problem(filetest)

    tstart=time.time()
    #print labelist
    pool=Pool(4)
    for i in range(3):
        for j in range(10):
            print "%s %s"%(i,j)
            pool.apply_async(decomp_train,args=(i,j))

    pool.close()
    pool.join()
    print "Train finished, using %s seconds"%(time.time()-tstart)
    tstart=time.time()
    pool=Pool(4)
    for i in range(3):
        for j in range(10):
            print "%s %s"%(i,j)
            pool.apply_async(decomp_predict,args=(i,j,labelist))

    pool.close()
    pool.join()
    print "Modular predict finished, using %s seconds"%(time.time() - tstart)
    result=[]
    for i in range(37786):
        result.append(labelist[0][i] or labelist[1][i] or labelist[2][i])
    TPR,FPR,TP,FN,FP,TN=rp.Result_Analy(result,y2)
    F1=rp.F1(TP,FN,FP,TN)
    acc = evaluations(y2, result)
    print "Accuracy is ", acc,'Percent'
    print 'More accurately TPR is :%s FPR is: %s F1 is : %s'%(TPR,FPR,F1)

