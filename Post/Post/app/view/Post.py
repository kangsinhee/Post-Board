import os
import datetime
from flask import (
    render_template, request, redirect,
    url_for, session, jsonify
)
from werkzeug.utils import secure_filename
from Post.app.exception import AuthenticateFailed
from Post.app.extension import app, db
from Post.app.models import User, Post, Comment, C_comment, Files
from Post.app.util.Auth_Validate import Auth_Validate, check_Access_token, check_Refresh_token, extend_Access_token

@app.route('/', methods=['GET'])
def index():
    user = session.get('User', None)
    Page = request.args.get('page', type=int, default=1)
    List = Post.query.order_by(Post.uuid.desc())
    Post_list = List.paginate(Page, per_page=7)
    return render_template("index.html", post=Post_list, user = user)


@app.route('/post/<int:uuid>', methods=['GET', 'POST'])
def viewpost(uuid):
    user = session.get('User', None)
    post = Post.query.get(uuid)
    comment = Comment.query.filter_by(post_id = uuid).order_by(Comment.uuid.desc()).all()
    c_comment = C_comment.query.filter_by(post_id = uuid).order_by(C_comment.uuid.asc()).all()

    Previous = Post.query.filter(Post.uuid < post.uuid).order_by(Post.uuid.desc()).first()
    Next = Post.query.filter(Post.uuid > post.uuid).order_by(Post.uuid.asc()).first()

    if user != None:
        if request.method == 'POST':
            now = datetime.datetime.now()
            content = request.form['content']
            if content != '':
                comment = Comment(uuid, user, content, now)
                db.session.add(comment)
            else:
                return jsonify({
                    "msg": "Please fill all blanks"
                }), 401
            return redirect(url_for('viewpost', uuid=uuid))
    return render_template('Content.html',
                            user=user, post=post, comment = comment,
                            c_comment=c_comment, Previous=Previous, Next=Next)


@app.route('/add', methods=['POST', 'GET'])
@Auth_Validate
def add():
    Access_Token = check_Access_token()
    user = User.query.filter_by(Userid=Access_Token).first()
    if request.method == 'POST':
        now = datetime.datetime.now()
        title = request.form['title']
        content = request.form['content']
        file = request.files['file']

        if title != '' and content != '':
            UPLOAD_FOLDER_LOCATION = os.getenv("UPLOAD_FOLDER_LOCATION")
            file.save(UPLOAD_FOLDER_LOCATION + secure_filename(file.filename))

            post = Post(title, content, now, user.nickname)
            files = Files(Access_Token, UPLOAD_FOLDER_LOCATION + secure_filename(file.filename))
            db.session.add(post)
            db.session.add(files)
        else:
            return jsonify({
                "msg": "Please fill all blanks"
            }), 401
        return redirect(url_for('index'))
    return render_template('add.html', user=user)


@app.route('/post/<int:uuid>/edit', methods=['POST', 'GET'])
@Auth_Validate
def edit(uuid):
    user = session.get('User', None)
    post = Post.query.get(uuid)
    if user != post.writer:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            now = datetime.datetime.now()
            post.title, post.content = request.form['title'], request.form['content']
            post.created_at = now
            return redirect(url_for('viewpost', uuid = uuid))
    return render_template('edit.html', user=user, note=post)


@app.route('/post/<int:uuid>/delete', methods=['GET'])
@Auth_Validate
def delete(uuid):
    user = session.get('User', None)
    post = Post.query.get(uuid)
    comment = Comment.query.filter_by(post_id=uuid).all()
    c_comment = C_comment.query.filter_by(post_id=uuid).all()
    if user != post.writer:
        return redirect(url_for('login'))
    else:
        db.session.delete(post)
        for item in comment:
            db.session.delete(item)
        for item in c_comment:
            db.session.delete(item)
        return redirect(url_for('index'))