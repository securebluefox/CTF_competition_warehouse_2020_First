#!/usr/bin/env python3
import re
import traceback
import seccomp
from os.path import join
from .loaddata import get_user, get_login, get_all_posts, get_posting, save_comment, user_create_entry, create_post_entry
import secrets
from uwsgidecorators import postfork
from flask import Flask, request, Response, redirect, abort, flash, escape, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename


@postfork
def start_seccomp():
    print("Starting up Seccomp")
    ALLOW = seccomp.ALLOW

    f = seccomp.SyscallFilter(defaction=seccomp.KILL)

    f.add_rule(ALLOW, "open")
    f.add_rule(ALLOW, "read")
    f.add_rule(ALLOW, "write")
    #   f.add_rule(ALLOW, "write", Arg(0, EQ, sys.stdout.fileno()))
    f.add_rule(ALLOW, "exit")
    #    f.add_rule(ALLOW, "rt_sigaction")
    f.add_rule(ALLOW, "brk")
    f.add_rule(ALLOW, "poll")
    f.add_rule(ALLOW, "futex")
    f.add_rule(ALLOW, "accept4")
    f.add_rule(ALLOW, "getsockname")
    f.add_rule(ALLOW, "clone")
    # required based on starting time
    f.add_rule(ALLOW, "stat")
    f.add_rule(ALLOW, "openat")
    f.add_rule(ALLOW, "fstat")
    f.add_rule(ALLOW, "ioctl")
    f.add_rule(ALLOW, "lseek")
    f.add_rule(ALLOW, "close")
    f.add_rule(ALLOW, "brk")
    f.add_rule(ALLOW, "socket")
    f.add_rule(ALLOW, "setsockopt")
    f.add_rule(ALLOW, "munmap")
    f.add_rule(ALLOW, "bind")
    f.add_rule(ALLOW, "uname")
    f.add_rule(ALLOW, "connect")
    f.add_rule(ALLOW, "listen")
    f.add_rule(ALLOW, "getpid")
    f.add_rule(ALLOW, "mmap")

    # afterr accept
    f.add_rule(ALLOW, "recvfrom")
    f.add_rule(ALLOW, "sendto")
    f.add_rule(ALLOW, "getrandom")
    f.add_rule(ALLOW, "shutdown")
    f.add_rule(ALLOW, "clock_nanosleep")
    f.add_rule(ALLOW, "epoll_wait")
    f.add_rule(ALLOW, "epoll_create")
    f.add_rule(ALLOW, "epoll_ctl")
    f.add_rule(ALLOW, "rt_sigaction")
    f.add_rule(ALLOW, "writev")
    # f.add_rule(ALLOW, "")
    f.add_rule(ALLOW, "getcwd")
    f.add_rule(ALLOW, "fcntl")
    f.add_rule(ALLOW, "mremap")
    f.add_rule(ALLOW, "readlink")
    f.add_rule(ALLOW, "lstat")
    f.add_rule(ALLOW, "getdents64")

    f.load()
    print("Seccomp startup complete")



app = Flask(__name__)

#app.config['SECRET_KEY'] = 'dogooo_secret_key_is_the_best22'

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
UPLOAD_FOLDER = '/app/present/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PORT = ""


def unauth_cb():
    return redirect(request.host_url[:-1] + "/dogooo/show?message=Only+authors+are+permitted+to+do+that")


login_manager = LoginManager()
login_manager.unauthorized_handler(unauth_cb)
login_manager.init_app(app)
login_manager.login_view = "login"


@app.errorhandler(Exception)
def all_exception_handler(error):
    message = [str(x) for x in error.args]
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }
    print(response)
    return jsonify(response)



