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
    user = session.get('userid', None)
    if user != None:
        if request.method == 'POST':
            now = datetime.datetime.now()
            user = session.get('userid', None)
            title, content = request.form['title'], request.form['content']
            post = Post(title, content, now, user)  #수정필요
            db.session.add(post)
            return redirect(url_for('index'))
        return render_template('add.html', title='작성하기')
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
            post.title = request.form['title']
            post.content = request.form['content']
            return redirect(url_for('index'))
    return render_template('add.html', title = "수정하기", note = post)

@app.route('/delete/<int:uuid>', methods=['GET'])
def delete(uuid):
    user = session.get('userid', None)
    owner = Post.query.filter_by(uuid=uuid).first()
    if user != owner.writer:
        return redirect(url_for('login'))
    else:
        post = Post.query.get(uuid)
        db.session.delete(post)
        return redirect(url_for('index'))
