from flask import Blueprint

from flask_restful import Api

from Post.app.view import Post
from Post.app.view import User_Account
from Post.app.view import Comment

from Post.app.view.Post import Index, HelloWorld
from Post.app.view.User_Account import logout, register, logout, delete_account

Blueprint = Blueprint("Post", __name__, url_prefix="/")
Post_Api = Api(Blueprint)

Post_Api.add_resource(HelloWorld, "/")