import os
import pymysql
import hashlib
import shutil
from PIL import Image

class Upload:
    def newAlbum(self,title,about):
        con = pymysql.connect(host='localhost', user='root', passwd='A19990701', db='blog', port=3306,
                              charset='utf8mb4')
        cur = con.cursor()
        cur.execute('insert into album values (null,%s,%s,default )',(title, about))
        cur.close()
        con.commit()
        con.close()

    def newPhotos_s(self,album_name,path):
        self.path = path
        con = pymysql.connect(host='localhost', user='root', passwd='A19990701', db='blog', port=3306,
                              charset='utf8mb4')
        cur = con.cursor()
        files = os.listdir(self.path)
        uri = os.path.abspath(os.path.join(os.getcwd() + '/app/static/', album_name+'_s'))
        os.makedirs(uri)
        for file in files:
            cur.execute('select id from album where title=%s', (album_name))
            album_id = cur.fetchone()
            filename, ext = file.split('.', 1)
            oldname = os.path.join(self.path, file)
            newname = hashlib.md5(filename.encode('utf-8')).hexdigest()[:10]+'.'+ext
            shutil.copyfile(oldname,os.path.join(uri,newname))
            img = Image.open(os.path.join(uri, newname))
            img = img.resize((1500, 840),Image.ANTIALIAS)
            img.save(os.path.join(uri, newname))
            cur.execute('insert into photos_s values (null,%s,%s)', (album_id[0], newname))
        cur.close()
        con.commit()
        con.close()

    def newPhotos_t(self,album_name,path):
        self.path = path
        con = pymysql.connect(host='localhost', user='root', passwd='A19990701', db='blog', port=3306,
                              charset='utf8mb4')
        cur = con.cursor()
        files = os.listdir(self.path)
        uri = os.path.abspath(os.path.join(os.getcwd() + '/app/static/', album_name+'_t'))
        os.makedirs(uri)
        for file in files:
            cur.execute('select id from album where title=%s', (album_name))
            album_id = cur.fetchone()
            filename, ext = file.split('.', 1)
            oldname = os.path.join(self.path, file)
            newname = hashlib.md5(filename.encode('utf-8')).hexdigest()[:10]+'.'+ext
            shutil.copyfile(oldname,os.path.join(uri,newname))
            img = Image.open(os.path.join(uri, newname))
            img = img.resize((1200, 400),Image.ANTIALIAS)
            img.save(os.path.join(uri, newname))
            cur.execute('insert into photos_t values (null,%s,%s)', (album_id[0], newname))
        cur.close()
        con.commit()
        con.close()

Upload = Upload()
#Upload.newAlbum('FordCar', '汽车是男人的浪漫')
Upload.newPhotos_s('GAME', r'C:\Users\86728\Pictures\GAME')
#Upload.newPhotos_t('FordCar', r'E:\壁纸\2018 GeigerCars Ford F-150（福特猛禽） Raptor EcoBoost HP520_t')