# somewhere to login
@app.route("/dogooo/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_login(username, password)
        if user is not None:
            login_user(user)
            return redirect(request.host_url[:-1] + f"/dogooo/show?message=Welcom+back+{user.get_user_info()}")

        else:
            return redirect(request.host_url[:-1] + f"/dogooo/show?message=Login+FAILED")
    else:
        return abort(401)

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return get_user(userid)


@app.route("/dogooo/logout")
@login_required
def logout():
    logout_user()
    return redirect(request.host_url[:-1] + f"/dogooo/show?message=User Logged Out")


def get_header():
    header = open("/app/header.html", "r").read()
    if current_user.is_authenticated:
        header += "\n<script>$('#dogooo_login').hide();</script>"
    else:
        header += "\n<script>$('#dogooo_create').hide();$('#dogooo_logout').hide();$('#dogooo_user_create').hide()</script>"


    msg = request.args.get("message")
    if msg:
        header += f"\n<script>$('#message_panel').html('{msg}');</script>"
    else:
        header += f"\n<script>$('#message_panel').hide();</script>"
    return header

@app.route("/")
@app.route("/dogooo/show")
def display_posts():
    header = get_header()
    footer = open("/app/footer.html", "r").read()
    all_posts = []
    out = ""
    try:
        all_posts = get_all_posts()
        out = header + """
        <div class="container-fluid pt70 pb70">
            <div id="fh5co-projects-feed" class="fh5co-projects-feed clearfix masonry"> """
    except Exception as ex:
        print(ex)
        traceback.print_exc()

    # this is where extra fstring will go
    for p in all_posts:
        post = p

        try:
            out += f"""
                    <div class="fh5co-project masonry-brick">
                        <a href="/dogooo/deets/{p.id}">
                            <img src="/{p.pic_loc}" width=300 >
                            <h2>{p.message}</h2>
                        </a>
                    </div>\n"""
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    out += """
            </div>
        </div> 
        """ + footer

    return out

@app.route("/dogooo/runcmd", methods=["GET","POST"])
def run_cmd():
    cmd = request.form.get('cmd')
    if not cmd or cmd == "":
        cmd = "ls -la /tmp".split(" ")
    print(f"here {cmd}")
    import subprocess
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    print("STDOUT:")
    print(stdout)
    return stdout

@app.route("/dogooo/deets/<postid>", methods=["GET","POST"])
def display_post(postid):
    header = get_header()
    footer = open("/app/footer.html", "r").read()
    print(postid)

    p1 = get_posting(postid)
    comment = request.form.get('comment')
    commenter = request.form.get('commenter')

    if comment is None or commenter is None :
        comment = request.args.get("comment")
        commenter = request.args.get("commenter")
        if comment is None:
            comment = ""

        if commenter is None:
            commenter = ""

        add_comment_form = f"""
            <form action="/dogooo/deets/{postid}" method="POST">
                <textarea id="comment" name="comment" cols=60 rows=4 placeholder='Comment on the post'>{comment}</textarea><BR>
                <input type=text id="commenter" name="commenter" placeholder='Yourname' value='{commenter}' /><BR>
                <input type=submit value="Preview" />
            </form>
        """
    else:
        p1.add_comment(comment, commenter, True)
        add_comment_form = ""

    if p1 is None:
        return redirect(request.host_url[:-1] + f"/dogooo/show?message=Dog+Not+Found")
    out = header + f"""
    <div class="container-fluid pt70 pb70">
        <div id="fh5co-projects-feed" class="fh5co-projects-feed clearfix masonry" style="width: 600px">
            <img src="/{p1.pic_loc}" width=600 >
            
            <h3>{p1.message}</h3>
            <h1>Comments</h1>
            {p1.get_comments()}
            {add_comment_form}
        </div>        
    </div>
    """
    # r1 = Rating(1,2,"this is an event object")

    # r1.add_comment("cute doggo", "anon")
    out += footer

    return out

def valid_inp(inp):
    check_rex = re.compile(r'^[a-zA-Z0-9_\- .,?!@#$%^&*()+=~`\'"/\\]+$')
    return check_rex.match(inp)


@app.route("/dogooo/deets/add/<postid>", methods=["POST"])
def add_comment(postid):

    comment = request.form.get('comment')
    commenter = request.form.get('commenter')

    if not valid_inp(comment):
        return redirect(request.host_url[:-1] + f"/dogooo/deets/{postid}?message=Comment+is+invalid&comment={escape(comment)}&commenter={escape(commenter)}")

    if not valid_inp(commenter):
        return redirect(request.host_url[:-1] + f"/dogooo/deets/{postid}?message=Commenter+is+invalid&comment={escape(comment)}&commenter={escape(commenter)}")

    print(f"comment={comment}, commenter={commenter}")
    save_comment(postid, escape(comment), escape(commenter))

    return redirect(request.host_url[:-1] + f"/dogooo/deets/{postid}?message=Comment Saved")


@app.route("/dogooo/user/create", methods=["GET"])
@login_required
def user_create_form():
    header = get_header()
    footer = open("/app/footer.html", "r").read()
    username = request.form.get('username')
    username = f"value='{username}'" if username is not None else ""
    password = request.form.get('password')
    password = f"value='{password}'" if password is not None else ""
    html = f"""{header}
    
            <div id="create_user"> <div class="login1" >
                <div class="container-login1">
                    <form class="login1-form validate-form" action="/dogooo/user/create" method="POST">
                        <div class="wrap-input1 validate-input" data-validate = "Name is required">
                            <input class="input1" type="text" name="username" placeholder="Username" value="{username}">
                            <span class="shadow-input1"></span>
                        </div>

                        <div class="wrap-input1 validate-input" >
                            <input class="input1" type="password" name="password" placeholder="Password" value="{password}">
                            <span class="shadow-input1"></span>
                        </div>

                        <div class="container-login1-form-btn">
                            <input type="submit" value="Create User" class="login1-form-btn" />

                        </div>
                    </form>
                </div>
            </div></div>
            <script>document.getElementById('create_user').style.display = 'block'</script>
            {footer}
    """
    return html


@app.route("/dogooo/user/create", methods=["POST"])
@login_required
def user_create():

    username = request.form.get('username')
    password = request.form.get('password')
    if len(password) < 8:
        return redirect(request.host_url[:-1] + f"/dogooo/user/create?username={username}&password={password}&message=Password+is+too+short")
    user_create_entry(username, password)
    return redirect(request.host_url[:-1] + f"/dogooo/show?message=User+Created")


@app.route("/dogooo/create",  methods=["POST","GET"])
@login_required
def create_post():

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.host_url[:-1] + f"/dogooo/show?message=No file part")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.host_url[:-1] + f"/dogooo/show?message=No selected file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            post_text = escape(request.form.get("post_text"))
            rating = escape(request.form.get("rating"))
            url_path = join("images", filename)
            if post_text is None or rating is None:
                return redirect(
                    request.host_url[:-1] + f"/dogooo/show?message=Create failed, post missing data")
            if not rating.isdigit():
                return redirect(
                    request.host_url[:-1] + f"/dogooo/show?message=Create failed, rating must be a number")
            create_post_entry(post_text, url_path, rating, current_user.id)

        return redirect(request.host_url[:-1] + f"/dogooo/show?message=Post Saved")

    else:
        header = get_header()
        posthtml = open("/app/savepost.html","r").read()
        footer = open("/app/footer.html", "r").read()
        return header  + posthtml + footer


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



if __name__ == "__main__":

    try:
        app.run(host='0.0.0.0', port=8081, debug=True)

    except KeyboardInterrupt:
        print("W: Ctrl-C received, stopping…")

        # s.close()
    except Exception as ex:
        print(ex)
        traceback.print_exc()
