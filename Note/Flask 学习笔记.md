# Flask 学习笔记

> Flask是一个小型的web框架，主要有两个依赖：一个是路由，调试，web服务器的网关接口，另一个是模板系统主要由Jinjia提供。
>
> Flask 不支持原生的数据库访问，web表单验证，以及用户认证等功能，这些功能都需要以扩展的形式构成，然后再与核心包集成。

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