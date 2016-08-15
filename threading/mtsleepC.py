__author__= 'hawrk'
__date__ = '2016.08.15'

import threading
from time import ctime,sleep

loops = [4,2]

def loop(nloop,nsec):
    print ('start nloop ', nloop , 'at :', ctime())
    sleep(nsec)
    print ('end nloop ' , nloop , 'at' , ctime())

def main():
    print ('start at:' + ctime())

    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target=loop,args = (i,loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print ('all done at' + ctime())


if __name__ == '__main__':
    main()