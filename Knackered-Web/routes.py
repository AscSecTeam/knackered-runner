from flask import Flask, render_template, Response
from flask.ext.login import LoginManager, UserMixin, login_required
from User import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')

    if token is not None:
        user_entry = User.get(request.authorization.username)
        if user_entry is not None:
            user = User(user_entry[0], user_entry[1])
            if user.password == request.authorization.password:
                print user.password
                return user
    return None

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/configure', methods=["GET"])
@login_required
def admin_config():
    return render_template('configure.html')



if __name__ == '__main__':
    app.config["SECRET_KEY"] = "Does this even do anything?"
    app.run(port=5000,debug=True)