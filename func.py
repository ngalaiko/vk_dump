import datetime
import time
import os
import vk 

# returns obj to access api
def auth(vk_token, vk_login, vk_password):
	vk_api = None

	if vk_token:
		session = vk.AuthSession(access_token=vk_token)

		vk_api = vk.API(session)
	elif vk_login and vk_password:
		session = vk.AuthSession(
			app_id='5513659', 
			user_login = vk_login, 
			user_password = vk_password,
			scope = 'messages,friends,audio,docs,photos,video,offline')

		vk_api = vk.API(session)

	return vk_api

# returnes if of authorized user
def me(vk_api):
	response = vk_api.users.get(v='2.0.2')
	current_id = response[0]['uid']

	return current_id

def dump_friends(vk_api, user_id):
	print('dumping friends...')
	
	friends = vk_api.friends.get(user_id=user_id, order='hints', fields='nickname', v='2.0.2')
	with open('./result/friends.txt', 'w') as f:
		for user in friends:
			f.write(
				user['first_name'] + ' ' + user['last_name'] + 
				' vk.com/id' + str(user['uid']) + 
				'\n')

	print('Done\n')

def dump_dialogs(vk_api, user_id):
	print('dumping dialogs...')
	offset = 0

	all_dialogs = []
	while True:
		response = vk_api.messages.getDialogs(count=200, offset=offset, v='2.0.2')
		dialogs = response[1:]
		all_dialogs.append(dialogs)

		if len(dialogs) == 0:
			break

		path_to_res = './result'
		for dialog in dialogs:
			newpath = path_to_res
			need_sleep = False
			id_to_dump = 0
			is_multichat = False

			try:
				# if it is not multichat, will fail
				check = dialog['chat_id']

				id_to_dump = dialog['chat_id']
				is_multichat = True
				newpath += '/groups/' + dialog['title']
			except:
				# get user
				user = vk_api.users.get(user_ids=dialog['uid'], v='2.0.2')[0]
				
				newpath += '/messages/' + user['first_name'] + ' ' + user['last_name']
				id_to_dump = user['uid']

				need_sleep = True	
			finally:
				if not os.path.exists(newpath):
					os.makedirs(newpath)

			if need_sleep:
				sleep()

			dump_dialog_history(vk_api, id_to_dump, is_multichat, newpath)

		offset += 200
		sleep()

	print('Done')

def dump_dialog_history(vk_api, user_id, is_multichat, path):
	offset = 0
	all_messages = []
	all_user_ids = set()
	all_users = {}

	if not is_multichat:
		user = vk_api.users.get(user_ids=user_id, v='2.0.2')[0]
		all_users[user['uid']] = user

		print('	dumping history with', user['first_name'], user['last_name'] + '...')

		sleep()
	else:
		chat = vk_api.messages.getChat(chat_id=user_id, v='2.0.2')

		print('	dumping history in', chat['title'] + '...')

		# api requrement
		user_id += 2000000000
		
		sleep()

	while True:
		response = vk_api.messages.getHistory(user_id=user_id, v='2.0.2', count=200, offset = offset, rev = 1)
		messages = response[1:]
		all_messages += messages

		if len(messages) == 0:
			break

		# remember all user_ids in chat
		for message in messages:
			all_user_ids.add(message['from_id'])		

		offset += 200

		sleep()

	# map of all users in chat
	users = vk_api.users.get(user_ids=all_user_ids, v='2.0.2')
	for user in users:
		all_users[user['uid']] = user
	
	history_file = open(path + '/history.txt', 'w')
	photos_file = open(path + '/photos.txt', 'w')
	vieos_file = open(path + '/videos.txt', 'w')

	for message in all_messages:
		from_user = all_users[message['from_id']]

		date = datetime.datetime.fromtimestamp(
	        int(message['date'])
	    ).strftime('%Y-%m-%d %H:%M:%S')

		history_file.write(
			'[' + date + '] ' + 
			from_user['first_name'] + ' ' + from_user['last_name'] + ': ' 
			+ message['body'] + '\n')

		dump_attachments(vk_api, message, history_file, photos_file, vieos_file)

	history_file.close()
	photos_file.close()
	vieos_file.close()

def dump_attachments(vk_api, message, history_file, photos_file, vieos_file):
	try:
		attatchments = message['attachments']
		for attatchment in attatchments:
			if attatchment['type'] == 'photo':
				photo_url = attatchment['photo']['src_big']

				photos_file.write(photo_url + '\n')
				history_file.write(photo_url + '\n')
			elif attatchment['type'] == 'video':
				video = vk_api.video.get(v='2.0.2', videos=
					str(attatchment['video']['owner_id']) + '_' +
					str(attatchment['video']['vid']) + '_' +
					str(attatchment['video']['access_key']))[1]
					
				sleep()

				video_url = video['player']

				vieos_file.write(video_url + '\n')
				history_file.write(video_url + '\n')		
	except:
		return

# default sleep time
def sleep():
	time.sleep(1)
