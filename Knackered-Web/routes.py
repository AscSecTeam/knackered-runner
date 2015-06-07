from flask import Flask, render_template, request, session
from beaker.middleware import SessionMiddleware
from flask.ext.login import LoginManager, UserMixin, login_required
from BeakerSessionInterface import BeakerSessionInterface
from User import User

app = Flask(__name__)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.data_dir': 'sessions/',
}

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET"])
def login():
    return render_template('login.html')

@app.route('/do-login', methods=["POST"])
def do_login():
    if 'user_id' not in session:
        if User.is_valid(request.form['username'], request.form['password']):
            session['user_id'] = 4
        else:
            return render_template('login.html')
    return render_template('index.html')

@app.route('/do-logout', methods=["GET"])
def do_logout():
    session.invalidate()
    return render_template('index.html')

@app.route('/configure', methods=["GET"])
def admin_config():
    return render_template('configure.html')

if __name__ == '__main__':
    app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
    app.session_interface = BeakerSessionInterface()
    app.run(port=5000, debug=True)
