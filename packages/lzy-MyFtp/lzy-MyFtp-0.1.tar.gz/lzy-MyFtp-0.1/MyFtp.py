from ftplib import FTP
from pathlib import Path

def MyFtp(*args,**kwargs):
    ftp = FTP()
    ftp.connect(*args)
    ftp.login(kwargs.get('username'), kwargs.get('password'))
    if kwargs.get('pattern') == 'w':
        with open(kwargs.get('file'),'rb') as f:
            ftp.storbinary(F"STOR {Path(kwargs.get('file')).name}",f)
            f.close()
    elif kwargs.get('pattern') == 'd':
        ftp.delete(kwargs.get('file'))
    ftp.quit()