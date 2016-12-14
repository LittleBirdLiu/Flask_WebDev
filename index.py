from flask import  Flask
from flask import make_response,redirect, render_template
from flask_bootstrap import Bootstrap

from flask_script import Manager
app = Flask(__name__)
manager = Manager(app)
b_app = Bootstrap(app)

@app.route('/')
def index():
    response = make_response('<h1>the page carry a cookie</h1>')
    response.set_cookie('answer','42')

    return  render_template('index.html', var = 'hello')

@app.route('/user/<name_PY>')
def UserPage(name_PY):
    return render_template('User.html', name = name_PY)




if __name__ == '__main__':
    app.run()


