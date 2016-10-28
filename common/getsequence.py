__author__ = 'hawrk'
__date__ = '2016.10.28'

import shelve

def create_sequence():
    db = shelve.open('./sequence.db',flag = 'c',protocol=2,writeback=True)
    assert isinstance(db,shelve.Shelf)

    #插入序列号
    db['sequence'] = 1
    db.sync()  #立即写入文件中，防止程序崩溃内存中的数据消失

    print (db['sequence'])

    db.close()

def key_exist():
    s = shelve.open('./sequence.db')
    flag = 'sequence' in s
    s.close()
    return flag

def get_sequence(fill_size):
    if not key_exist():
        create_sequence()

    s = shelve.open('./sequence.db')
    try:
        sequence = int(s['sequence'])
        s['sequence'] = str(sequence + 1)
    finally:
        s.close()

    out_seq = str(sequence).zfill(fill_size)
    print ('get sequce:%s' %out_seq)
    return out_seq

if __name__ == '__main__':

    str_seq = get_sequence(6)

    print ('out str_seq = %s' %str_seq)

