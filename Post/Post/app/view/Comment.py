import datetime
from flask import (
    render_template, request, redirect,
    url_for, jsonify
)
from Post.app.extension import db
from Post.app.models import Comment, C_comment
from Post.app.util.Auth_Validate import Auth_Validate, Load_Token

# @app.route('/post/<int:uuid>/comment/<int:c_uuid>/edit', methods=['POST', 'GET'])
@Auth_Validate
def edit_comment(uuid, c_uuid):
    try:
        Token = Load_Token('Access_Token')
        user = Token['nickname']
    except:
        user = None
    comment = Comment.query.filter_by(uuid = c_uuid, post_id = uuid).first()
    if user != comment.nickname:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            comment.content = request.form['content']
            return redirect(url_for('viewpost', uuid = uuid))
    return render_template('Edit_comment.html', user=user, comment=comment)

#
# @app.route('/post/<int:uuid>/comment/<int:c_uuid>/delete', methods=['GET'])
@Auth_Validate
def delete_comment(uuid, c_uuid):
    try:
        Token = Load_Token('Access_Token')
        user = Token['nickname']
    except:
        user = None
    comment = Comment.query.filter_by(uuid = c_uuid, post_id = uuid).first()
    if user != comment.nickname:
        return redirect(url_for('login'))
    else:
        db.session.delete(comment)
        return redirect(url_for('viewpost', uuid = uuid))


# @app.route('/post/<int:uuid>/<int:c_uuid>', methods=['POST', 'GET'])
@Auth_Validate
def c_comment(uuid, c_uuid):
    try:
        Token = Load_Token('Access_Token')
        user = Token['nickname']
    except:
        user = None
    if user != None:
        if request.method == 'POST':
            now = datetime.datetime.now()
            content = request.form['content']
            if content != '':
                comment = C_comment(uuid, c_uuid, user, content, now)
                db.session.add(comment)
            else:
                return jsonify({
                    "msg": "Please fill all blanks"
                }), 401
            return redirect(url_for('viewpost', uuid=uuid))
    return render_template('Edit_comment.html', user=user, comment=None)


# @app.route('/post/<int:uuid>/c-comment/<int:c_uuid>/edit', methods=['POST', 'GET'])
@Auth_Validate
def edit_c_comment(uuid, c_uuid):
    try:
        Token = Load_Token('Access_Token')
        user = Token['nickname']
    except:
        user = None
    comment = C_comment.query.filter_by(uuid = c_uuid, post_id = uuid).first()
    if user != comment.nickname:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            comment.content = request.form['content']
            return redirect(url_for('viewpost', uuid = uuid))
    return render_template('Edit_comment.html', user=user, comment=comment)


# @app.route('/post/<int:uuid>/c-comment/<int:c_uuid>/delete', methods=['GET'])
@Auth_Validate
def delete_c_comment(uuid, c_uuid):
    try:
        Token = Load_Token('Access_Token')
        user = Token['nickname']
    except:
        user = None
    comment = C_comment.query.filter_by(uuid = c_uuid, post_id =  uuid).first()
    if user != comment.nickname:
        return redirect(url_for('login'))
    else:
        db.session.delete(comment)
        return redirect(url_for('viewpost', uuid = uuid))