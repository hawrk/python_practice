

import collections

def py_deque():
    queue = collections.deque(["Eric","Jone","Michale"])
    queue.append("Terry")
    queue.append("Graham")

    print(queue.popleft())  #弹出Eric
    queue.popleft()  #弹出Jone

    print (queue)   #打印余下的元素

def py_set():
    a = set('abracadabra')
    b = set('alacazam')
    print ("a = ",a)
    print ("b =",b)
    print ("a-b = ",a-b)  #在a中但不在 b中
    print ("a|b =",a|b)   # 在a 中或者在b 中
    print ("a&b=",a&b)    #在a中并且在b中
    print ("a^b=",a^b)    #不能同时在a和b中，即 ^(a&b)

if __name__ == '__main__':
    py_deque()
    py_set()