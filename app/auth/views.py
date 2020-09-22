from flask import  render_template, url_for, request, flash, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from . import auth
from app.models import UserModel, UserData
from app.firestore_service import get_user, create_user
from werkzeug.security import generate_password_hash, check_password_hash




@auth.route('/login', methods=['POST', 'GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']    
        user_doc = get_user(email)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if check_password_hash(password_from_db, password):

                user_data = UserData(user_doc.to_dict()['name'], email, password)
                
                user = UserModel(user_data)

                login_user(user)

                flash(u'Bienvenido de nuevo!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Información no validad', 'error')
        else:
            flash('El usuario no existe!')
        
        return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        user ={
            'name': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password'],
            'confirm_password': request.form['confirm_password'],  
        }
        
        if len(user['password']) < 8:
            flash('La contraseña debe contener por lo menos 8 caracteres', 'error')

        elif user['password'] == None:
            flash('Contraseña no valida', 'error')

        elif user['password'] != user['confirm_password']:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('auth.register'))
        else:
            user_doc = get_user(user['email'])
            if user_doc.to_dict() is None:
                password_hash = generate_password_hash(user['password'])
                user_data = UserData(user['name'], user['email'], password_hash)
                create_user(user_data)

                user = UserModel(user_data)
                login_user(user)
                flash('Que bueno verte de nuevo!', 'success')

                return redirect(url_for('auth.login'))
            else:
                flash('El usuario ya existe', 'error')
            

    return render_template('register.html')



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto', 'success')

    return redirect(url_for('auth.login'))