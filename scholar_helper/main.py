#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-28 23:58:29
# @Author  : Kaiyan Zhang (kaiyanzh@outlook.com)
# @Link    : https://github.com/iseesaw
# @Version : 1.0
import os
import sys

from flask import Flask
from flask_bootstrap import Bootstrap
from flask import flash, redirect, url_for, render_template
from flask_moment import Moment

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret string'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

bootstrap = Bootstrap(app)
moment = Moment(app)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask import render_template


class HelloForm(FlaskForm):
    name = StringField('Article', validators=[DataRequired(), Length(1, 100)])
    submit = SubmitField()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

from scholar_helper import get_search_result
@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        #flash('Your message have been sent to the Server')
        # return redirect(url_for('index'))
        try:
            result = get_search_result(name)
        except:
            result = {
                "cites": [{"name": "", "body":""}],
                "title": "Something error"
            }
        messages = result["cites"]
        title = result["title"]
        return render_template('index.html', form=form, messages=messages, title=title)
    return render_template('index.html', form=form, messages=[{"name": "", "body":""}], title="Result")

if __name__ == '__main__':
    app.run(host="0.0.0.0")
