
from MySQLdb import connect
from fstring import fstring as f
from bleach import clean
import json
post_results = None

with open("/dbcreds.json","r") as jf:
    jdata = json.load(jf)
    db_user = jdata["db_user"]
    db_pass = jdata["db_pass"]


class Comment(object):
    def __init__(self, comment, commenter, preview=False):
        self.comment = comment
        self.author = commenter
        self.preview = preview

class Post(object):
    def __init__(self, id, message, rating, pic_loc):
        self.id = id
        self.rating = rating
        self._message = message
        self.pic_loc = pic_loc
        self.author = ""
        self.comments = list()

    @property
    def message(self):

        return self._message

    @message.setter
    def message(self, msg):
        self._message = msg

    def add_comment(self, comment, commenter, preview=False):
        self.comments.append(Comment(comment, commenter, preview))

    def get_comments(self):
        out = ""
        for ccnt, cmt in enumerate(self.comments):
            fmt_cmt = cmt.comment.format(rating=self.__dict__)
            form_save = f"""
                <form action="/dogooo/deets/add/{self.id}" method="POST">
                    <input type=hidden id="comment" name="comment" value='{fmt_cmt}'></textarea>
                    <input type=hidden id="commenter" name="commenter" value='{cmt.author}'/>
                    <input type=submit value="Save" />
                </form>
            """
            if cmt.preview:
                out += f"<ul class='square'>{fmt_cmt} - {cmt.author} {form_save} </ul>\n"
            else:
                out += f"<ul class='square'>{fmt_cmt} - {cmt.author}</ul>\n"

        return out


def get_posting(post_id):
    global post_results
    db = connect("127.0.0.1", db_user, db_pass, "dogdb")

    cursor = db.cursor()
    sql = """SELECT * FROM post, user
             WHERE fk_user_id = user.id  
             AND post.id = %s;"""
    cursor.execute(sql, (post_id,))
    post_results = cursor.fetchall()
    if len(post_results) == 0:
        return None
    else:
        pr = post_results[0]
        post = Post(id=pr[0], message=pr[1], rating=pr[3], pic_loc=pr[4])
        post.author = pr[6]

        sql = """SELECT * FROM comment  
                     WHERE fk_post_id = %s;"""
        comment_cursor = db.cursor()
        comment_cursor.execute(sql, (post_id,))
        comment_results = comment_cursor.fetchall()

        for row in comment_results:

            post.add_comment(comment=row[1], commenter=row[3])


    return post


from flask_login import UserMixin


def save_comment(postid, comment, commenter):
    db = connect("127.0.0.1", db_user, db_pass, "dogdb")
    if commenter.strip() == "":
        commenter = "anon"
    comment = clean(comment)
    commenter = clean(commenter)
    cursor = db.cursor()
    sql = """INSERT into comment (comment_text, fk_post_id,cname) VALUES(%s, %s, %s)"""

    cursor.execute(sql, (comment, postid, commenter))
    db.commit()


def get_all_posts():
    global post_results
    db = connect("127.0.0.1", db_user, db_pass, "dogdb")

    cursor = db.cursor()
    sql = """SELECT * FROM post  order by post.id DESC"""

    cursor.execute(sql)
    post_results = cursor.fetchall()
    posts = []
    if len(post_results) == 0:
        return None
    else:
        for row in post_results:
            posts.append(Post(id=row[0], message=row[1], rating=row[3], pic_loc=row[4]))

    return posts


def create_post_entry(post_text, filepath, rating, userid ):
    db = connect("127.0.0.1", db_user, db_pass, "dogdb")
    post_text = clean(post_text)

    cursor = db.cursor()
    sql = """INSERT into post (post_text, fk_user_id, rating, dog_pic) VALUES(%s, %s, %s, %s)"""

    cursor.execute(sql, (post_text, userid, rating, filepath))
    db.commit()


# silly user model
class User(UserMixin):

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.username, self.password)

    def get_user_info(self):
        return f(self.username)

def user_create_entry(username, password):
    db = connect("127.0.0.1", db_user, db_pass, "dogdb")

    cursor = db.cursor()
    sql = """INSERT into user (username, password) VALUES(%s, %s)"""

    cursor.execute(sql, (username, password))
    db.commit()



def get_login(username, password):
    db = connect("127.0.0.1", db_user, db_pass, "dogdb")

    cursor = db.cursor()
    sql = """SELECT * FROM user 
             WHERE username = %s AND password = %s """

    cursor.execute(sql, (username, password))
    user_results = cursor.fetchone()

    if user_results:
        return User(user_results[0], user_results[1], user_results[2])
    else:
        return None



def get_user(userid):
    db = connect("127.0.0.1", db_user, db_pass, "dogdb")

    cursor = db.cursor()
    sql = """SELECT * FROM user 
             WHERE id = %s """

    cursor.execute(sql, (userid, ))
    user_results = cursor.fetchone()

    if user_results:
        return User(user_results[0], user_results[1], user_results[2])
    else:
        return None






