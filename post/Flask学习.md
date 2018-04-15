# flask的4种请求钩子
有时在处理请求之前或者之后执行代码会很有用。例如：在请求开始时，我们可能需要创建数据库连接或者认证发起请求的用户，为了避免在每个视图函数中都有重复的代码，Flask提供了注册通用函数的功能，注册的函数可以在请求被分别发布到视图函数之前或之后自动调用。这种注册函数的功能就称之为“请求钩子”。
### @before_first_request
注册一个函数，在处理第一个请求之前执行。
### @before_request
注册一个函数，在每次请求之前执行。
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'hi'

@app.before_request
def hello():
    print('hello')
```
### @after_request
注册一个函数，如果没有未处理的异常抛出，在每次请求之后执行。
### @teardown_request
注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。
# flask的4种上下文全局变量
## 请求上下文(request context)
### request
请求对象，封装了客户端发出的HTTP请求中的内容。
```python
from flask import request,Flask,abort

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return 'hello'
    else:
        abort(404)
```
这段代码表示当客户端以GET的方式发送HTTP请求时，会返回hello，否则abort()会抛出一个404错误。
#### request获取HTTP请求内容的几种方式
1. request.method  
获取HTTP请求方式
2. request.form.get('name')  
获取form中的内容，当name不存在时返回None。(注意：用request.form['name']也可以把内容取出来，但是任何时候都不应该用这种危险的方式，因为当name不存在时会直接抛出错误，下文同理)
3. request.args.get('name')  
获取以查询字符串中的内容，当name不存在时返回None。
4. request.cookies.get('name')  
获取cookies中的内容，当name不存在时返回None。
5. request.headers.get('name')  
获取HTTP请求的header中的内容，当name不存在时返回None。
6. request.url/base_url/path/url_root
获取请求url相关内容，直接上结果方便理解：

```
return 'url: %s , path: %s , base_url: %s , url_root : %s' % (request.url,request.script_root, request.path,request.base_url,request.url_root)

#url: http://192.168.1.183:5000/testrequest?a&b ,path: /testrequest , base_url: http://192.168.1.183:5000/testrequest , url_root : http://192.168.1.183:5000/
```

### g
g：global。处理请求时用作临时存储的对象，**每次请求**都会**重设**这个变量。  
**g还常用于在请求钩子和视图函数之间共享数据**。例如：before_request处理程序可以从数据库中加载已登录用户并将其保存到g.user中，随后调用视图函数时，视图函数就可以直接使用g.user获取用户。
```python
from flask import Flask,g,request,render_templat,g

def login_log():
    print ('当前登录用户是：%s' % g.username)

def login_ip():
    print ('当前登录用户的IP是：%s' % g.ip)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/login/',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        g.username = username
        g.ip = password
        login_log()
        login_ip()
        return '恭喜登录成功！'

if __name__ == '__main__':
    app.run()
```
![](http://p1csf090h.bkt.clouddn.com/g.png)
## 程序上下文(app context)
### current_app
current_app，顾名思义这个变量表示当前激活的程序实例
```python
from flask import current_app,Flask

app = Flask(__name__)

@app.route('/test')
def index():
    return current_app.name
```
![](http://p1csf090h.bkt.clouddn.com/current_app.png)
### session
用户回话，用于存储请求直接需要“记住”的值的**字典**，其操作方式也与字典相似。当客户端关闭则session失效。
```python
from flask import Flask,session,url_for

app = Flask(__name__)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        return url_for('index')
    return """
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
"""

@app.route('/')
def index():
    if 'username' in session:
        return '%s 已经登录' % session['username']
    return '请登录'
```
# 蓝图
为了方便开发和调试，我们用蓝图将程序分成一些不同的部分。每一部分相互独立。通常同一部分的程序url都带有相同的前缀，如:
```
http://127.0.0.1/user/1和http://127.0.0.1/2
```
## 创建蓝图
在flask中，通过自带的blueprint函数就能注册一个创建一个蓝图：
```python
# !E:/web_develop/bp/__init__.py
from flask import blueprint

bp = blueprint('bp',__name__)

from . import views,errors
```
blueprint接受两个参数：第一个参数是这个蓝图的名字，第二个参数是蓝图所在文件或模块的名字，通常是__name__  
**注意：**我们在创建蓝图后导入bp的视图函数模块views和错误处理模块errors，这是因为这两个模块中都有这一句：
```python
from . import bp
```
这句话会从__init__.py中尝试导入bp，如果在创建bp前导入这两个模块，会出现循环调用的问题。
## 注册蓝图
蓝图创建好了之后，还要在分发函数中注册它：
```python
# !E:/web_develop/__init__.py
from flask import Flask
from .bp import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.register_blueprint(bp,url_prefix='/bp')
    ...
```
通过register_blueprint()函数就可以注册这个蓝图，url_prefix属性指定url前缀。
## 在蓝图中创建视图函数
在蓝图外，我们通常用:@app.route()注册视图函数，在蓝图内，我们用:@蓝图名.route()注册视图函数。如：
```python
@bp.before_app_request
def hello():
    print ('hello')

@bp.errorhandler(404)
def error(e):
    return 'Not Found',404

@bp.route('/hi')
def hi():
    return 'hi'
```
这样注册的函数的作用范围仅限于蓝图内。要让函数变得全局可用，我们要这样写：
```python
@bp.app_errorhandler(404)
def error(e):
    return 'Not Found',400

@bp.before_app_request
def hello():
    print('hello')
```