from flask import Flask, request, redirect, render_template, flash, session as login_session, Blueprint,url_for
from app.models import UserDetails
auth_bp = Blueprint("auth", __name__)
from app import db

# login
@auth_bp.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        
        password1 = request.form.get("password")
        email1 = request.form.get("email")

        user = UserDetails.query.filter_by(email = email1, password = password1).first()
        if user:
            login_session["user"] = user.name
            flash("You have logged in successfuly!", 'success')
            return redirect(url_for("task.view_post"))
        
        flash("Invalide details. Please check your email and password!", "denger")
        return render_template("login.html")
    
    return render_template("login.html")

# register
@auth_bp.route("/register", methods = ["POST", "GET"])
def register():

    if request.method == "POST":

        username = request.form.get("name")
        if username not in login_session:

            user = UserDetails.query.filter_by(name = username).first()

            if user:
                flash("Username alreday exists. Please select another username!", "denger")
                return render_template("register.html")

            password1 = request.form.get("password")
            password2 = request.form.get("cpassword")
            if password1 == password2:
                email = request.form.get("email")

                user_info = UserDetails(name = username, email = email, password = password1) 
                db.session.add(user_info)    
                db.session.commit()
                
                login_session["user"] = user_info.name
                flash("Your account has been created!", 'success')
                return redirect(url_for('task.view-post'))
            
            flash("Both passwords are not same", 'denger')
            return render_template("register.html")
        
        return redirect(url_for('auth.login'))
        
    return render_template("register.html")

    

# logout
@auth_bp.route("/logout", methods = ["POST", "GET"])
def logout():
    if "user" in login_session:
        login_session.pop("user")
        flash("Logged out sucessfuly!", "success")
        return redirect(url_for('task.view_post'))
    
    return redirect(url_for('auth.login'))

# account
@auth_bp.route("/user_account", methods = ["POST", "GET"])
def user_account():
    if request.method == "POST":

        up_name = request.form.get("name")
        up_email = request.form.get("email")
        username = login_session.get("user")

        user = UserDetails.query.filter_by(name = username).first()
        if user:
            user.name = up_name
            user.email = up_email
            db.session.commit()
            login_session["user"]=user.name
            flash("Your account has been updated", "success")
            return redirect(url_for('auth.user_account'))
        return render_template("account.html")
    
    pic = request.args.get("profilepic")
    username = login_session.get("user")
    user =UserDetails.query.filter_by(name = username).first()
    return render_template("account.html", userinfo = user, pic = pic)


# about   

@auth_bp.route("/about", methods = ["POST", "GET"])
def about():
    
    return render_template("about.html")


@auth_bp.context_processor
def inject_session():
    return dict(session=login_session)
