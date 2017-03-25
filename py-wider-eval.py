



import os
import numpy as np
import matplotlib.pyplot as plt
from tools import *
import datetime

DEBUG = False
eval_root = '/home/rick/Space/clone/py-faster-rcnn/data/WIDER_FACE_devkit/wider_eval_tools'

def get_eval_result():
    '''
        This will invoke matlab-wider-eval script to perform evaluation( will overwrite any previous result)
        And load result mat files into here, then return them
    '''


    import matlab.engine  # package install see: https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
    from mlabwrap import mlab  # package install see: http://mlabwrap.sourceforge.net/#installation
    # make sure 'matlab' executable is in your $PATH
    single, _ = make_dirs(mat_bak=True)
    current_pwd = os.getcwd()
    print "Current location: ", current_pwd
    if not DEBUG: mlab.path(mlab.path(), eval_root)
    os.chdir(eval_root)
    print "Executing matlab, Please wait..."
    if not DEBUG: mlab.my_wider_eval('./val')
    result_dir = os.path.join(os.getcwd(), 'plot/baselines/Val/setting_int/Ours')
    os.chdir(current_pwd)
    D = load_result_mat(result_dir,single)
    return D, current_pwd
    # D.keys():
        #['easy','medium','hard']
    # D['easy'][0] is: precision-recall curve points
    # D['easy'][1] is: legend name string

def main_plot(show=False):

    D, current_pwd = get_eval_result()


    # f= plt.figure()
    plt.ylim(0,1.05)
    lgs = []; aps=[]
    plt.xlabel("recall")
    plt.ylabel("Precision")
    plt.grid()
    for n,c in zip(['easy','medium','hard'],['g','orange','r']):
        pr = D[n][0]
        name = D[n][1]
        recall = pr[:,1]
        prec = pr[:,0]
        ap = VOCap(recall, prec); aps.append(ap)
        lg,=plt.plot(recall,prec,c,linewidth=3,label='{}({:.4f})'.format(n,ap))
        lgs.append(lg)

    plt.legend(handles=lgs,loc=3)
    fig = plt.gcf()
    if show:
        plt.show()
        plt.draw()
    single, timeline = make_dirs()
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    fig_name = "singlefigure-{:.4f}-{:.4f}-{:.4f}-{}.png".format(aps[0],aps[1],aps[2],now)
    fig_name = os.path.join(current_pwd,single,fig_name)

    fig.savefig(fig_name)

    print "\n\nPlot save to: {}".format(fig_name)

if __name__ == '__main__':
    DEBUG = True
    main_plot()