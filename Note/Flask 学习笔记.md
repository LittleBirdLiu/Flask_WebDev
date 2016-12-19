# Flask 学习笔记

> Flask是一个小型的web框架，主要有两个依赖：一个是路由，调试，web服务器的网关接口，另一个是模板系统主要由Jinjia提供。
>
> Flask 不支持原生的数据库访问，web表单验证，以及用户认证等功能，这些功能都需要以扩展的形式构成，然后再与核心包集成。

------



## 虚拟环境

> 对于PYTHON中的虚拟环境很有用，为每一个项目创建不同的虚拟环境可以避免全局的包跟依赖混乱，版本冲突等问题。
>
> 方法如下:

```shell
sudo easy_install virtualenv

virtualenv --version 
#用来查看虚拟环境的版本

virtualenv venv
source venv/bin/activate
#用来激活虚拟环境

pip3 install flask
#安装flask
```

​	对于IDE， pycharm 有更方便的方法创建虚拟环境

![Screen Shot 2016-12-13 at 16.33.03](/Users/allen/Desktop/Screen Shot 2016-12-13 at 16.33.03.png)



------



## 程序基本结构

### 基本程序

```python
from flask import Flask

app = Flask(__name__)
@app.route('/')
#定义路由: (路由指的是程序需要知道每一个URL 对应的代码)
def index():
	return '<h1>Hello world</h1>'
#定义带参数的路由
@app.route('/user/<name>')
def User(name):
	return '<h1>Hellow %s</h1>' % name

if __name__ == '__main__':
	app.run(debug = True)


```

### 上下文

| 变量名         | 分类    | 用法                     |
| :---------- | ----- | ---------------------- |
| current_app | 程序上下文 | 用来说明当前的程序实例            |
| g           | 程序上下文 | 处理请求时候的用于临时存储的对象       |
| request     | 请求上下文 | 请求对象，封装了客户端发出的HTTP请求内容 |
| session     | 请求上下文 | 用户会话，用于存储请求之间需要记住的值的字典 |

