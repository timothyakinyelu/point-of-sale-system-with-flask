from flask import render_template, redirect, url_for, flash
from . import nonAuth

@nonAuth.route('/login')
def login():
    return render_template('login.html')