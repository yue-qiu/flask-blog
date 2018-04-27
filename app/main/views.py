from . import main
from flask import render_template,redirect,url_for,request,session,request
import pymysql
import os
from .. import photos

@main.route('/')
def index():
    con = pymysql.connect(host='localhost',user='root',passwd='A19990701',db='blog',port=3306,charset='utf8mb4')
    cur = con.cursor()
    cur.execute('select * from Text where title=%s',('Flask学习'))
    talk = cur.fetchall()
    cur.execute('select * from Text where title=%s',('进程与线程'))
    book = cur.fetchall()
    cur.execute('select * from Text where title=%s',('一点感想'))
    python = cur.fetchall()
    cur.close()
    con.commit()
    con.close()
    return render_template('index.html',talk=talk,book=book,python=python)

@main.route('/text/<int:id>')
def text(id):
    con = pymysql.connect(host='localhost',user='root',passwd='A19990701',db='blog',port=3306,charset='utf8mb4')
    cur = con.cursor()
    if id == 0:
        cur.execute('select * from Text')
        posts = cur.fetchall()
        cur.close()
        con.commit()
        con.close()
        return render_template('post.html',posts=posts)
    else:
        cur.execute('select * from Text where id=%s',id)
        post = cur.fetchall()
        cur.close()
        con.commit()
        con.close()
        return render_template('text.html',post=post)

@main.route('/album')
def Album():
    con = pymysql.connect(host='localhost',user='root',passwd='A19990701',db='blog',port=3306,charset='utf8mb4')
    cur = con.cursor()
    cur.execute('select distinct * from album')
    albums = cur.fetchall()
    d = {}
    for album in albums:
        cur.execute('select url_t from photos_t where album_id=%s',album[0])
        urls = cur.fetchall()
        d[album] = [file for file in urls]
    return render_template('show.html',d=d)

@main.route('/album/<album_id>')
def photos(album_id):
    d = {}
    con = pymysql.connect(host='localhost',user='root',passwd='A19990701',db='blog',port=3306,charset='utf8mb4')
    cur = con.cursor()
    cur.execute('select url_s from photos_s where album_id=%s',album_id)
    urls = cur.fetchall()
    cur.execute('select title from album where id=%s',album_id)
    album = cur.fetchone()
    d[album[0]] = [file for file in urls]
    cur.close()
    con.commit()
    con.close()
    return render_template('photos.html',d=d)

@main.app_errorhandler(404)
def error1(e):
    return render_template('errors/404.html'),404

@main.app_errorhandler(500)
def error2(e):
    return render_template('errors/500.html'),500