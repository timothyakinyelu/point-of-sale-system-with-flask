from flask import render_template, redirect, url_for, flash
from . import auth

@auth.route('/')
def index():
    return render_template('home.html')