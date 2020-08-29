from flask import (
    render_template, request, redirect,
    url_for, session, jsonify, blueprints
)
from Post.app.extension import app, db, jwt
from Post.app.models import Post, Comment
import datetime
from Post.app import view

@app.route('/', methods=['GET'])
def index():
    user = session.get('userid', None)
    post = request.args.get('page', type=int, default=1)
    post_list = Post.query.order_by(Post.uuid.desc())
    Post_list = post_list.paginate(post, per_page=7)
    return render_template("index.html", post=Post_list, user = user)

@app.route('/post/<int:uuid>', methods=['POST', 'GET'])
def viewpost(uuid):
    user = session.get('userid', None)
    post = Post.query.get(uuid)
    comment = Comment.query.filter_by(post_id = uuid).order_by(Comment.uuid.desc()).all()
    Previous = Post.query.filter(Post.uuid < post.uuid).order_by(Post.uuid.desc()).first()
    Next = Post.query.filter(Post.uuid > post.uuid).order_by(Post.uuid.asc()).first()

    if request.method == 'POST':
        now = datetime.datetime.now()
        nickname = session.get('userid', None)
        content = request.form['content']
        if content != '':
            comment = Comment(uuid, nickname, content, now)
            db.session.add(comment)
        else:
            return jsonify({
                "msg": "Please fill all blanks"
            }), 401
        return redirect((url_for('viewpost')))
    return render_template('Content.html', user=user, post=post, comment = comment, Previous=Previous, Next=Next)

@app.route('/add', methods=['POST', 'GET'])
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

@app.route('/edit/<int:uuid>', methods=['POST', 'GET'])
def edit(uuid):
    user = session.get('userid', None)
    post = Post.query.get(uuid)
    if user != post.writer:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            post.title, post.content = request.form['title'], request.form['content']
            return redirect(url_for('index'))
    return render_template('add.html', user=user, title = "수정하기", note = post)

@app.route('/delete/<int:uuid>', methods=['GET'])
def delete(uuid):
    user = session.get('userid', None)
    post = Post.query.get(uuid)
    if user != post.writer:
        return redirect(url_for('login'))
    else:
        post = Post.query.get(uuid)
        db.session.delete(post)
        return redirect(url_for('index'))