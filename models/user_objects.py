from datetime import datetime

class comments:
	comment_id = None
	post_id = None
	user_id = None
	content = None
	commented_when = datetime.now()

class friends:
	user_id = None
	friend_id = None

class friend_requests:
	request_id = None
	from_id = None
	to_id = None
	when_sent = datetime.now()

class likes_comment:
	comment_id = None
	liked_by_id = None

class likes_post:
	post_id = None
	liked_by_id = None

class location_post:
	post_id = None
	location_area = None

class usr_profile:
	user_id = None
	school = None
	university = None
	job = None

class relationship:
	relationship_id = None
	user_id = None
	user_id_map = None
	relationship = None

class users:
	user_id = None
	password = None
	first_name = None
	last_name = None
	email_id = None
	join_date = datetime.now()
	current_location = None
	relationship_status = None
	date_of_birth = None
	profile_pic = "default.png"
	friends_visibility_id = 1
	post_visibility_id = 1

class user_post:
	post_id = None
	user_id = None
	posted_when = datetime.now()
	content = None
	title = None
	upload = None
	visibility_id = None
