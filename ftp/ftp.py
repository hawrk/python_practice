__author__ = 'hawrk'
__date__ = '2016.08.01'

import ftplib
import os

def ftp_connect(host,username,password):
    ftp = ftplib.FTP()
    ftp.set_debuglevel(2)
    ftp.connect(host,21)
    ftp.login(username,password)
    return ftp

#notice the remotefile must be the absolute path,like /home/hawrk/testftp.txt
def ftp_upload(ftp,remotefile,localfile):
    bufsize = 1024
    fp = open(localfile,'rb')
    ftp.storbinary('STOR ' + remotefile,fp,bufsize )
    ftp.set_debuglevel(0)

    fp.close()
    print ('ftp up ok')

def ftp_download(ftp,remotefile,localfile):
    bufsize = 1024
    fp = open(localfile,'wb')
    ftp.retrbinary('RETR ' + remotefile,fp.write,bufsize)
    ftp.set_debuglevel(0)
    fp.close()

if __name__== '__main__':
    ftp  = ftp_connect('127.0.0.1','hawrk','root.123')
    ftp_upload(ftp,'/home/hawrk/testftp.txt','/home/hawrk/PycharmProjects/ftp/testftp.txt')

    ftp_download(ftp,'/home/hawrk/testftp.txt','/home/hawrk/download/testftp.txt')

    ftp.quit()