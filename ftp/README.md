notice :默认的ftp 服务 不开通上传功能 ，需要先行修改/etc/vsftpd.conf里面的文件 ，把 wirte_enable=YES前面的#去掉，使这行生效，然后重启ftp服务，service vsftpd restart 即可
