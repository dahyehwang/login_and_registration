from system.core.controller import *
from flask.ext.bcrypt import Bcrypt

bcrypt = Bcrypt()

class Logins(Controller):
    def __init__(self, action):
        super(Logins, self).__init__(action)
        self.load_model('Login')
        self.db = self._app.db
   
    def index(self):
        return self.load_view('index.html')

    def user_info(self):
        data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_pw': request.form['confirm_pw']
        }

        create_status = self.models['Login'].add_user(data)
        if create_status['status'] == False:
            for message in create_status['errors']:
                flash(message)
            return redirect('/')
        else:
            session['first_name'] = request.form['first_name']
            return redirect('/success')

    def login(self):
        data = {
        'email': request.form['email'],
        'password': request.form['password']
        }
        user = self.models['Login'].validate_user(data)
        if bcrypt.check_password_hash(user[0]['password'], request.form['password']):
            session['email'] = user[0]['email']
            session['first_name'] = user[0]['first_name']
            session['last_name'] = user[0]['last_name']
            return redirect('/success')
        else:
            flash('Email and password are not matched. Try again!')
            return redirect('/')

    def success(self):
        return self.load_view('result.html')
