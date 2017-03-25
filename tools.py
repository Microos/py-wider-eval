import numpy as np
import scipy.io as sio
import os

def VOCap(rec,prec):
    mrec = np.insert(rec,0,0); mrec= np.append(mrec,1)
    mpre = np.insert(prec,0,0); mpre = np.append(mpre,0)
    for i in range(len(mpre)-2,-1,-1):
        mpre[i] = max(mpre[i],mpre[i+1])
    i = np.where(mrec[1:] != mrec[0:-1])[0]+1
    ap = sum( (mrec[i]-mrec[i-1]) * mpre[i] )
    return ap



def load_result_mat(result_dir):
    ret = {}
    names = [os.path.join(result_dir,f) for f in os.listdir(result_dir)]
    for n in names:
        mat = sio.loadmat(n)
        pr = mat['pr_cruve']
        if 'easy' in n: ret['easy'] = [pr,str(mat['legend_name'][0])+'-easy']
        if 'med' in n: ret['medium'] = [pr,str(mat['legend_name'][0])+'-medium']
        if 'hard' in n: ret['hard'] = [pr,str(mat['legend_name'][0])+'-hard']
    return ret


def make_dirs():
    single = './figures/single-result'
    timeline = './figures/timeline-result'
    os.system('mkdir -p {}'.format(single))
    os.system('mkdir -p {}'.format(timeline))
    return single, timeline