import os
import datetime
from flask import (
    render_template, request, redirect,
    url_for, jsonify, flash, Blueprint
)
from werkzeug.utils import secure_filename
from Post.app.extension import app, db
from Post.app.models import Post, Comment, C_comment, Files
from Post.app.util.Auth_Validate import Auth_Validate, Load_Token
from Post.app.exception import AuthenticateFailed, NotFound
from Post.config.app_config import allowed_file


@app.route('/', methods=['GET'])
def Index():
    try:
        Token = Load_Token('Access_Token')
        user = Token['nickname']
    except:
        user = None
    Page = request.args.get('page', type=int, default=1)
    List = Post.query.order_by(Post.uuid.desc())
    Post_list = List.paginate(Page, per_page=7)
    return render_template("index2.html", post=Post_list, user=user)


@app.route('/add', methods=['POST', 'GET'])
@Auth_Validate
def Add():
    try:
        Token = Load_Token('Access_Token')
        user = Token['nickname']
    except:
        user = None
    if request.method == 'POST' and Token != None:
        now = datetime.datetime.now()
        title = request.form['title']
        content = request.form['content']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url), 404
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_location = app.config['UPLOAD_FOLDER'] + '/' + user
        if title != '' and content != '':

            post = Post(title, content, now, user)
            db.session.add(post)
        else:
            return jsonify({
                "msg": "Please fill all blanks"
            }), 401
        return redirect(url_for('index'))
    return render_template('add.html', user=user)


Post_bp = Blueprint('post', __name__, url_prefix='/post')


@Post_bp.route('/<int:uuid>', methods=['GET', 'POST'])
def View_Post(uuid):
    try:
        Token = Load_Token('Access_Token')
        user = Token['nickname']
    except:
        user = None

    post = Post.query.get(uuid)
    comment = Comment.query.filter_by(post_id=uuid).all()
    c_comment = C_comment.query.filter_by(post_id=uuid) \
        .order_by(C_comment.uuid.asc()).all()

    Previous = Post.query.filter(Post.uuid < post.uuid) \
        .order_by(Post.uuid.desc()).first()
    Next = Post.query.filter(Post.uuid > post.uuid) \
        .order_by(Post.uuid.asc()).first()

    count = len(comment) + len(c_comment)

    if request.method == 'POST' and Token != None:
        now = datetime.datetime.now()
        content = request.form['content']
        if content != '':
            comment = Comment(uuid, Token['nickname'], content, now)
            db.session.add(comment)
        else:
            return jsonify({
                "msg": "Please fill all blanks"
            })
        return redirect(url_for('viewpost', uuid=uuid))
    return render_template('Content.html',
                           user=user, post=post, count=count, comment=comment,
                           c_comment=c_comment, Previous=Previous, Next=Next)


@app.route('/<int:uuid>/edit', methods=['POST', 'GET'])
@Auth_Validate
def edit(uuid):
    Token = Load_Token('Access_Token')
    if Token != None:
        post = Post.query.get(uuid)
        if Token['nickname'] != post.writer:
            return redirect(url_for('login'))
        else:
            if request.method == 'POST':
                now = datetime.datetime.now()
                post.title, post.content = request.form['title'], request.form['content']
                post.created_at = now
                return redirect(url_for('viewpost', uuid=uuid))
        return render_template('edit.html', user=Token['nickname'], note=post)
    else:
        raise AuthenticateFailed()


@app.route('/<int:uuid>/delete', methods=['GET'])
@Auth_Validate
def delete(uuid):
    Token = Load_Token('Access_Token')
    if Token != None:
        post = Post.query.get(uuid)
        comment = Comment.query.filter_by(post_id=uuid).all()
        c_comment = C_comment.query.filter_by(post_id=uuid).all()
        if Token['nickname'] != post.writer:
            return redirect(url_for('login'))
        else:
            db.session.delete(post)
            for item in comment:
                db.session.delete(item)
            for item in c_comment:
                db.session.delete(item)
            return redirect(url_for('index'))
    else:
        raise AuthenticateFailed()
