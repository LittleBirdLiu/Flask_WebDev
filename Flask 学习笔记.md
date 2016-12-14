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

## 模板

### Jinja2 模板引擎





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