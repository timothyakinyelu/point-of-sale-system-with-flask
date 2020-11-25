from flask import render_template, redirect, url_for, flash, request
from . import nonAuth
from app.controllers import AuthController


@nonAuth.route('/login', methods=['GET', 'POST'])
def login():
    return AuthController.authenticate()

@nonAuth.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html')

