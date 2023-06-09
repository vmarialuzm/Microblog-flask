from flask import Blueprint,render_template,redirect,url_for,request,jsonify
from flask_login import current_user,login_required
from app.db import db
from app.models.posts import Post
from app.forms import PostForm,CommentForm
from app.utils.utils import Permission

post_router = Blueprint("post",__name__)

@post_router.route("/post", methods=["GET","POST"])
@login_required
def post():
    post_form=PostForm()

    if current_user.can(Permission.WRITE) and post_form.validate_on_submit():
        new_post = Post(body=post_form.body.data,user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index.index'))

    return render_template("post.html",post_form=post_form)

@post_router.route("/post/<id>")
def post_detail(id):
    comment_form = CommentForm()

    post=Post.query.filter_by(id=id).first()

    context = {
        "comment_form": comment_form,
        "post":post
    }

    return render_template("post-detail.html", **context)

@post_router.route("/api/post",methods=["POST"])
def api_post():
    #esta es la informacion que nos envia el cliente
    #recuerden que con .json transforma la data y puedo leerlo desde py
    #para este caso solo requiero 2 cosas body, user_id
    #{"body": "Texto del post","user_id": 1}
    client_post_information = request.json
    new_post=Post(body=client_post_information["body"],user_id=client_post_information["user_id"])
    db.session.add(new_post)
    db.session.commit()
    #nota: el estado de una creacion es 201:created
    return (jsonify(new_post.to_json(),201))