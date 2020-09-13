from flask import (
    render_template, request, redirect, make_response,
    url_for, jsonify, blueprints, session
)
from Post.app.extension import app, db, jwt
from Post.app.models import Post, User, Comment, C_comment
from Post.app.exception import AuthenticateFailed
from Post.app.util.Token_generator import decode_token
from Post.app.util.Cookie_generator import generate_cookie

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
            Userid = request.form['Userid']
            Passwd = request.form['password']
            try:
                user_info = User.query.get(Userid)
                if user_info.check_password(Passwd):
                    session.clear()
                    resp = make_response(redirect(url_for('index')))
                    Cookie = generate_cookie(resp)

                    session['User'] = user_info.nickname
                    Cookie.access_cookie(user_info.Userid)
                    Cookie.refresh_cookie(user_info.Userid)
                    return resp
                else:
                    raise AuthenticateFailed()
            except:
                raise AuthenticateFailed()

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        Userid = request.form.get("Userid")
        password = request.form.get("password")
        nickname = request.form.get("nickname")

        newUser = User(Userid=Userid, password=password, nickname=nickname)
        db.session.add(newUser)
        return redirect(url_for('login')), 301
    return render_template('register.html')


@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect(url_for('index')))

    Cookie = generate_cookie(resp)
    Cookie.delete_cookie()
    session.clear()

    return resp


@app.route('/delete_account', methods=['POST', 'GET'])
def delete_account():
    Access_cookie = request.cookies.get("Access_Token")
    Userid = decode_token(Access_cookie)
    user_info = User.query.filter_by(Userid=Userid).first()
    if request.method == 'POST':
        password = request.form['password']
        try:
            if user_info.check_password(password):
                post = Post.query.filter_by(writer=user_info.Userid).all()
                comment = Comment.query.filter_by(nickname=user_info.nickname).all()
                c_comment = C_comment.query.filter_by(nickname=user_info.nickname).all()
                for user in post:
                    user.writer = '(알수없음)'
                for user in comment:
                    user.nickname = '(알수없음)'
                for user in c_comment:
                    user.nickname = '(알수없음)'
                db.session.delete(user_info)
                session.clear()
                return redirect(url_for('index')), 301
            else:
                raise AuthenticateFailed()
        except:
            raise AuthenticateFailed()
    return render_template('exit.html', user=user_info.Userid)
