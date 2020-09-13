from flask import (
    render_template, request, redirect,
    url_for, session, jsonify, blueprints
)
from Post.app.extension import app, db, jwt
from Post.app.models import Post, Comment, C_comment
import datetime
from Post.app.util.Auth_Validate import Auth_Validate

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
    user = session.get('User', None)
    if user != None:
        if request.method == 'POST':
            now = datetime.datetime.now()
            title, content = request.form['title'], request.form['content']
            if title != '' and content != '':
                post = Post(title, content, now, user)
                db.session.add(post)
            else:
                return jsonify({
                    "msg": "Please fill all blanks"
                }), 401
            return redirect(url_for('index'))
        return render_template('add.html', user=user)
    else:
        return redirect(url_for('login'))

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

@app.route('/post/<int:uuid>/comment/<int:c_uuid>/edit', methods=['POST', 'GET'])
@Auth_Validate
def edit_comment(uuid, c_uuid):
    user = session.get('User', None)
    comment = Comment.query.filter_by(uuid = c_uuid, post_id =  uuid).first()
    if user != comment.nickname:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            comment.content = request.form['content']
            return redirect(url_for('viewpost', uuid = uuid))
    return render_template('Edit_comment.html', user=user)

@app.route('/post/<int:uuid>/comment/<int:c_uuid>/delete', methods=['GET'])
@Auth_Validate
def delete_comment(uuid, c_uuid):
    user = session.get('User', None)
    comment = Comment.query.filter_by(uuid = c_uuid, post_id = uuid).first()
    if user != comment.nickname:
        return redirect(url_for('login'))
    else:
        db.session.delete(comment)
        return redirect(url_for('viewpost', uuid = uuid))

@app.route('/post/<int:uuid>/<int:c_uuid>', methods=['POST', 'GET'])
@Auth_Validate
def c_comment(uuid, c_uuid):
    user = session.get('User', None)
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
    return render_template('Edit_comment.html', user=user)

@app.route('/post/<int:uuid>/c-comment/<int:c_uuid>/edit', methods=['POST', 'GET'])
@Auth_Validate
def edit_c_comment(uuid, c_uuid):
    user = session.get('User', None)
    comment = C_comment.query.filter_by(uuid = c_uuid, post_id = uuid).first()
    if user != comment.nickname:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            comment.content = request.form['content']
            return redirect(url_for('viewpost', uuid = uuid))
    return render_template('Edit_comment.html', user=user)

@app.route('/post/<int:uuid>/c-comment/<int:c_uuid>/delete', methods=['GET'])
@Auth_Validate
def delete_c_comment(uuid, c_uuid):
    user = session.get('User', None)
    comment = C_comment.query.filter_by(uuid = c_uuid, post_id =  uuid).first()
    if user != comment.nickname:
        return redirect(url_for('login'))
    else:
        db.session.delete(comment)
        return redirect(url_for('viewpost', uuid = uuid))
