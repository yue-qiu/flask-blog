## 面向对象编程（OOP）
### 方法与函数
面向对象编程思想中，方法是指一个对象可以使用的函数，举个例子
```python
arr = [1,2,3]
arr.remove(2)
```
arr被定义为指向列表对象的变量，而remove则是list对象的一个方法，用于从列表中删除某个值。  
而函数则是对对象进行操作，例如
```python
arr = [1,2,3]
len(arr)
```
len()函数对其参数求长度。在本例中len()的参数既是一个列表。
### 一切皆对象
python一个很出名的特性是一切皆对象。比如变量，类，甚至函数也可以作为一个对象传给变量。比如：
```python
def plus(x,y):
    return x+y
plus(1,3)

from threading import Threat

if __name__ == '__main__':
    t = Threat(target=plus,args=(1,3,))
    t.start()
    t.join()
```
第八行的target参数传入的是plus函数的对象，此时不需要括号。而第三行的plus()加了括号是告诉python解释器执行这个函数对象。
## python常用的装饰器
python中的装饰器可以对函数进行扩展。
### @property
**@property装饰器可以把类的方法变成属性**。例如
```python
class Student():
    def __init__(self,score):
        self.score = score

#调用Student类
qiuyue = Student(90)
print(qiuyue.score) #输出结果90
```
可是这样也不无问题，比如当输入分数不合理（如1000）时，无法对分数进行检查。当然，可以对Student类附加方法实现检查分数。
```python
class Student():
    def get_score(self):
        return self._score

    def set_score(self,value):
        if not isinstance(score,int):
            raise ValueError('score must is an integer!')
        if value > 100 or value < 0:
            raise ValueError('score must between 0 to 100!')
        self._score = value

#调用Student类
qiuyue = Student()
qiuyue.set_score(90)
print(qiuyue.get_score()) #输出90        
```
通过set方法对Student的score属性赋值，再用get方法获取score属性。这样就可以实现对score合法性的检查。但是为了一个属性特地写两个方法未免过于繁琐。所以用到装饰器@property封装set方法和get方法，实现对score属性赋值的同时进行数值合法性检查。

