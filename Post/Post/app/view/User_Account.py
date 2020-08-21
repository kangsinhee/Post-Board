from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)
from Post.app import app, db
from Post.app.models import User
from flask_jwt_extended import (
    JWTManager,
    get_jwt_claims,
    create_refresh_token,
    create_access_token,
    get_jwt_identity,
    jwt_required
)
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        Userid = request.form['Userid']
        password = request.form['password']
        try:
            user_info = User.query.filter_by(Userid = Userid).first()
            if user_info.Userid == Userid and user_info.check_password(password):
                session['userid'] = user_info.Userid
                return redirect(url_for('index'))
            else:
                return jsonify({
                    "msg": "Bad username or password"
                }), 401
        except:
            return jsonify({
                "msg": "Bad username or password"
            }), 401
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        Userid = request.form['Userid']
        password = request.form['password']
        nickname = request.form['nickname']
        newUser = User(Userid=Userid, password=password, nickname=nickname)
        db.session.add(newUser)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    user = session.get('userid', None)
    session.pop('userid', None)
    print("logout [ %s ]" % user)
    return redirect(url_for('index'))