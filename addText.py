import pymysql
import os
from datetime import datetime
import bleach
import mistune

markdown = mistune.Markdown()
con = pymysql.connect(host='localhost',user='root',passwd='A19990701',db='blog',port=3306,charset='utf8mb4')
cur = con.cursor()
cur.execute('delete from Text where id between 1 and 10000')
path = r'C:\Users\86728\blog\post'
for file in os.listdir(path):
    with open(os.path.join(path,file),'r',encoding='utf-8') as f:
        content = f.read().strip()
        html = bleach.linkify(markdown(content))
        cur.execute('insert into Text values (null,%s,%s,%s,%s)',(file[:-3],content,html,datetime.utcnow()))
cur.close()
con.commit()
con.close()
