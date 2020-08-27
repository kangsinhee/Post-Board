from flask import (
    render_template, request, redirect, url_for,
    session, jsonify
)
from Post.app import app, db
from Post.app.models import Post, User
from flask_jwt_extended import (
    JWTManager, create_refresh_token,
    create_access_token, get_jwt_identity, jwt_required
)
import re

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            Userid = request.form['Userid']
            password = request.form['password']

            user_info = User.query.filter_by(Userid = Userid).first()
            if user_info.check_password(password):
                session['userid'] = user_info.Userid
                accesstoken = create_access_token(identity = user_info.Userid)
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

@app.route('/delete_account', methods=['POST', 'GET'])
def delete_account():
    user = session.get('userid', None)
    user_info = User.query.filter_by(Userid=user).first()

    if request.method == 'POST':
        password = request.form['password']
        try:
            if user_info.check_password(password):
                post = Post.query.filter_by(writer=user_info.Userid).all()
                # 닉네임으로 수정 필요
                for posts in post:
                    posts.writer = '(알수없음)'

                db.session.delete(user_info)
                session.pop('userid', None)
                return redirect(url_for('index'))
            else:
                return jsonify({
                    "msg": "incorrect password"
                }), 401
        except:
            return jsonify({
                "msg" : "incorrect password"
            }), 401
    return render_template('exit.html', user = user_info.Userid)