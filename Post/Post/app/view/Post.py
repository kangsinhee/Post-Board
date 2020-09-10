from flask import (
    render_template, request, redirect,
    url_for, session, jsonify, blueprints
)
from Post.app.extension import app, db, jwt
from Post.app.models import Post, Comment, C_comment
import datetime
from Post.app.util.token_checker import token_checker

@app.route('/', methods=['GET'])
def index():
    user = session.get('userid', None)
    Page = request.args.get('page', type=int, default=1)
    List = Post.query.order_by(Post.uuid.desc())
    Post_list = List.paginate(Page, per_page=7)
    return render_template("index.html", post=Post_list, user = user)

@app.route('/add', methods=['POST', 'GET'])
@token_checker
def add():
    user = session.get('userid', None)
    if user != None:
        if request.method == 'POST':
            now = datetime.datetime.now()
            nickname = session.get('userid', None)  #수정필요
            title, content = request.form['title'], request.form['content']
            if title != '' and content != '':
                post = Post(title, content, now, nickname)
                db.session.add(post)
            else:
                return jsonify({
                    "msg": "Please fill all blanks"
                }), 401
            return redirect(url_for('index'))
        return render_template('add.html', title='작성하기', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/post/<int:uuid>/edit', methods=['POST', 'GET'])
@token_checker
def edit(uuid):
    user = session.get('userid', None)
    post = Post.query.get(uuid)
    if user != post.writer:
        return redirect(url_for('login'))
    else:
        if request.method == 'DELETE':
            now = datetime.datetime.now()
            post.title, post.content = request.form['title'], request.form['content']
            post.created_at = now
            return redirect(url_for('index'))
    return render_template('add.html', user=user, title = "수정하기", note = post)

@app.route('/post/<int:uuid>/delete', methods=['GET'])
@token_checker
def delete(uuid):
    user = session.get('userid', None)
    post = Post.query.get(uuid)
    comment = Comment.query.filter_by(post_id=uuid).all()

    if user != post.writer:
        return redirect(url_for('login'))
    else:
        db.session.delete(post)
        for i in comment:
            db.session.delete(i)
        return redirect(url_for('index'))

@app.route('/post/<int:uuid>', methods=['GET', 'POST'])
@token_checker
def viewpost(uuid):
    user = session.get('userid', None)
    post = Post.query.get(uuid)
    comment = Comment.query.filter_by(post_id = uuid).order_by(Comment.uuid.desc()).all()

    Previous = Post.query.filter(Post.uuid < post.uuid).order_by(Post.uuid.desc()).first()
    Next = Post.query.filter(Post.uuid > post.uuid).order_by(Post.uuid.asc()).first()
    if user != None:
        if request.method == 'POST':
            now = datetime.datetime.now()
            userid = session.get('userid', None)
            content = request.form['content']
            if content != '':
                comment = Comment(uuid, userid, content, now)
                db.session.add(comment)
            else:
                return jsonify({
                    "msg": "Please fill all blanks"
                }), 401
            return redirect(url_for('viewpost', uuid=uuid))
    return render_template('Content.html', user=user, post=post, comment = comment, Previous=Previous, Next=Next)

@app.route('/post/<int:uuid>/<int:c_uuid>', methods=['POST', 'GET'])
@token_checker
def edit_comment(uuid, c_uuid):
    user = session.get('userid', None)
    comment = Comment.query.filter_by(uuid = c_uuid, post_id =  uuid).first()
    if user != comment.nickname:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            comment.content = request.form['content']
            return redirect(url_for('viewpost', uuid = uuid))
    return render_template('Edit_comment.html', user=user)

@app.route('/post/<int:uuid>/delete/<int:c_uuid>', methods=['GET'])
@token_checker
def delete_comment(uuid, c_uuid):
    user = session.get('userid', None)
    comment = Comment.query.filter_by(uuid = c_uuid, post_id =  uuid).first()
    if user != comment.nickname:
        return redirect(url_for('login'))
    else:
        db.session.delete(comment)
        return redirect(url_for('viewpost', uuid = uuid))