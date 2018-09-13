from flask import render_template
from app import app
from app.input import RandomForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('/home.html', title='Home')
    return "Hello, World!"


@app.route('/random-commander')
def login():
    form = RandomForm()
    return render_template('random.html', title='Random Commander', form=form)