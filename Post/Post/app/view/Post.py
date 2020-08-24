from flask import render_template, request, redirect, url_for, session, jsonify
from Post.app import app, db, jwt
from Post.app.models import Post, User
import datetime
from Post.app import view

@app.route('/', methods=['GET'])
def index():
    user = session.get('userid', None)
    post = request.args.get('page', type=int, default=1)
    post_list = Post.query.order_by(Post.uuid.desc())
    Post_list = post_list.paginate(post, per_page=7)
    return render_template("index.html", post=Post_list, user = user)

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        now = datetime.datetime.now()
        user = session.get('userid', None)
        title, content = request.form['title'], request.form['content']
        post = Post(title, content, now, user)
        db.session.add(post)
        return redirect(url_for('index'))
    return render_template('add.html', title='작성하기')

@app.route('/edit/<int:uuid>', methods=['POST', 'GET'])
def edit(uuid):
    user = session.get('userid', None)
    if user == None:
        return redirect(url_for('index'))
    else:
        post = Post.query.get(uuid)
        if request.method == 'POST':
            user = session.get('userid', None)
            post.title = request.form['title']
            post.content = request.form['content']
            post.writer = user
            return redirect(url_for('index'))
    return render_template('add.html', title = "수정하기", note = post)

@app.route('/delete/<int:uuid>', methods=['POST', 'GET', 'DELETE'])
def delete(uuid):
    post = Post.query.get(uuid)
    db.session.delete(post)
    return redirect(url_for('index'))
