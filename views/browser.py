from . import app
from flask import (render_template,
                   session,
                   redirect,
                   url_for,
                   request,
                   Flask,
                   send_from_directory)
from functools import wraps
import os,md5
from werkzeug import secure_filename
from datetime import timedelta, datetime
from models.usermodel import UserModel
from models.user_objects import *
from werkzeug import secure_filename

def login_required(func):
    """
    wrapper for login
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.has_key('user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('home'))
    return wrapper

@app.route('/')
def home():
    return render_template('master.html')

@app.route('/editprofile')
@login_required
def editprofile():
    return render_template('additionaldetails.html', user=session["user"])

@app.route('/saveadditional')
@login_required
def saveadditional():
    user_profile =  usr_profile()
    user_profile.school = request.args["txtschool"]
    user_profile.university = request.args["txtuniversity"]
    user_profile.job = request.args["txtjob"]
    model_object = UserModel()
    model_object.saveadditional(session["user"]["user_id"], user_profile)
    return redirect('/wall')

@app.route('/wall')
@login_required
def wall():
    model_object = UserModel()
    posts = model_object.get_posts(session["user"]["user_id"])
    msgs = model_object.get_messages(session["user"]["user_id"])
    requests = model_object.get_friend_requests(session["user"]["user_id"])
    return render_template('index.html', posts=posts, user = session["user"], requests=requests, msgs=msgs)


@app.route('/login', methods=["POST"])
def login():
    fields = users()
    model_object = UserModel()
    fields.email_id = request.form["txtusername"]
    fields.password = request.form["txtuserpassword"]
    if model_object.login(fields):
        return "1"
    return "0"

@app.route('/logout')
@login_required
def logout():
    session.pop("user")
    return redirect("/")

@app.route('/register', methods=["POST"])
def register():
    fields = users()
    model_object = UserModel()
    fields.first_name = request.form["txtfname"]
    fields.last_name = request.form["txtlname"]
    fields.email_id = request.form["txtemail"]
    fields.password = request.form["txtpassword"]
    model_object.register_user(fields)
    return "text"

@app.route('/profile/<user_id>')
@login_required
def profile(user_id):
    model_object = UserModel()
    user_data = model_object.get_profile(user_id)
    posts = model_object.get_user_posts(user_id, session["user"]["user_id"])
    user = session["user"]
    friendship = model_object.get_user_profile_relation(user["user_id"], user_id)
    frnds = model_object.get_user_friends(user_id, user["user_id"])
    return render_template("profile.html", posts=posts, user=user, user_data=user_data, friendship = friendship, frnds = frnds)

@app.route('/updateprofile', methods=["GET"])
@login_required
def updateprofile():
    model_object = UserModel()
    model_object.updateprofile(session["user"]["user_id"], request.args["column"], request.args["value"])
    session["user"][request.args["column"]] = request.args["value"]
    return ""
@app.route("/sendmessage", methods=["GET"])
def sendmessage():
    model_object = UserModel()
    model_object.sendmessage(request.args["to_id"], session["user"]["user_id"], request.args["msg"])
    return ""

@app.route('/search', methods=["GET"])
@login_required
def search():
    searchtext = request.args["query"]
    user = session["user"]
    model_object = UserModel()
    friends_list = []
    if "category" in request.args:
        if request.args["category"] == "1":
            results, friends_list = model_object.searchfriends(user["user_id"], searchtext)
            return render_template("friends-search.html", user=user, searchtext=searchtext, results=results)
        if request.args["category"] == "2":
            results = model_object.searchposts(user["user_id"], searchtext)
            return render_template("posts.html", user=user, searchtext=searchtext, posts=results)
        if request.args["category"] == "3":
            results = model_object.searchlocation(user["user_id"], searchtext)
            return render_template("posts.html", user=user, searchtext=searchtext, posts=results)
    results, friends_list = model_object.searchfriends(user["user_id"], searchtext)
    return render_template("search.html", user=user, searchtext=searchtext, results=results, friends = friends_list)


@app.route('/addfriend', methods=["GET"])
@login_required
def addfriend():
    objfriend_requests = friend_requests()
    objfriend_requests.to_id = request.args["profile_id"]
    objfriend_requests.from_id = session["user"]["user_id"]
    model_object = UserModel()
    request_id = model_object.addfriend(objfriend_requests)
    return str(request_id)

@app.route('/confirmfriend', methods=["GET"])
@login_required
def confirmfriend():
    objfriend_requests = friend_requests()
    objfriend_requests.request_id = request.args["request_id"]
    objfriend_requests.from_id = request.args["profile_id"]
    objfriend_requests.to_id = session["user"]["user_id"]
    model_object = UserModel()
    model_object.confirmfriend(objfriend_requests)
    return ""

@app.route('/decline', methods=["GET"])
@login_required
def decline():
    objfriend_requests = friend_requests()
    objfriend_requests.request_id = request.args["request_id"]
    objfriend_requests.from_id = request.args["profile_id"]
    objfriend_requests.to_id = session["user"]["user_id"]
    model_object = UserModel()
    model_object.declinefriend(objfriend_requests)
    return ""

@app.route('/unfriend', methods=["GET"])
@login_required
def unfriend():
    objfriends = friends()
    objfriends.user_id = request.args["profile_id"]
    objfriends.friend_id = session["user"]["user_id"]
    model_object = UserModel()
    profile_id = model_object.unfriend(objfriends)
    return str(profile_id)


@app.route('/cancelfriend', methods=["GET"])
@login_required
def cancelfriend():
    request_id = request.args["request_id"]
    model_object = UserModel()
    model_object.cancelfriend(request_id)
    return ""

@app.route('/changephoto', methods=["POST"])
@login_required
def changephoto():
    filename = upload_content(request.files['picupload'])
    model_object = UserModel()
    model_object.changephoto(filename, session['user']['user_id'])
    session["user"]["profile_pic"] = filename
    return filename

@app.route('/postcontent', methods=['POST'])
@login_required
def postcontent():
    objuser = user_post()
    user = session["user"]
    objuser.user_id = user["user_id"]
    objuser.content = request.form["txtcontent"]
    objuser.title = request.form["txttitle"]
    location = request.form["txtlocation"]
    if request.form["selectvisibility"]:
        objuser.visibility_id = request.form["selectvisibility"]
    if 'fileupload' in request.files:
        print "in"
        try:
            objuser.upload = upload_content(request.files['fileupload'])
        except Exception as ex:
            print str(ex)
    model_object = UserModel()
    post_id = model_object.postcontent(objuser, location)
    posts = []
    post = {"post_id" : post_id,
            "first_name" : user["first_name"],
            "last_name" : user["last_name"],
            "title" : objuser.title,
            "posted_when" : objuser.posted_when,
            "content" : objuser.content,
            "upload" : str(objuser.upload),
            "user_id": user["user_id"],
            "location" : location,
            "likes":{}}
    posts.append(post)
    return render_template("posts.html", posts = posts, user = session["user"])

@app.route('/likepost')
@login_required
def likepost():
    model_object = UserModel()
    like = likes_post()
    like.liked_by_id = session['user']['user_id']
    like.post_id = request.args["post_id"]
    print like
    likes = model_object.likepost(like)
    return str(likes)

@app.route('/unlikepost')
@login_required
def unlikepost():
    model_object = UserModel()
    like = likes_post()
    like.liked_by_id = session['user']['user_id']
    like.post_id = request.args["post_id"]
    likes = model_object.unlikepost(like)
    return likes

@app.route('/likecomment')
@login_required
def likecomment():
    model_object = UserModel()
    like = likes_comment()
    like.liked_by_id = session['user']['user_id']
    like.comment_id = request.args["comment_id"]
    likes = model_object.likecomment(like)
    return str(likes)

@app.route('/unlikecomment')
@login_required
def unlikecomment():
    model_object = UserModel()
    like = likes_comment()
    like.liked_by_id = session['user']['user_id']
    like.comment_id = request.args["comment_id"]
    likes = model_object.unlikecomment(like)
    return likes

@app.route("/comment")
@login_required
def comment():
    comment = comments()
    comment.content = request.args["comment"]
    comment.post_id = request.args["post_id"]
    comment.user_id = session["user"]["user_id"]
    model_object = UserModel()
    rowid = model_object.comment(comment)
    resp = '<div class="row" id="%s" style="background-color:#f5f5f5;">\
                <div class="col-md-6" style="padding-left:30px;">\
                    <a href="#" class="text-info">%s</a>&nbsp;&nbsp;&nbsp;&nbsp;\
                    %s &nbsp;&nbsp;&nbsp;&nbsp;<small><em class="text-warning">%s</em></small>\
                    <br>\
                    <small><a href="#" data-toggle="tooltip" data-html="true" href="#" data-original-title="" class="acommentlike" type="like">Like</a></small>\
                </div>\
            <br>\
            <hr>\
    </div>' %(rowid, session["user"]["first_name"], comment.content, comment.commented_when)
    return resp

def get_file_location(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as ex:
        print ex

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def upload_content(fileupload):
    try:
        if fileupload and allowed_file(fileupload.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(fileupload.filename)
            ext=filename.split('.')
            filename=secure_filename(session["user"]['first_name'] + "_" + str(datetime.now()) + "." + ext[len(ext)-1])
            fileupload.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename
    except Exception as ex:
        print str(ex)