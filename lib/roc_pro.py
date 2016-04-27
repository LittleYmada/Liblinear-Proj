

def predict_threshold(p_values,threshold):
    p_labels=[]
    for i in p_values:
        if i<threshold:
            p_labels=p_labels+[0]
        else:
            p_labels=p_labels+[1]
    return p_labels

def Result_Analy(p_labels,t_labels):
    TP,FN,FP,TN=0,0,0,0
    for p, t in zip(p_labels, t_labels):
          if t==0:
              if p==t:
                  TN+=1
              else:
                  FP+=1
          else:
              if p==t:
                  TP+=1
              else:
                  FN+=1
    TPR=float(TP)/float(TP+FN)
    FPR=float(FP)/float(FP+TN)
    
    return TPR,FPR,TP,FN,FP,TN

def F1(TP,FN,FP,TN):
    if TP+FP==0:
	F1=1
        return F1
    p=float(TP)/float(TP+FP)
    r=float(TP)/float(TP+FN)
    F1=(2*r*p)/(r+p)
    return F1