[深入理解flask的上下文](https://segmentfault.com/a/1190000004859568)

> 在flask 分发请求之前 程序上下文 跟请求上下文会被激活，请求处理完成之后会再将其删除。程序上下文被推送之后，就可以使用current_app跟g两个变量，请求上厦门被推送之后就可以使用request跟session两个变量。

### 响应

大多数情况下响应就是一个简单的字符串，作为HTML页面返回给客户端

Flask 的响应码是200, 表示成功处理了一个响应

make_response: 返回一个Response 对象

redirect ： 表示重定向

```python
from flask import  Flask
from flask import make_response,redirect
app = Flask(__name__)

@app.route('/')
def index():
    response = make_response('<h1>the page carry a cookie</h1>')
    response.set_cookie('answer','42')
    
    return  redirect('http://www.baidu.com')

@app.route('/user/<name>')
def UserPage(name):
    return '<h1>Hello %s</h1>' % name



if __name__ == '__main__':
    app.run(debug= True)
```

### Flask 扩展

```python
from flask import  Flask
from flask import make_response,redirect
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
    
>>>

usage: index.py [-?] {runserver,shell} ...

positional arguments:
  {runserver,shell}
    runserver        Runs the Flask development server i.e. app.run()
    shell            Runs a Python shell inside Flask application context.

optional arguments:
  -?, --help         show this help message and exit
```

### Jinja2 模板引擎

> 模板是一个包含响应文本的文件，其中包含用占位变量表示的动态部分，其中具体值只有在请求的上下文中才能知道，然后用真实值替换掉变量，再返回相应的字符串，也就是HTML，这个过程就是渲染。

对于Flask 而言，采用的是一个叫做**Jinja2**的 模板引擎



#### 渲染模板

code:

```python
#我们需要引用render_template这个库去实现模板引擎。

from  flask import Flask, make_response, redirect,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name = name)


if __name__ == '__main__':
    app.run(debug= True)
```

需要注意的是：

- 默认情况下，程序会在文件夹下寻找**<u>templates</u>** 这个子文件件，所以我们要把所有的模板都放置在这个文件夹下面
- Flask 提供了render_template 函数来吧Jinja2模板引擎集成在程序中，所以我们必须引入这个库
- render_template 这个函数的第一个位置参数是所需要使用的html的名字，**<u>随后的参数都是键值对</u>**

> Jinja2 提供了多重控制结构可以来改变模板的渲染流程。

- 选择

```jinja2
{% if user %}
	hello {{ user }}
{% else %}
	Hello strange!
{% endif %}
```

- 循环

```jinja2
<ul>
	{% for comment in comments %}
		<li>{{ comment }}<\li>
	{% endfor %}
</ul>
```

- 宏 <==> 相当于函数

```jinja2
{% macro render_comment{comment} %}
	<li>{{ comment }}</li>
{% endmacro %}

<ul>
	{% for comment in comments %}
		{{ render_comment(comment) }}
	{% endfor %}
</ul>
```

```jinja2
{% import 'macros.html' as macros %} 
<ul>
 	{% for comment in comments %}
		{{ macros.render_comment(comment) }}
	{% endfor %} 
</ul>
```

> 需要在多处重复使用的模板代码片段可以写入单独的文件，再包含在所有模板中，以避免重复:

```
{% include 'common.html' %}
```

- **<u>模板继承</u>**

```jinja2
#base.html
<html>
<head>
	{% block head%}
	<title>{%block title%}{%endblock%} - My Application</title>
	{% endblock %}
</head>
	{%block body%}
	{%endblock%}
</html>
```

**如何继承base.html 呢， 关键语法： extends**

```jinja2
{% extends "base.html" %}
{% block title %}Index{% endtitle %}
{% block head %}
	[{supper()}]
	<style>
	</style>
{% endblock%}
{% block body %}
<h1>Hello world</h1>
{% endblock%}
```

[Jinja2 的中文文档](http://docs.jinkan.org/docs/jinja2/)

### 使用Bootstrap

> Bootstrap 是一个Twitter开发的一个开源框架，目标是客户端，不会操作到服务器部分。Server端只要做的事情就是提供应用了Bootstrap的 CSS 样式层跟JS文件的HTML 响应，并在HTML， CSS，js 代码中实例化所需要的组件。

- 安装

```shell
pip install flask-bootstrap	
```

​	安装之后，我们需要实例化bootstrap 对象。

```python
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
```



> 当我们实例化了bootstrap之后，我们基于可以在程序中使用一个包含了Bootstrap样式的文件的基模板。

```html
{% extends "bootstrap/base.html" %}
{% block title%}Flasky{% endblock %}
{% block navbar %}
<dir class = "navbar navbar-inverse" role="navigation">
  <div class = "container">
    <div class = 'navbar-header'>
      <button type = 'collapse' data-target='.navbar-collapse'>
        <span class = "sr-only">Toggle navigation</span>
        <span class = "icon-bar"></span>
        <span class = "icon-bar"></span>
        <span class = "icon-bar"></span>
      </button>
      <a class = "navbar-brand" href="/">Flasky</a>
    </div>
    <div class = "navbar collapse collapse">
      <ur class = "nav navbar-nav">
        <li><a href="/">Home</a></li>
      </ur>
    </div>
  </div>
</dir>
{% endblock %}

{% block content %}
<div class = "container">
  <div class = "page-header">
    <h1>Hell0, {{ name }}!</h1>
  </div>
  
</div>
{% endblock %}

```
- 使用Flask-Moment 本地化时间渲染 [Flask moment 介绍](http://www.tuicool.com/articles/ZZ3aiau)

> moment.js 是一个用js 开发的一个优秀的客户端代码库，用来在浏览器中渲染日期和时间。Flask-Moment 是一个Flask的程序扩展，能把moment.js集成到Jinja2 模板框架中。

==NOTE：==

- **Flask-Moment主要依赖有两个： 一个是moment.js 一个是jquery.js** 

> After that you have to include ==jquery.js== and ==moment.js== in your template(s). The template now has helper functions to make this easy:
>
> ```html
> <html>
> 	<head>
> 		<title>Flask-Moment example app</title>
> 		{{ moment.include_jquery() }}
> 		{{ moment.include_moment() }}
> 	</head>
> 	<body>
> 	...
> 	</body>
> </html>
> ```
>
> Note that you can include the scripts at the bottom of the page as well.

- **Bootstrap 已经引入了jquery.js，为了使用moment.js 我们还需要引入 moment.js 引入代码如下：**

> If you already have jquery included in your page then you can omit the ==include_jquery()==  line, ==but note that the `include_moment()` line must be present.==

```jinja2
{% block scripts %}
{{ super() }}
{{ moment.include_moment() }}
{% endblock %}
```

[moment.js 的详细文档](http://momentjs.com/)

[Flask-Moment 的开源代码](https://github.com/miguelgrinberg/Flask-Moment)

[Python datetime 包的文档](https://docs.python.org/2/library/datetime.html)

------



## 表单

### 介绍

- Flask-WTF 这是一个扩展，用来处理web 表单的。这个扩展对于WTForms包进行了包装，并将其集成到了flask框架
- 安装

```shell
pip install flask-wtf
```

- 跨站请求伪造保护

  [wiki:csrf](https://en.wikipedia.org/wiki/Cross-site_request_forgery)

  [中文介绍以及防护措施](http://www.ibm.com/developerworks/cn/web/1102_niugang_csrf/index.html)

  > CSRF（Cross Site Request Forgery, 跨站域请求伪造）是一种网络的攻击方式，该攻击可以在受害者毫不知情的情况下以受害者名义伪造请求发送给受攻击站点，从而在并未授权的情况下执行在权限保护之下的操作，有很大的危害性。

  在flask中防御csrf 可以设置一个密钥。flask-wtf会使用这个密钥生成加密令牌，在根据加密令牌验证请求中的表单数据是否是真的

  当我们post数据时候，会生成一个csrf token，如下

  ```shell
  csrf_token:1481775999##d274f971590511924c0eeea5c28e7f80394b8135
  name:allen
  submit:Submit
  ```

### WTF 使用

**相关代码如下：**

1. step 1， 编写表格的类

   **这个类是继承自FlaskForm这个父类，在这个类中可以定义所需要的的表单格式，在wtf中定义了HTML 支持的标准字段**

   | 字段类型                | 说明                        |
   | ------------------- | ------------------------- |
   | StringField         | 文本字串                      |
   | TextAreaField       | 多行文本字段                    |
   | PasswordField       | 密码文本字段                    |
   | HiddenField         | 隐藏文本字段                    |
   | DateField           | 文本，值是datetime.date的格式     |
   | DateTimeFiled       | 文本，值是datetime.datetime的格式 |
   | IntegerField        | 文本，值是整型                   |
   | DecimalField        | 文本，值是decimal.Decimal      |
   | FloatFiled          | 文本，值是浮点                   |
   | BoolenFiled         | 复选框，值是True Flase          |
   | RadioFiled          | 一组单选框                     |
   | SelectField         | 下拉列表                      |
   | SelectMultipleField | 下拉多选列表                    |
   | FileFiled           | 文件上传字段                    |
   | SubmitField         | 表单提交字段                    |
   | FormField           | 把表单当做字段潜入到另一个表单           |
   | FieldList           | 一组指定类型的字段                 |
   | **WTForms 验证函数**    |                           |

   | 验证函数        | 说明             |
   | ----------- | -------------- |
   | Email       | 验证是否是email 地址  |
   | EqualTo     | 比较两个字段是否一致     |
   | IPAddress   | 验证IPV4网络地址     |
   | NumberRange | 验证输入的值在某个数字范围中 |
   | Optional    | 无输入值是跳过其他验证函数  |
   | Required    | 确保字段中一定有值      |
   | Regexp      | 使用正则表达式去验证输入的值 |
   | URL         | 验证             |
   | AnyOf       | 确保输入的值在可选值列表中  |
   | NoneOf      | 确保输入的值不在可选列表中  |
   |             |                |

   ```python
   class PasswordForm(FlaskForm):
       name = StringField('What is your name', validators= [Required()])
       password = PasswordField('Please input your password',validators= [DataRequired()])
       inputAgain = PasswordField('Input again', validators=[Required(),EqualTo('password', message='Input not ok')])
       submit  = SubmitField('Submit')

   ```

2. 编写模板，调用wtf表单去渲染 wtf.quick_form

   ```html
   {% extends "base.html" %}
   {% import "bootstrap/wtf.html" as wtf %}
   {% block title %}SumbitForm{% endblock%}
   {% block page_content %}
   <div class="page-header">
       <h1>This is a sumbit form page,Hi  {%if name%}{{ name }}{% else %} Strange{%endif%}</h1>
       <p>{% if message %}{{ message }}{%else%}please set the password{% endif %}</p>
   </div>
   {{ wtf.quick_form(form1)}}
   {% endblock%}

   ```

3. 在视图函数中处理表单，需要在路由中添加post方法

   > 把 POST 加入方法列表很有必要，因为将提交表单作为 POST 请求进行处理更加便利。表单也可作为 GET 请求提交，不过 GET 请求没有主体，提交的数据以查询字符串的形式附加到URL 中，可在浏览器的地址栏中看到。基于这个以及其他多个原因，提交表单大都作为POST 请求进行处理。						

```python
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import  Required, EqualTo, DataRequired

class PasswordForm(FlaskForm):
    name = StringField('What is your name', validators= [Required()])
    password = PasswordField('Please input your password',validators= [DataRequired()])
    inputAgain = PasswordField('Input again', validators=[Required(),EqualTo('password', message='Input not ok')])
    submit  = SubmitField('Submit')

@app.route('/Submit', methods = ['GET','POST'])
def sumbitForm():
    PW_Form = PasswordForm()
    name_submit = None
    submitResult = PW_Form.validate_on_submit()
    password = PW_Form.password.data
    print(password)
    PasswordRes = PW_Form.validate_on_submit()
    message_PW  = None
    print(PasswordRes)
    print(submitResult)
    if PasswordRes :
        name_submit = PW_Form.name.data
        print(name_submit)
        PW_Form.name.data = ''
    if  submitResult:
        message_PW = 'Set password OK'
    return render_template('Form.html' ,
                           form1 = PW_Form,
                           name = name_submit,
                           message = message_PW)
```

[Flask-wtf 介绍](http://www.ttlsa.com/python/python-flask-wtf-and-wtforms/)

[别人的笔记 有关WTF](https://zhuanlan.zhihu.com/p/22495558#!)
### 重定向与用户会话

> 使用重定向作为 POST 请求的响应，而不是使用常规响应。重定向是一种特殊的响应，响应内容是 URL，而不是包含 HTML 代码的字符串。浏览器收到这种响应时，会向重定向的 URL 发起 GET 请求，显示页面的内容。这个页面的加载可能要多花几微秒，因为要先把第二个请求发给服务器。除此之外，用户不会察觉到有什么不同。现在，最后一个请求是 GET 请求，所以刷新命令能像预期的那样正常使用了。这个技巧称为 Post/ 重定向 /Get 模式。

> 但这种方法会带来另一个问题。程序处理 POST 请求时，使用 form.name.data 获取用户输入的名字，可是一旦这个请求结束，数据也就丢失了。因为这个 POST 请求使用重定向处理，所以程序需要保存输入的名字，这样重定向后的请求才能获得并使用这个名字，从而构建真正的响应

简而言之的就是，用这个重定向的方法，主要要调用的是一个叫做`url_for()`的方法， 因为redirection是传入一个url。



### Flask 消息

在flask中定义了一个flash函数用来发送一个消息，比如alert等

为了让用户知道状态发生了变化。这里包括确认消息，警告消息等。

code 如下：

```python
@app.route('/Submit', methods = ['GET','POST'])
def sumbitForm():
    PW_Form = PasswordForm()
    name_submit = None
    submitResult = PW_Form.validate_on_submit()
    password = PW_Form.password.data
    print(password)
    PasswordRes = PW_Form.validate_on_submit()
    message_PW  = None
    print(PasswordRes)
    print(submitResult)
    if PasswordRes and submitResult :
        session['name'] = PW_Form.name.data
        print(name_submit)
        PW_Form.name.data = ''
        message_PW = 'Set password OK'
        return redirect(url_for('sumbitForm'))
    if not PasswordRes and password is not None:
    #这里直接调用flash的方法，生成一个message   
    	flash('the password is not match , please check')
    return render_template('Form.html' ,
                           form1 = PW_Form,
                           name = session.get('name'),
                           message = message_PW)
```

仅仅这么做是没有办法在网页中显示的，还需要在模板中加入对应的样式来渲染这个结果。

> Flask 把 get_flash_messages()函数开放给了模板，用来渲染flash函数。

code：

```jinja2
{% block content%}
<div class = "container">
	{% for message in get_flashed_messages() %}
	<div class = "alert alert-warning">
		<button type = "button" class = "close" data-dismiss ="alert">&times;</button>
		{{ message }}
	</div>
	{% endfor %}
	{% block page_content %}{% endblock %}
</div>
{% endblock%}
```

> 在模板中使用的循环，是因为请求循环中每次调用 flash() 函数时都会生成一个消息，
> 所以可能有多个消息在排队等待显示。get_flashed_messages() 函数获取的消息在下次调
> 用时不会再次返回，因此 Flash 消息只显示一次，然后就消失了。

------



## 数据库

数据库是按照一定的规则保存数据的， 程序在发起查询取回所需的数据。

常用的是关系数据库，也叫作SQL数据库，近几年来用到的是文档数据库跟键值对数据库。

### Sql 数据库

[Sql 教程](http://www.w3school.com.cn/sql/sql_intro.asp)

> 关系型数据库把数据存储在表中，表模拟程序中不同的实体表中有个特殊的列，称为主键，其值为表中各行的唯一标识符。表中还可以有称为外键的列，引用同一个表或不同表中某行的主键。行之间的这种联系称为关系，这是关系型数据库模型的基础。



### NoSql 数据库

[Mango DB 介绍与教程](http://www.runoob.com/mongodb/mongodb-tutorial.html)

[Redis 教程](http://www.runoob.com/redis/redis-tutorial.html)

> Nosql 数据库是不遵守上述介绍的所有数据库的总和，对于NoSql而言，一般用集合来代替表，用文档代替记录。NOSql 这种方式使得联结变得异常困难，因此大部分NoSql数据库都不再支持联结这种方式。这种方式减少了表的数量，但增加了数据的重复性。
>
> 好处： 这种NoSql的方式使得查询速度变得很快
>
> 坏处：维护成本很高，也很耗时去更新文档

### Python中的数据库框架 - SqlAlchemy

- 使用的扩展 ： **<u>Flask-SqlAlchemy</u>**
- [SqlAlchemy 快速教程 官方](http://www.mapfish.org/doc/tutorials/sqlalchemy.html#engine-api)

| 数据库引擎        | URL                                      |
| ------------ | ---------------------------------------- |
| MySQL        | <u>*mysql://username:password@hostname/database*</u> |
| Postgres     | <u>*postgresql://username:password@hostname/database*</u> |
| SQLite(Unix) | <u>*sqlite:///absolute/path/to/database*</u> |

==Note: Sqllite 是在主机上的，不需要用户名 密码==

==Note：Mac 要将存放数据库的文件夹权限开放==

- 安装：

```shell
pip3 install flask-sqlalchemy
```

### 配置数据库

对于数据库的配置，我们需要指定数据库的URL 到Flask 对象中。另外在flask-sqlalchemy 中，有一个key是要求置为true的。

```python
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
```

配置完成之后，我们要实例数据库对象。

相关的code：

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:\\\'+ os.path.join(basedir, 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

```

### 创建模型

**==模型：==** 指的是在程序过程中使用的持久化实体。对于python而言。一个模型对应的是一个类，类中的属性就是这个数据表中的列

code：

```python
class User(db.Modle):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unqiue = True, index = True)
	
	def __repr__(self):
		return '<the Username is %s>' % self.username	
```

解释：

> - `__tablename__ `定义了模型所在的表名，习惯要求要用复数。
>
>
> - db.Column 是SqlAlchemy的一个实例方法，第一个参数是数据库列和模型属性的类型。常用的列类型如下：
>
> | 类型名          | python 类型          | 说明                   |      |
> | ------------ | ------------------ | -------------------- | ---- |
> | Integer      | int                | 整型                   |      |
> | SmallInteger | int                | 取值很小范围的整数，一般是16位     |      |
> | BigInteger   | int/long           | 不限精度的整数              |      |
> | Float        | float              | 浮点                   |      |
> | Numeric      | decimal.Decimal    | 定点数                  |      |
> | String       | str                | 定长字符                 |      |
> | Text         | str                | 不定长                  |      |
> | Unicode      | unicode            | 变长Unicode            |      |
> | UnicodeText  | unicode            | 变长Unicode ，对较长的字符有优化 |      |
> | Boolean      | bool               | 布尔                   |      |
> | Date         | datetime.date      | 日期                   |      |
> | Time         | datetime.time      | 时间                   |      |
> | DateTime     | datetime.datetime  | 日期时间                 |      |
> | Interval     | datetime.timedelta | 时间间隔                 |      |
> | Enum         | str                | 一组字符串                |      |
> | largeBinary  | str                | 二进制文件                |      |
> |              |                    |                      |      |
>
> - db.Column 中的其余参数设置
>
>   ==Flask-SQLAlchemy 要求每个模型都要定义主键，这一列经常命名为 id==
>
>   ​
>
> | 选项名         | 说明                         |
> | ----------- | -------------------------- |
> | primary_key | bool： 主键                   |
> | unique      | bool: 不允许出现重复的值            |
> | index       | bool: 为这一列创建索引             |
> | nullable    | bool:True,允许空值，False 不允许空值 |
> | default     | 为这列定义默认值                   |



### 建立关系

> 关系数据库使用关系来链接不同的表的不同行。 方法是
>
> `db.relationship('表名', **kwg)`

实际上就是外键的关系： [主键与外键](http://www.cnblogs.com/longyi1234/archive/2010/03/24/1693738.html)

| 选项名           | 说明                                  |
| ------------- | ----------------------------------- |
| backref       | 在关系中的另一个模型中添加反向应用                   |
| primaryjoin   | 明确两个模型之间使用的联结条件。只在模棱两可的关系中需要指定      |
| lazy          | 指定应该如何加载相关记录                        |
| uselist       | False 不使用列表，而是用标量值                  |
| order_by      | 指定关系中的记录的排序方式                       |
| secondary     | 指定多对多关系中关系表的名字                      |
| secondaryjoin | SQLAlchemy 无法自行决定时候，指定多对多关系中的二级联结条件 |



### 数据库操作

`db.create_all()`

> 创建数据库文件， 文件的名字就是在配置中指定的。

`db.drop_all()`

> 删除旧表

`db.session.add()`

`db.session.commit()`

> 添加行到数据库， add 方法也可以更新模型

`db.session.rollback()`

> 回滚数据库状态

`db.session.delete(xx)`

`db.commit()`

> 删除行

```python
Role.query_all()
Role.filter_by(role='xx').all()
Role.filter_by(role='xx').first()
```

> 查询操作是对模型类的。要查询具体的sql 语句可以直接转换类型即可str（）

###  在视图函数中操作

直接上code

```python
@app('/submit')
def SumbitForm():
	form = NameForm()
	if form.validate_on_submit():
		if User.query_filter_by(username = form.name.data).first() is None:
			db.session.add(User(username = form.name.data))
            db.session.commit()
            session['Known'] = False
        else:
            session['Known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                          name = session.get('name'),
                          known = session.get('Known'))

```



### 集成python shell <!--need read again-->



### 使用Flask-Migrate 实现数据库迁移 <!--need read again-->





## 电子邮件

- 库： flask-mail 或者 smtplib
- 安装: `pip3 install flask-mail`
- Flask smtp 服务器的配置

| 配置            | default value | explaination                             |
| ------------- | ------------- | ---------------------------------------- |
| MAIL_SERVER   | localhost     | 电子邮件服务器的主机 ip                            |
| MAIL_PORT     | 25            | 端口号                                      |
| MAIL_USE_TLS  | False         | 启用传输层安全协议                                |
| MAIL_USE_SSL  | False         | 启用[安全套接层协议](http://www.webstart.com/jed/papers/HRM/references/ssl.html) |
| MAIL_USERNAME | None          | 用户名                                      |
| MAIL_PASSWORD | None          | 密码                                       |

直接上code

```python
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SUBJECT_PREFIX'] = 'HELLO '
app.config['MAIL_SENDER'] = 'Allen <liu_heyu@126.com>'
# app.config['APP_ADMIN'] = os.environ.get('APP_ADMIN')
app.config['MAIL_USERNAME'] = 'liu_heyu@126.com'
app.config['MAIL_PASSWORD'] = '19910820'
app.config['APP_ADMIN'] = 'liu_heyu@126.com'

mail = Mail(app)

def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['MAIL_SENDER'], recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    # msg.html = render_template(template + '.html' , **kwargs)
    mail.send(msg)
    
    
@app.route('/Submit', methods = ['GET','POST'])
def sumbitForm():
    PW_Form = PasswordForm()
    name_submit = None
    password = PW_Form.password.data
    PasswordRes = PW_Form.validate_on_submit()
    message_PW  = None

    if PasswordRes  :
        user = User.query.filter_by(userName = PW_Form.name.data).first()
        print(User.query.all())
        print(user)
        if user is None:
            user = User(username= PW_Form.name.data)
            db.session.add(user)
            session['Known'] = False
            db.session.commit()
            print('APP ADMIN IS' + app.config['APP_ADMIN'])
            #这里需要注意的是 Mail 内容的模板是要定义在项目所在文件夹下 mail
            #子文件夹下面
            if app.config['APP_ADMIN']:
                send_mail(app.config['APP_ADMIN'],
                          'new user',
                          'mail/new_user',
                          user = user)

        else:
            session['Known'] = True
        session['name'] = PW_Form.name.data
        print(name_submit)
        PW_Form.name.data = ''
        message_PW = 'Set password OK'
        return redirect(url_for('sumbitForm'))
    if not PasswordRes and password is not None:
        flash('the password is not match , please check')
```

- 异步发送Mail

```python
def async_sendmail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['MAIL_SENDER'], recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    # msg.html = render_template(template + '.html' , **kwargs)
    thr = Thread(target= async_sendmail, args=[app, msg])
    return thr
```



**<u>*Note:*</u>**

> 不过要记住，程序要发送大量电子邮件时，使用专门发送电子邮件的作业要比给每封邮件都新建一个线程更合适。例如，我们可以把执行 send_async_email() 函数的操作发给 [Celery](http://www.celeryproject.org/)任务队列。						





## 程序结构

- [ ] 待总结



------

# 实战记录 - 个人博客

## 用户认证

大多数程序都会进行用户追踪，用户连接程序时候会进行身份认证，通过这一过程，让程序知道对方身份。

- Flask 的认证扩展

  - [Flask-Login](https://flask-login.readthedocs.io/en/latest/)： 管理已经登录用户的用户回话

  > Flask-Login provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users’ sessions over extended periods of time.
  >
  > Flask-Login 为flask 提供了一个用户session管理模块，他用来处理这种通用的的任务：登入，注销，记住一段时间的用户的session
  >
  > ```python
  > @app.route('/login', methods=['GET', 'POST'])
  > def login():
  >     # Here we use a class of some kind to represent and validate our
  >     # client-side form data. For example, WTForms is a library that will
  >     # handle this for us, and we use a custom LoginForm to validate.
  >     form = LoginForm()
  >     if form.validate_on_submit():
  >         # Login and validate the user.
  >         # user should be an instance of your `User` class
  >         login_user(user)
  >
  >         flask.flash('Logged in successfully.')
  >
  >         next = flask.request.args.get('next')
  >         # is_safe_url should check if the url is safe for redirects.
  >         # See http://flask.pocoo.org/snippets/62/ for an example.
  >         if not is_safe_url(next):
  >             return flask.abort(400)
  >
  >         return flask.redirect(next or flask.url_for('index'))
  >     return flask.render_template('login.html', form=form)
  >
  > ```

  - [Werkzeug](http://werkzeug.pocoo.org/): 计算密码散列值并进行核对

  > Werkzeug is a WSGI utility library for Python. It's widely used and BSD licensed.
  >
  > Werkzeug 是对python的一个工具集[WSGI](https://zh.wikipedia.org/wiki/Web%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%BD%91%E5%85%B3%E6%8E%A5%E5%8F%A3)库，它广泛的被使用并且[BSD](https://zh.wikipedia.org/wiki/BSD)认证

  - [itsdangerous](http://itsdangerous.readthedocs.io/en/latest/): 生成并核对加密安全令牌

  > 有时候你想向不可信的环境发送一些数据，但如何安全完成这个任务呢？解决的方法就是签名。使用只有你自己知道的密钥，来加密签名你的数据，并把加密后的数据发给别人。当你取回数据时，你就可以确保没人篡改过这份数据。

  ### 密码安全性

  > 要保证数据库中的用户密码安全，关键不在于存储密码本身，而在要存储密码的散列值。计算密码散列值的函数接收密码来作为输入，使用一种或者多种加密的方式来转换密码，最终得到一种跟原密码没有关系的密码。

  > 计算密码散列值是个复杂的任务，很难正确处理。因此强烈建议你不要自己
  > 实现，而是使用经过社区成员审查且声誉良好的库。如果你对生成安全密码
  > 散列值的过程感兴趣，“Salted Password Hashing - Doing it Right”(计算加盐
  > 密码散列值的正确方法，https://crackstation.net/hashing-security.htm)这篇文章值得一读。

  ### 使用Werkzeug 实现密码散列


- 实现密码散列值的计算，只需要实现两个函数：一个是在用户注册阶段，一个是在用户验证阶段

```python
#input string:password ; output string,hash value
generate_password_hash(password, method=pbkdf2:sha1, salt_length = 8):

#verfiy the password hash value
check_password(hash, password)
```

跟新User模块

```python
from werkzeug import generate_password_hash, check_password

...
def __init__(self, userName, password):
	self.userName = userName
	self.password = password
....

password_hash = db.Cloumn(db.String(128))

@property 
def password(self):
	rasie AttributeError('password can not be read')
	
@password.setter
def password(password):
	self.password_hash = genertate_password_hash(password)
	
def ver_password(password):
	return check_password(self.password_hash, password)
	
```

### 创建认证蓝本

> 蓝本的作用是在全局作用域中定义路由
>
> auth蓝本保存在同名python包下。蓝本的包构造文件创建蓝本对象，再从view.py模块中引入路由

**step1**: 创建蓝本的构造函数

```python
# __init__.py
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
```

**step2:** 建立视图函数

```python
#view.py

from flask import render_template
from . import auth

@auth.route('/login')
def login():
	return render_template('auth/login.html')	
```

**step 3:** 在全局的create_app函数中注册蓝本

```python
def create_app(config_name):
	...
	from auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='\auth')
	
	return app
```

