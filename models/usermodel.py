import MySQLdb, md5
from flask import session
from user_objects import *
class UserModel:
    def __init__(self):
        self.db = MySQLdb.connect(host="localhost",
                             user="root",
                              passwd="",
                              db="employee_network")

        self.runquery = self.db.cursor()

    def register_user(self, user):
        users_query = "insert into users(password,\
                                         first_name,\
                                         last_name,\
                                         email_id,\
                                         join_date,\
                                         friends_visibility_id,\
                                         post_visibility_id) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
                                        %(md5.md5(user.password).hexdigest(),
                                          user.first_name,
                                          user.last_name,
                                          user.email_id,
                                          user.join_date,
                                          user.friends_visibility_id,
                                          user.post_visibility_id)
        self.runquery.execute(users_query)
        self.db.commit()
        user.user_id = self.runquery.lastrowid
        user_data = {}
        user_data["user_id"] = user.user_id
        user_data["first_name"] = user.first_name
        user_data["last_name"] = user.last_name
        user_data["email_id"] = user.email_id
        user_data["current_location"] = user.current_location
        user_data["relationship_status"] = user.relationship_status
        user_data["date_of_birth"] = user.date_of_birth
        user_data["profile_pic"] = user.profile_pic
        user_data["friends_visibility_id"] = user.friends_visibility_id
        user_data["post_visibility_id"] = user.post_visibility_id
        session["user"] = user_data
        return None

    def saveadditional(self, user_id, user_profile):
        self.runquery.execute("insert into profile(user_id, school, university, job) values('%s', '%s', '%s', '%s')"%(user_id, user_profile.school, user_profile.university, user_profile.job))
        self.db.commit()
        return
    def updateprofile(self, user_id, column, value):
        update_query = "update users set %s = '%s' where user_id = '%s'" %(column, value, user_id)
        self.runquery.execute(update_query)
        self.db.commit()
        return ""

    def addfriend(self, friend_request):
        add_query = "insert into friend_requests(from_id, to_id, when_sent) values('%s', '%s', '%s')" %(friend_request.from_id, friend_request.to_id, friend_request.when_sent)
        self.runquery.execute(add_query)
        self.db.commit()
        return self.runquery.lastrowid

    def cancelfriend(self, request_id):
        add_query = "delete from friend_requests where request_id = '%s'" %request_id
        self.runquery.execute(add_query)
        self.db.commit()
        return ""

    def searchfriends(self, user_id, searchtext):
        search_query = "select user_id, first_name, last_name, email_id, current_location, date_of_birth, profile_pic from users where first_name like '%" + searchtext + "%' or last_name like '%" + searchtext + "%' and user_id <> '"+str(user_id)+"'"
        print search_query
        self.runquery.execute(search_query)
        data = self.runquery.fetchall()
        results = []
        for data_record in data:
          result = {}
          result["user_id"] = data_record[0]
          result["first_name"] = data_record[1]
          result["last_name"] = data_record[2]
          result["email_id"] = data_record[3]
          result["current_location"] = data_record[4]
          result["date_of_birth"] = data_record[5]
          result["profile_pic"] = data_record[6]
          result["friendship"] = self.get_user_profile_relation(user_id, data_record[0])
          results.append(result)
        friends_list = self.get_friends(user_id)
        return results, friends_list

    def changephoto(self, filename, user_id):
        update_query = "update users set profile_pic = '%s' where user_id = '%s'" %(filename, user_id)
        self.runquery.execute(update_query)
        self.db.commit()
        return ""
    
    def get_profile(self, user_id):
        profile_query = "select user_id,\
                              first_name,\
                              last_name,\
                              email_id,\
                              current_location,\
                              relationship_status,\
                              date_of_birth,\
                              profile_pic,\
                              friends_visibility_id,\
                              post_visibility_id, join_date from users where \
                              user_id = '%s'" %(user_id)
        self.runquery.execute(profile_query)
        data = self.runquery.fetchone()
        if data:
            user_data = {}
            user_data["user_id"] = data[0]
            user_data["first_name"] = data[1]
            user_data["last_name"] = data[2]
            user_data["email_id"] = data[3]
            user_data["current_location"] = data[4]
            user_data["relationship_status"] = data[5]
            user_data["date_of_birth"] = str(data[6])
            user_data["profile_pic"] = data[7]
            user_data["friends_visibility_id"] = data[8]
            user_data["post_visibility_id"] = data[9]
            user_data["join_date"] = data[10]
            return user_data

    def get_friend_requests(self, user_id):
        print user_id
        self.runquery.execute("select fr.request_id, fr.from_id, fr.to_id, us.first_name, us.last_name from friend_requests fr,users us where to_id = '%s' and us.user_id=fr.from_id"%user_id)
        results = self.runquery.fetchall()
        requests = []
        for result in results:
            request = {}
            request["request_id"] = result[0]
            request["from_id"] = result[1]
            request["to_id"] = result[2]
            request["first_name"] = result[3]
            request["last_name"] = result[4]
            requests.append(request)
        return requests

    def confirmfriend(self, friend_request):
        self.runquery.execute("delete from friend_requests where request_id = '%s'"%(friend_request.request_id))
        self.db.commit()
        self.runquery.execute("insert into friends(user_id, friend_id) values('%s', '%s')"%(friend_request.from_id, friend_request.to_id))
        self.db.commit()
        self.runquery.execute("insert into friends(user_id, friend_id) values('%s', '%s')"%(friend_request.to_id, friend_request.from_id))
        self.db.commit()
        return

    def declinefriend(self, friend_request):
        self.runquery.execute("delete from friend_requests where request_id = '%s'"%(friend_request.request_id))
        self.db.commit()
        return

    def unfriend(self, friend):
        self.runquery.execute("delete from friends where user_id = '%s' and friend_id = '%s'"%(friend.user_id, friend.friend_id))
        self.db.commit()
        self.runquery.execute("delete from friends where user_id = '%s' and friend_id = '%s'"%(friend.friend_id, friend.user_id))
        self.db.commit()
        return

    def get_user_profile_relation(self, user_id, profile_id):
        content = {}
        self.runquery.execute("select request_id from friend_requests where from_id = '%s' and to_id ='%s'"%(user_id, profile_id))
        data = self.runquery.fetchone()
        if data:
            content["friend_requests"] = { "request_id" : data[0] }

        self.runquery.execute("select request_id from friend_requests where from_id = '%s' and to_id ='%s'"%(profile_id, user_id))
        data = self.runquery.fetchone()
        if data:
            content["confirm_request"] = { "request_id" : data[0] }

        self.runquery.execute("select * from friends where user_id = '%s' and friend_id = '%s'"%(user_id, profile_id))
        data = self.runquery.fetchone()
        if data:
            content["unfriend"] = [1]
        return content

    def login(self, user):
        users_query = "select user_id,\
                              first_name,\
                              last_name,\
                              email_id,\
                              current_location,\
                              relationship_status,\
                              date_of_birth,\
                              profile_pic,\
                              friends_visibility_id,\
                              post_visibility_id from users where \
                              email_id = '%s' and \
                              password = '%s'" %(user.email_id, md5.md5(user.password).hexdigest())
        self.runquery.execute(users_query)
        data = self.runquery.fetchone()
        if data:
            user_data = {}
            user_data["user_id"] = data[0]
            user_data["first_name"] = data[1]
            user_data["last_name"] = data[2]
            user_data["email_id"] = data[3]
            user_data["current_location"] = data[4]
            user_data["relationship_status"] = data[5]
            user_data["date_of_birth"] = str(data[6])
            user_data["profile_pic"] = data[7]
            user_data["friends_visibility_id"] = data[8]
            user_data["post_visibility_id"] = data[9]
            session['user'] = user_data
            return True
        return False

    def searchposts(self, user_id, searchtext):
        friends_list = self.get_friends(user_id)
        in_list = "("
        for frnd in friends_list:
            in_list+=str(frnd[0])+","
        in_list = in_list[:-1]
        in_list+=")"
        posts_query = 'select distinct p.post_id, u.first_name, u.last_name, p.title, p.posted_when, p.content, p.upload, l.location_area, p.user_id from users u, user_post p, location_post l where p.post_id = l.post_id and p.user_id=u.user_id and match(p.title, p.content) against("%s") and p.user_id in %s order by posted_when DESC' %(searchtext, in_list)
        print posts_query
        self.runquery.execute(posts_query)
        data = self.runquery.fetchall()
        posts = []
        for item in data:
            post = {}
            post["post_id"] = item[0]
            post["first_name"] = item[1]
            post["last_name"] = item[2]
            post["title"] = item[3]
            post["posted_when"] = item[4]
            post["content"] = item[5]
            post["upload"] = item[6]
            post["location"] = item[7]
            post["user_id"] = item[8]
            post["likes"] = {}
            self.runquery.execute("select u.first_name, u.user_id from users u, likes_post l where l.liked_by_id = u.user_id and l.post_id = '%s'"%post["post_id"])
            likes = self.runquery.fetchall()
            for like in likes:
                post["likes"][like[1]] = like[0]
            post["comments"] = []
            self.runquery.execute("select c.comment_id, u.first_name, u.user_id, c.content, c.commented_when from users u, comments c where c.user_id = u.user_id and c.post_id = '%s'"%post["post_id"])
            comments = self.runquery.fetchall()
            for comment in comments:
              row = {}
              row["comment_id"] = comment[0]
              row["first_name"] = comment[1]
              row["user_id"] = comment[2]
              row["content"] = comment[3]
              row["commented_when"] = comment[4]
              row["likes"] = {}
              self.runquery.execute("select u.first_name, u.user_id from users u, likes_comment l where l.liked_by_id = u.user_id and l.comment_id = '%s'"%row["comment_id"])
              likes = self.runquery.fetchall()
              for like in likes:
                  row["likes"][like[1]] = like[0]
              post["comments"].append(row)
            posts.append(post)
        return posts

    def searchlocation(self, user_id, searchtext):
        friends_list = self.get_friends(user_id)
        in_list = "("
        for frnd in friends_list:
            in_list+=str(frnd[0])+","
        in_list = in_list[:-1]
        in_list+=")"
        posts_query = 'select distinct p.post_id, u.first_name, u.last_name, p.title, p.posted_when, p.content, p.upload, l.location_area, p.user_id from users u, user_post p, location_post l where p.post_id = l.post_id and p.user_id=u.user_id and l.location_area like "%'+ searchtext +'%"and p.user_id in '+in_list+' order by posted_when DESC'
        print posts_query
        self.runquery.execute(posts_query)
        data = self.runquery.fetchall()
        posts = []
        for item in data:
            post = {}
            post["post_id"] = item[0]
            post["first_name"] = item[1]
            post["last_name"] = item[2]
            post["title"] = item[3]
            post["posted_when"] = item[4]
            post["content"] = item[5]
            post["upload"] = item[6]
            post["location"] = item[7]
            post["user_id"] = item[8]
            post["likes"] = {}
            self.runquery.execute("select u.first_name, u.user_id from users u, likes_post l where l.liked_by_id = u.user_id and l.post_id = '%s'"%post["post_id"])
            likes = self.runquery.fetchall()
            for like in likes:
                post["likes"][like[1]] = like[0]
            post["comments"] = []
            self.runquery.execute("select c.comment_id, u.first_name, u.user_id, c.content, c.commented_when from users u, comments c where c.user_id = u.user_id and c.post_id = '%s'"%post["post_id"])
            comments = self.runquery.fetchall()
            for comment in comments:
              row = {}
              row["comment_id"] = comment[0]
              row["first_name"] = comment[1]
              row["user_id"] = comment[2]
              row["content"] = comment[3]
              row["commented_when"] = comment[4]
              row["likes"] = {}
              self.runquery.execute("select u.first_name, u.user_id from users u, likes_comment l where l.liked_by_id = u.user_id and l.comment_id = '%s'"%row["comment_id"])
              likes = self.runquery.fetchall()
              for like in likes:
                  row["likes"][like[1]] = like[0]
              post["comments"].append(row)
            posts.append(post)
        return posts

    def sendmessage(self, to_id, from_id, msg):
        self.runquery.execute("insert into message(to_id, from_id, msg) values('%s', '%s', '%s')"%(to_id, from_id, msg))
        self.db.commit()
        return

    def get_messages(self, user_id):
        self.runquery.execute("select u.first_name, u.last_name, m.from_id, m.msg from message m, users u where u.user_id = m.from_id and m.to_id='%s' order by m.sent_when DESC"%user_id)
        data = self.runquery.fetchall()
        msgs = []
        for item in data:
            msg = {}
            msg["first_name"] = item[0]
            msg["last_name"] = item[1]
            msg["from_id"] = item[2]
            msg["msg"] = item[3]
            msgs.append(msg)
        return msgs
    def postcontent(self, objuser_post, location):
        print objuser_post.upload
        post_query = 'insert into user_post(user_id,\
                                            posted_when,\
                                            content,\
                                            title,\
                                            upload,\
                                            visibility_id) \
                                            values("%s", "%s", "%s", "%s","%s" , "%s")'\
                                            %(objuser_post.user_id,
                                            objuser_post.posted_when,
                                            objuser_post.content,
                                            objuser_post.title, 
                                            objuser_post.upload,
                                            objuser_post.visibility_id)
        self.runquery.execute(post_query)
        post_id = self.runquery.lastrowid
        self.db.commit()

        if location.strip() == "":
            area = None
        else:
            area = location
        location_query = "insert into location_post(post_id, location_area) values('%s', '%s')" %(post_id, location)
        self.runquery.execute(location_query)
        self.db.commit()
        return post_id

    def is_friend(self, user_id, logged_in_user):
        self.runquery.execute("select * from friends where user_id='%s' and friend_id='%s'"%(logged_in_user, user_id))
        return self.runquery.fetchone()

    def is_friend_of_friend(self, user_id, logged_in_user):
        self.runquery.execute("select friend_id from friends where user_id='%s'"%(logged_in_user))
        friend_ids = self.runquery.fetchall()
        if friend_ids:
          in_list = "("
          for item in friend_ids:
              in_list+=str(item[0])+","
          in_list=in_list[:-1]+")"
        else:
          return False

        self.runquery.execute("select friend_id from friends where user_id in %s"%in_list)
        friends_of_friend = self.runquery.fetchall()
        frnds = []
        for frnd in friends_of_friend:
            frnds.append(str(frnd[0]))
        if user_id in frnds:
            return True
        return False

    def get_frnd_visibility(self, user_id):
        self.runquery.execute("select friends_visibility_id from users where user_id='%s'"%user_id)
        return self.runquery.fetchone()[0]

    def get_user_friends(self, user_id, logged_in_user):
        frnd_uery = "select u.first_name, u.last_name, f.friend_id from users u, friends f where u.user_id = f.friend_id and f.user_id = '%s'"%user_id
        self.runquery.execute(frnd_uery)
        lst = self.runquery.fetchall()
        frnds_lst = []
        for lt in lst:
          frnd_lst = {}
          frnd_lst["first_name"] = lt[0]
          frnd_lst["last_name"] = lt[1]
          frnd_lst["user_id"] = lt[2]
          frnds_lst.append(frnd_lst)
        return frnds_lst

    def get_user_posts(self, user_id, logged_in_user):
        if self.is_friend(user_id, logged_in_user) or (str(logged_in_user) == str(user_id)):
            posts_query = 'select distinct p.post_id, u.first_name, u.last_name, p.title, p.posted_when, p.content, p.upload, l.location_area from users u, user_post p, location_post l where p.user_id = u.user_id and l.post_id = p.post_id and p.user_id = "%s" order by posted_when DESC' %user_id
        elif self.is_friend_of_friend(user_id, logged_in_user):
            posts_query = 'select distinct p.post_id, u.first_name, u.last_name, p.title, p.posted_when, p.content, p.upload, l.location_area from users u, user_post p, location_post l where p.user_id = u.user_id and l.post_id = p.post_id and p.user_id = "%s" and (p.visibility_id=2 or p.visibility_id=3) order by posted_when DESC' %user_id
        else:
            return []
        self.runquery.execute(posts_query)
        data = self.runquery.fetchall()
        posts = []
        for item in data:
            post = {}
            post["post_id"] = item[0]
            post["first_name"] = item[1]
            post["last_name"] = item[2]
            post["title"] = item[3]
            post["posted_when"] = item[4]
            post["content"] = item[5]
            post["upload"] = item[6]
            post["location"] = item[7]
            post["user_id"] = user_id
            post["likes"] = {}
            self.runquery.execute("select u.first_name, u.user_id from users u, likes_post l where l.liked_by_id = u.user_id and l.post_id = '%s'"%post["post_id"])
            likes = self.runquery.fetchall()
            for like in likes:
                post["likes"][like[1]] = like[0]
            post["comments"] = []
            self.runquery.execute("select c.comment_id, u.first_name, u.user_id, c.content, c.commented_when from users u, comments c where c.user_id = u.user_id and c.post_id = '%s'"%post["post_id"])
            comments = self.runquery.fetchall()
            for comment in comments:
              row = {}
              row["comment_id"] = comment[0]
              row["first_name"] = comment[1]
              row["user_id"] = comment[2]
              row["content"] = comment[3]
              row["commented_when"] = comment[4]
              row["likes"] = {}
              self.runquery.execute("select u.first_name, u.user_id from users u, likes_comment l where l.liked_by_id = u.user_id and l.comment_id = '%s'"%row["comment_id"])
              likes = self.runquery.fetchall()
              for like in likes:
                  row["likes"][like[1]] = like[0]
              post["comments"].append(row)
            posts.append(post)
        return posts

    def get_posts(self, user_id):
        friends_list = self.get_friends(user_id)
        in_list = "("
        for frnd in friends_list:
            in_list+=str(frnd[0])+","
        in_list+= str(user_id)
        in_list+=")"
        posts_query = 'select distinct p.post_id, u.first_name, u.last_name, p.title, p.posted_when, p.content, p.upload, l.location_area, p.user_id from users u, user_post p, location_post l where p.post_id = l.post_id and p.user_id=u.user_id and p.user_id in %s order by posted_when DESC' %in_list
        print posts_query
        self.runquery.execute(posts_query)
        data = self.runquery.fetchall()
        posts = []
        for item in data:
            post = {}
            post["post_id"] = item[0]
            post["first_name"] = item[1]
            post["last_name"] = item[2]
            post["title"] = item[3]
            post["posted_when"] = item[4]
            post["content"] = item[5]
            post["upload"] = item[6]
            post["location"] = item[7]
            post["user_id"] = item[8]
            post["likes"] = {}
            self.runquery.execute("select u.first_name, u.user_id from users u, likes_post l where l.liked_by_id = u.user_id and l.post_id = '%s'"%post["post_id"])
            likes = self.runquery.fetchall()
            for like in likes:
                post["likes"][like[1]] = like[0]
            post["comments"] = []
            self.runquery.execute("select c.comment_id, u.first_name, u.user_id, c.content, c.commented_when from users u, comments c where c.user_id = u.user_id and c.post_id = '%s'"%post["post_id"])
            comments = self.runquery.fetchall()
            for comment in comments:
              row = {}
              row["comment_id"] = comment[0]
              row["first_name"] = comment[1]
              row["user_id"] = comment[2]
              row["content"] = comment[3]
              row["commented_when"] = comment[4]
              row["likes"] = {}
              self.runquery.execute("select u.first_name, u.user_id from users u, likes_comment l where l.liked_by_id = u.user_id and l.comment_id = '%s'"%row["comment_id"])
              likes = self.runquery.fetchall()
              for like in likes:
                  row["likes"][like[1]] = like[0]
              post["comments"].append(row)
            posts.append(post)
        return posts

    def likepost(self, like_post):
        like_query = "insert into likes_post(post_id, liked_by_id) values('%s', '%s')" %(like_post.post_id, like_post.liked_by_id)
        self.runquery.execute(like_query)
        self.db.commit()
        self.runquery.execute("select count(*) from likes_post where post_id='%s'"%like_post.post_id)
        data = self.runquery.fetchone()
        if data[0] > 0:
          return "(" + str(data[0]) + ")"
        return ""

    def unlikepost(self, like_post):
        unlike_query = "delete from likes_post where post_id = '%s' and liked_by_id = '%s'" %(like_post.post_id, like_post.liked_by_id)
        self.runquery.execute(unlike_query)
        self.db.commit()
        self.runquery.execute("select count(*) from likes_post where post_id='%s'"%like_post.post_id)
        data = self.runquery.fetchone()
        if data[0] > 0:
          return "(" + str(data[0]) + ")"
        return ""

    def comment(self, comment):
        comment_query = "insert into comments(post_id, content, user_id) values('%s', '%s', '%s')" %(comment.post_id, comment.content, comment.user_id)
        self.runquery.execute(comment_query)
        self.db.commit()
        return str(self.runquery.lastrowid)

    def likecomment(self, like_comment):
        like_query = "insert into likes_comment(comment_id, liked_by_id) values('%s', '%s')" %(like_comment.comment_id, like_comment.liked_by_id)
        self.runquery.execute(like_query)
        self.db.commit()
        self.runquery.execute("select count(*) from likes_comment where comment_id='%s'"%like_comment.comment_id)
        data = self.runquery.fetchone()
        if data[0] > 0:
          return "(" + str(data[0]) + ")"
        return ""

    def unlikecomment(self, like_comment):
        unlike_query = "delete from likes_comment where comment_id = '%s' and liked_by_id = '%s'" %(like_comment.comment_id, like_comment.liked_by_id)
        self.runquery.execute(unlike_query)
        self.db.commit()
        self.runquery.execute("select count(*) from likes_comment where comment_id='%s'"%like_comment.comment_id)
        data = self.runquery.fetchone()
        if data[0] > 0:
          return "(" + str(data[0]) + ")"
        return ""

    def get_friends(self, user_id):
        friends_query = "select friend_id from friends where user_id = '%s'" %user_id
        self.runquery.execute(friends_query)
        results = self.runquery.fetchall()
        return results

