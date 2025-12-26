from flask import Flask, request, url_for, render_template, session as login_session, flash, Blueprint, redirect
from app.models import UserPost
from app import db

task_bp = Blueprint("task", __name__)

@task_bp.route("/")
def view_post():

    userpost = UserPost.query.all()
    return render_template("home.html",userpost = userpost)

@task_bp.route("/task_post", methods = ["POST", "GET"])
def task_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        user_post = UserPost(title = title, content = content)
        if user_post:
            db.session.add(user_post)
            db.session.commit()
            return redirect(url_for("task.view_post", user_post = user_post))
        
        flash("No post yest created. creat one!", "denger")
        return render_template("posts.html")
    
    return render_template("posts.html")
            