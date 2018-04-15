## 关系型数据库中表的关系
### 一对多
考虑下面的代码
```python
from flask-sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)

# 配置app，实例化SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir + 'db.sqlite')
app.config['SECRECT_KEY'] = 'a secrect string'
db = SQLAlchemy(app)

# 定义模型
class Writer(db.Model):
    __tablename__ = writers
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    posts = db.relationship('Article',backref='writer')

class Article(db.Model):
    __tablename__ = articles
    id = db.Column(db.Integer,primary_key)
    title = db.Column(db.String(64))
    body = db.Column(db.String(2018))
    writer_id = db.Colum(db.Integer,db.ForeignKey('writers.id'))
```
1. 在Writer模型中，relationship()定义了两张表之间的关系：**第一个参数是子表模型名**，backref属性相当于在另一张表中也定义了一个相关关系，用于访问父表的模型。这样Writer实例通过posts属性可以访问所有与之相关的Article模型，返回一个关联Article组成的列表。Article实例通过writer属性可以访问对应的Writer模型。
2. 在Article模型中，writer_id属性被定义为外键，ForeignKey()函数的含义是其所在的列的值域应当被限制在另一个表的指定列的取值范围之内。  
**这里要说明:ForeignKey()函数的参数形式应为'表名.字段名'而不是'Model名.字段名'**  
3. 一对多关系中，在父表模型中定义db.relationship(),用于指出和子表的关系，在子表模型中定义db.ForeignKey指向父表。

如下例,在实例化Article模型时，由relationship反向定义的writer属性要传入与love_python对应的的Writer实例susan。这样就可以让love_python与susan两个实例关联起来。  
```python
susan = Writer(name=susan)
love_python = Article(title='love python',body='python is easy and elegant'，writer=susan)
```


**_关系型数据库是通过主键与外键确定两张表的关系的_**。比如
```python
w1 = Writer('Jack')
w2 = Writer('Mike')
a = Article('hello','world',writer=w1)、
b = Article('hi','i like python',writer=w1)
c = Article('haha','i like flask',writer=w2)
db.session.add_all([w1,w2,a,b,c])
db.session.commit()
print(w.posts) # 会访问a和b，而不访问c
```
**_当w查询posts时，sqlalchemy会从Article模型中寻找外键与w.id相同的实例_**并返回这些对象。  
### 多对一
多对一关系中模型的定义与一对多类似，但是要将ForeignKey定义在父表中，即多的一方。  
```python
class Writer(db.Model):
    __tablename__ = writers
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    article_id = db.Column(db.Integer,db.ForeignKey(articles.id)
    posts = db.relationship('Article',backref='writer')

class Article(db.model):
    __tablename__ = articles
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.String(2018))
```

### 一对一
要让两张表是一对一关系，定义模型方式类似于一对多。只需要在**一**的模型中其relationship()的uselist参数设为False。
对于多对一关系，要改成一对一关系也很简单，只要用backref()函数在**一**的一方定义一个关系，并且将urslist设为False即可。  
```python
class Writer(db.Model):
    __tablename__ = writers
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    article_id = db.Column(db.Integer,db.ForeignKey(articles.id)
    posts = db.relationship('Article',backref=db.backref('writer',uselist=False)
```

### 多对多
要定义两张表的多对多关系，这时候光用两张表就不够了。要引入第三张表。  
举个例子，现在要定义课程与学生之间的关系。由于一个课程对应多个学生，一个学生也对应对个课程，这时候就不再是简单的一对多或者多对一而是多对多关系了。为了解决这个问题，我们引入第三张表Reflection，这张表定义了学生的id，对应的课程id与学生选这门课程的时间。这样一来，如果我们想要知道小明选了什么课，只需要在Reflection中根据小明的id找出对应的课程id，再通过课程id在Class中找到对应课程就OK啦~同时，通过Reflection我们还可以知道小明在什么时候选了这门课。
```python
class Reflection(db.Model):
    __tablename__ = 'reflections'
    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('students.id'))
    class_id = db.Column(db.Integer,db.ForeignKey('classes.id'))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)
    classes = db.relationship('Reflection',backref=db.backref('students',lazy='joined'),lazy='dynamic')

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    student = db.relationship('Reflection',backref=db.backref('classes',lazy='joined'),lazy='dynamic')
```
值得一提的是，在定义Reflection中回引模型的属性时用了backref()方法，并且将回引属性定义为joined加载。joined加载会在调用Reflection的同时找出对应的Student模型和Class模型，换言之，此时Reflection中的student和class直接指向对应的实例。这样就避免了selected加载导致的仅在调用Reflection.student或Reflection.class才加载相应模型。因为从数据库中加载模型是很耗费时间的，用joined一次就把所有模型都调用出来了，而selected需要调用多次，换言之，这样提高了效率。  
定义好的模型的关系，我们就可以试着进行操作了：  
先创建学生和课程实例
```python
Mike = Student(name='Mike',age=18)
English = Class(name='English')
db.session.add(Mike)
db.session.add(English)
db.session.commit()
```
将学生与课程之间的关系添加到Reflection中
```python
f = Reflection(students=Mike,classes=English)
db.session.add(f)
db.session.commit()
```
当我们想要查询学生的课程时，通过Student.classes获取到Reflection对象，再通过Reflection.class就可以查到该学生的课了。
```python
student = Student.query.filter_by(name='Mike').first()
classes = student.classes.class.all()
```
## 联结查询
在上面的例子中，我们为了获取学生的课程，执行了多次查询，这样的效率太低了，最好是一次就直接把结果查询出来。我们可以考虑把Class和Reflection结合起来，然后分别过滤Reflection中student_id与class_id，这样就得到一张包含了学生和相应课程的表。这种操作就叫做联结查询。
```python
class Student(db.Model):
    ......
    @property
    def getclass(self):
        return Reflection.query.join(Class,Class.id==Reflection.class_id).filter(Reflection.student_id==self.id)
```
下面对这行代码进行分析：
1. Reflection.query返回Reflection对象
2. join(Class,Class.id==Reflection.class_id) 联结Class与Reflection表，并且将Class.id与Reflection.class_id的值对应起来，相当于sql语句中的on
3. filter(Reflection.student_id==self.id) 对这张临时表进行过滤：只有Reflection.student_id与当前学生实例id相同的会留下来  

转换为sql语句是这样的：
```sql
select a.student_id,a.class_id,a.classes,a.students,a.timestamp,b.name,b.student from Reflection a join Class b on a.class_id=b.id where a.student_id=self.id
```
这样，我们就可以使用这样临时的表来获取想要的内容了。