from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
from functools import wraps
import jwt


# Environment variables
SECRET_KEY = 'super secret key' #  Used to decode cookies
EXPIRY_TIME = 60 * 60 #  1 hour


def required_cookie(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = payload.get('sub')
            if not current_user:
                return redirect(url_for('login'))
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))
        return function(current_user, *args, **kwargs)
    return decorated_function


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JWT_SECRET_KEY'] = SECRET_KEY

jwt_obj = JWTManager(app)


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/dashboard')
@required_cookie
def dashboard(current_user):
    return render_template('dashboard.html')


# User authentication
@app.route('/token', methods=['POST'])
def token():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    """ At this point we need to validate the user credentials
    trought a database or any other method. For this example we
    will use a trivial validation method.
    """
    if username != 'developer' or password != 'developer':
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=EXPIRY_TIME))
    response = jsonify({'message': 'Login successful'})
    # The property httponly=True also supports https protocol
    response.set_cookie('token', access_token, httponly=True, secure=True)
    return response


@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Se cerro la sesión exitosamente'})
    response.delete_cookie('token')
    return response


if __name__ == '__main__':
    app.run(debug=True)