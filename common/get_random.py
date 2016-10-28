 #copy from http://www.cnblogs.com/hongten/p/hongten_python_random.html

import random

def get_random():
    '''get a random number.
    return Random float x, 0.0 <= x < 1.0'''
    return random.random()

def get_uniform(a, b):
    '''Return a random floating point number N such that
    a <= N <= b for a <= b and b <= N <= a for b < a.
    The end-point value b may or may not be included in the
    range depending on floating-point rounding in the
    equation a + (b-a) * random().
    '''
    return random.uniform(a, b)

def get_randrange(n):
    '''return an Integer from 0 to n
    and the number n must be greater than 0
    or n > 0
    '''
    return random.randrange(n)

def get_randrange_ex(start, stop, step):
    '''返回一个从start开始到stop结束，步长为step的随机数'''
    return random.randrange(start, stop, step)

def choice(s):
    '''从一个字符串中随机获取一个字符串，传入的参数s是不能为空或者不能为None'''
    if s != '' and s != None:
        return random.choice(s)
    else:
        print('the param is empty or equals None!')

def shuffle(items):
    '''对一个序列进行洗牌的操作'''
    random.shuffle(items)
    return items

def sample(items, n):
    '''从一个序列中随机抽出n个数，当然，在这n个数中，可能出现有重复的数'''
    return random.sample(items, n)

def main():
    r = get_random()
    print('获取一个0.0-1.0之间的随机数：{}'.format(r))
    r = get_uniform(2, 100)
    print('获取一个2.0-100.0之间的随机数：{}'.format(r))
    r = get_randrange(100)
    print('获取一个0-100之间的随机数：{}'.format(r))
    r = get_randrange_ex(3, 100, 25)
    print('获取一个3-100之间的随机数：{}'.format(r))
    tem_str = 'this is a test message!'
    r = choice(tem_str)
    print('从[{}]中随机取出一个字符：{}'.format(tem_str, r))
    tem_items = [1, 2, 3, 4, 5, 6, 7]
    tem_r = tem_items[:]
    shuffle(tem_items)
    print('对序列{}进行洗牌操作：{}'.format(tem_r, tem_items))

    tem_list = sample(tem_r, 3)
    print('从{}中随机抽出3个数：{}'.format(tem_r, tem_list))

if __name__ == '__main__':
    main()