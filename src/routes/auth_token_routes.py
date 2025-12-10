from flask import Blueprint

import controllers

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    return controllers.login()

@auth.route('/logout', methods=['POST'])
def logout():
    return controllers.logout()