```python
class Student():
    @property
    def score(self)
        return self._score

    @score.setter
    def score(self,value)
        if not isinstance(value,int):
            raise ValueError('score must is an integer!')
        if value > 100 or value < 0:
            raise ValueError('score must between 0 to 100!')    
        self._score = value

    @property
    def grade(self):
        if self._score is None:
            return None
        elif self._score >= 90:
            print('优秀！')
        elif self._score >=60:
            print('及格！)
        else:
            print('不及格！')

#调用Student类
qiuyue = Student()
qiuyue.score = 90
print(qiuyue.score) # 输出90
qiuyue.score = 1000 # 报错，ValueError
qiuyue.grade = '及格' # 报错
qiuyue.grade # 输出优秀
```
可以看到，@property装饰的第一个score，实际上是一个get方法，而@score.setter装饰的第二个score实际上是set方法。@score.setter其实是@property装饰器的副产品。这两个装饰器一个装饰get方法，一个装饰set方法，这样就使score方法变成了Student类的属性，在对score属性赋值（即set方法）时会自动对值的合法性进行检查，调用score属性即调用get方法。  
@grade.setter并不是必须的，当缺少@grade.setter装饰器时grade属性变成只读属性，无法对其进行赋值，只能读取。
### @classmethod与@staticmethod
在介绍类方法@classmethod与静态方法staticmethod前，先要清楚一个概念：类属性与实例属性是**不同**的。
```python
class Plus():
    num = 1

f = Plus()
f.num = 2

print(Plus.num) # 结果为2    
print(f.num) # 结果为1
```
众所周知，要调用类的方法，我们首先要把这个类实例化，然后通过*实例名.方法名*的方式调用。而@classmethod与@staticmethod都可以实现通过*类名.方法名*的方式调用方法。
#### @classmethod
当类中有些方法不需要涉及实例，而需要涉及类，如对类属性的修改，往往使用@classmethod。用@classmethod修饰的方法不会将实例传入方法中，而会自动将自身类作为第一个参数传入。所以这个方法不需要写self参数，但需要一个cls参数代表这个类。  
```python
class Apple():
    apple = 1
    @classmethod
    def how_much(cls):
        if cls.app == 1:
            print('还有一个苹果')

Apple.how_much() # 输出：还有一个苹果
```
#### @staticmethod
如果类中有些方法既不涉及类，也不涉及实例，可以用@staticmethod。@staticmethod既不会将实例传入方法，也不会将自身类传入方法。所以既没有self参数也没有cls参数。  
```python
class Apple():
    apple = 1
    def change(self,data):
        self.apple = data
        print('还有%s个苹果' % self.apple)

    @staticmethod
    def how_much():
        print('没有苹果了')

apple = Apple()
apple.change(2) # 输出：还有2个苹果
Apple.how_much() # 输出： 没有苹果了
```
下面这个例子加深区分：
```python
class Apple():
    num = 1
    def __init__(self,data):
        self.num = data

    def common(self):
        print('还有%s个苹果' % self.num)

    @classmethod
    def clsmed(cls):
        print('还有%s个苹果' % cls.num)

    @staticmethod
    def stamed():
        print('没有苹果了')

apple = Apple(2)
apple.common() # 输出：还有2个苹果
Apple.clsmed() # 输出：还有1个苹果
Apple.stamed() # 输出：没有苹果了
```
## Python的特点
像java，C#这种编译型语言，会将代码编译成二进制再运行。而python作为一种解释型语言，是**动态的逐行解释代码**的，也就是从脚本第一行开始，没有统一的入口。一个Python源码文件除了可以被直接执行外，还可以作为模块（也就是库）被其他.py文件导入。此时这个源码文件的文件名（不包括.py）就是库名。  
python本身有很多有趣的方法，会在每一个python文件里自动生成，在特殊情况下还会自动调用，这种方法称之为魔法方法。魔法方法的形式为两个下划线(\_\_)+方法名+两个下划线(\_\_)。如：\_\_new\_\_。下面介绍一些常见的魔法方法。  
### \_\_file__
通过下面一行代码，就能很直接地看出\_\_file__的作用。  
```python
# 文件位置为E:/python/test.py
print(__file__)
# 输出E:/python/test.py
```
可见，_\_file\_\_代表了当前python文件的路径。而且如前面所言，这个方法是python自动实现的，不需要你去编写。  
### \_\_name__
相信不少python初学者都见到过这样一段代码：
```python
if __name__ == "__main__":
    app.run()
```
可能很多人第一次看到这段代码的时候都会困惑：这个\_\_main\_\_我理解，是主函数的意思，可是这\_\_name\_\_是个什么东东？老规矩，上一段代码:
```python
# 文件位置为E:/python/test.py
print(__name__)
# 输出__main__
```
java，C等语言都会显示地定义一个main()函数，一个用C编写的程序都是以main()作为程序入口的。而python不同，哪个文件被直接执行，哪个文件的模块名就是\_\_main\_\_。现在说回\_\_name\_\_, \_\_name\_\_存放的就是当前python文件的名字，那么现在情况就很明显了，开头那段代码的意思是：如果这个文件是被直接运行的，就执行app.run()，如果这个文件是被别的文件导入后运行的，就会跳过app.run()。这样做的好处是避免了一些只能在主程序里执行的代码由于被导入了其他文件而错误执行。
## requirements.txt
在查看别人的python项目时，常会见到一个requirements.txt文件，主要是说明这个项目依赖的模块及其版本。我们可以用这个命令生成requirements.txt文件：
```
pip freeze > requirements.txt
```
要导入这个文件里指出的模块也很简单，只要用:
```
pip install -r requirements.txt
```
## is与==的区别
写代码的时候常常用is和==来比较两个对象是否相等，但是它们有什么不同呢？参考下面的例子：
```python
a = 1
b = 1
a == b # True
a is b # True

a = 888
b = 888
a == b # True
a is b # False

a = 'hello'
b = 'hello'
a is b # True
a == b # True

a = 'hello world'
b = 'hello world'
a == b # True
a is b # False
```
奇怪真奇怪！is和==的结果不同！不是说好的都是比较两个对象是否相等吗？怎么到这里变了样了？不急，先介绍一下python内置的一个函数：id()，这个函数会打印参数的内存地址，让我们来试试：
```python
a = 888
b = 888
id(a) # 1939743592336
id(b) # 1939745557808

a = 'hello world'
b = 'hello world'
id(a) # 1939745897200
id(b) # 1939745912624
```
可以看到，尽管a、b的值是相同的，但是其内存地址却不同。那么答案就很显然了，**is比较的是两个对象的内存地址是否相等，==比较的是两个对象的值是否相等**。这样就能解释为什么is和==的结果不同了。But wait，那么为什么当a、b的值为1和'hello'时，is与==的结果是一样的呢？这就要说到python的小整数池和垃圾回收机制了。python为了让运行速度快些，在内存中专门开辟了一块区域放置0到256，所有代表0到256的对象都会指向这个区域。类似的，python为短文本也开辟了这样的一块内存空间。所以这时is和==会得到相同的结果：
```python
a = 1
b = 1
id(a) # 1963327952
id(b) # 1963327952

a = 'hello' 
b = 'hello' 
id(a) # 1939745887600
id(b) # 1939745887600 
```