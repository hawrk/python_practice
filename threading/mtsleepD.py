__author__= 'hawrk'
__date__ = '2016.08.15'

import threading
from time import ctime,sleep

loops = [4,2]

class ThreadFun(object):
    def __init__(self,fun,args,name =''):
        self.fun = fun
        self.args = args
        self.name = name

    def __call__(self):
        self.fun(*self.args)


def loop(nloop,nsec):
    print ('start nloop ', nloop , 'at :', ctime())
    sleep(nsec)
    print ('end nloop ' , nloop , 'at' , ctime())


def main():
    print ('start at' + ctime())

    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target = ThreadFun(loop,(i,loops[i]),loop.__name__))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print ('end at '+ ctime())

if __name__ == '__main__':
    main()