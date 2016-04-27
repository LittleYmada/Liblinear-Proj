import io
import random
def file_to_svm(fname):
    flag=1
    num=0;
    try:
        fr=open(fname,'r')
        fw=open('U'+fname,'w')
        for line in fr:
            num=0
            for  ch in line:
                num+=1
                if ch==' ':
                    break
            if line[0]=='A':
                fw.write('1 '+line[num:])
            else:
                fw.write('0 '+line[num:])
    finally:

            fr.close()
            fw.close()
    return 'U'+fname

def random_spilit(fname,n,m):
    try:
        fr=open(fname,"r")
        f_1=list(range(n))
        f_0=list(range(m))

        for i in range(n):
            f_1[i]=open("A/sub"+str(i)+".txt","w")
        for i in range(m):
            f_0[i]=open("B/sub"+str(i)+".txt","w")
        for line in fr:
            if line[0]=='1':
                group=random.randint(0,n-1)
                f_1[group].write(line)
            else:
                group=random.randint(0,m-1)
                f_0[group].write(line)
    finally:
        fr.close()
        for i in range(n):
            f_1[i].close()
        for i in range(m):
            f_0[i].close()

def prior_spilit(fname):

    section=['A','B','C','D']
    classes=['0','1','2','3','4','5','6','7','8','9']
    #subclass=['A','B','C','D','E','F','G','H']
    try:
        fr=open(fname,"r")
        f_l1=list(range(4))
        for i in f_l1:
            f_l1[i]=open("P/"+section[i],"w")
        for line in fr:
            f_l1[section.index(line[0])].write(line)
        for i in range(4):
            f_l1[i].close()
        for i in range(4):
            f_l1[i]=open("P/"+section[i],"r")

        f_l2=[list(range(10)),list(range(10)),list(range(10)),list(range(10))]
        for i in range(4):
            for j in range(10):
                f_l2[i][j]=open("P/P"+section[i]+"/"+classes[j],"w")

        for i in range(4):
            for line in f_l1[i]:
                num = 0
                for ch in line:
                    num+=1
                    if ch==' ':
                        break
                temp = line.split()[0].split(',')
                flag=[0 for x in range(10)]
                for j in temp:
                    l2=int(j[1:3])/10
                    if flag[l2]==0 :
                        f_l2[i][l2].write(str(1-min(i,1))+' '+line[num:])
                        flag[l2]=1
    finally:
        fr.close()
        for i in range(4):
            f_l1[i].close()
        for i in range(4):
            for j in range(10):
                f_l2[i][j].close()

def compose_file(a,b,S1,S2,D):
    fp1=open(S1+"/"+str(a),"r")
    fp2=open(S2+"/"+str(b),"r")
    fpmx=open(D+"/mxsub%s_%s"%(a,b),"w")

    linesa=fp1.readlines()
    linesb=fp2.readlines()
    lena=len(linesa)
    lenb=len(linesb)
    lens=min(lena,lenb)
    i=0
    while(i<lens):

        fpmx.write(linesa[i])
        fpmx.write(linesb[i])
        i+=1
    if lens==lena:
        while(i<lenb):
            fpmx.write(linesb[i])
            i+=1
    else:
        while(i<lena):
            fpmx.write(linesa[i])
            i+=1

    fp1.close()
    fp2.close()
    fpmx.close()



def preconstruct():
    random_spilit("Utrain.txt",3,10)
    for i in range(3):
        for j in range(10):
            compose_file(i,j,'A','B','M')

def prior_construct():
    #prior_spilit('train.txt')
    for i in range(4):
        for j in range(12):
             compose_file(i,j,'P/1','P/0','P/COMP')




if __name__=='__main__':
    prior_construct()
