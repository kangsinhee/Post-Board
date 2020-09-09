from flask import (
    render_template, request, redirect,
    url_for, jsonify, blueprints
)
from Post.app.extension import app, db, jwt
from Post.app.models import Post, User, Comment, Ben_list
from flask_jwt_extended import (
    JWTManager, set_refresh_cookies, create_refresh_token,
    set_access_cookies, create_access_token, get_jwt_identity, jwt_required
)
from Post.app.exception import AuthenticateFailed

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
            Userid = request.form['Userid']
            Passwd = request.form['password']
            try:
                user_info = User.query.get(Userid)
                if user_info.check_password(Passwd):
                    access_token = create_access_token(identity=Userid)
                    refresh_token = create_refresh_token(identity=Userid)

                    resp = jsonify({'login': 'True'})
                    set_access_cookies(resp, access_token)
                    set_refresh_cookies(resp, refresh_token)

                    return resp, 200
                else:
                    resp = jsonify({'login': 'False'})
                    return resp, 401
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


@app.route('/register-test', methods=['POST', 'GET'])
def register_test():
    if request.method == 'POST':
        Userid = request.form.get("Userid")
        password = request.form.get("password")
        nickname = request.form.get("nickname")
        
        ben_list = Ben_list.query.order_by(Ben_list.uuid.desc())
        for ben_list in ben_list:
            if nickname == ben_list.id:
                raise AuthenticateFailed()
        newUser = User(Userid=Userid, password=password, nickname=nickname)
        db.session.add(newUser)
        return redirect(url_for('login')), 301
    return render_template('register.html'), 200


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return redirect(url_for('index'))


@app.route('/delete_account', methods=['POST', 'GET'])
def delete_account():

    user_info = User.query.filter_by(Userid=user).first()

    if request.method == 'POST':
        password = request.form['password']
        try:
            if user_info.check_password(password):
                post = Post.query.filter_by(writer=user_info.Userid).all()
                comment = Comment.query.filter_by(nickname=user_info.Userid).all()
                # 닉네임으로 수정 필요
                for user in post:
                    user.writer = '(알수없음)'
                for user in comment:
                    user.nickname = '(알수없음)'

                db.session.delete(user_info)
                return redirect(url_for('index')), 301
            else:
                raise AuthenticateFailed()
        except:
            raise AuthenticateFailed()
    return render_template('exit.html', user = user_info.Userid)
