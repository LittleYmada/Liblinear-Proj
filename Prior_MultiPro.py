import os,sys,re
sys.path.append('lib')
from multiprocessing import Pool,Manager,Lock
import os, time
from liblinearutil import *
import os
import FilePro as FP

def decomp_prior(a,b,label):
    print "Start process %s"%(os.getpid())
    filetrain="P/COMP/mxsub%s_%s"%(a,b)
    y,x=svm_read_problem(filetrain)
    prob=problem(y,x)
    #print y

    param=parameter('-s 3 -c 5 -q')
           #train
    p_labels,acc,p_values=predict(y2,x2,train(prob,param))
    print "sub process start min: %s"%(os.getpid())
    with lock[a]:
        for i in range(len(p_labels)):
    	    label[a][i]= label[a][i] and p_labels[i]
            
    #print label[a][0:100]
    print "$ ",len(p_labels)," $ ",len(y2)," $ ",len(x2)
    #return p_labels

if __name__=='__main__':
    labelist=[Manager().list([1 for xx in range(37786)]) for yy in range(4)]
    lock=[Lock() for xx in range(4)]
    filetest="Data/Utest.txt"
    y2,x2=svm_read_problem(filetest)

    t=time.clock()
    #print labelist
    pool=Pool(2)
    for i in range(4):
        for j in range(12):
            print "%s %s"%(i,j)
            a=pool.apply_async(decomp_prior,args=(i,j,labelist))


    pool.close()
    pool.join()
    print "Total time is ", time.clock()-t," s"
    result=[]
    for i in range(37786):
        result.append(labelist[0][i] or labelist[1][i] or labelist[2][i] or labelist[3][i])

    #print result[0:100]
    acc = evaluations(y2, result)
    print "Accuracy is ", acc
