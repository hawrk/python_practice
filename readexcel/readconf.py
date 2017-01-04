import configparser
import time

def read_conf():
    cf = configparser.ConfigParser()
    cf.read('mail.conf')

    cf.sections()
    #option = cf.options("mail")
    date = cf.get("mail","date")
    send_flag = cf.getint("mail","send_flag")

    print ('date =%s' %date)
    print ('send_flag = %d' %send_flag)
    return date,send_flag

def set_conf(curdate):
    cf = configparser.ConfigParser()
    cf.read('mail.conf')

    cf.set("mail","date",curdate)
    cf.set("mail","send_flag","0")
    cf.write(open("mail.conf","w"))


if __name__ == '__main__':
    confdate,send_flag  = read_conf()
    curdate = time.strftime('%Y%m%d', time.localtime(time.time()))
    if curdate != confdate:
        set_conf(curdate)

