import time
import vk 

def auth(vk_token, vk_login, vk_password):
	vk_api = None

	if vk_token:
		session = vk.AuthSession(access_token=vk_token)

		vk_api = vk.API(session)
	elif vk_login and vk_password:
		print(vk_login, vk_password)

		session = vk.AuthSession(
			app_id='5513659', 
			user_login = vk_login, 
			user_password = vk_password, 
			scope = 'friends,audio,docs,photos,offline')

		vk_api = vk.API(session)

	return vk_api

def messages(vk_api, id_):
		offset = 0

		for i in range(100):
			pass
			messages = vk_api.messages.getHistory(user_id=id_, count=200, offset = offset)

			for message in messages[1:]:
				if message['uid'] == 3459878:
					print('Саша' + ': ' + message['body'])
				else:
					print('Настя' + ': ' + message['body'])

			offset += 200
			time.sleep(1)

def photos(vk_api, peer_id):
		offset = 0

		for i in range(1000):
			attatchments = vk_api.messages.getHistoryAttachments(peer_id=peer_id, media_type='photo', count = 200, offset=offset)

			for photo in attatchments[1:]:
				try:
					print(photo['photo']['src_xbig'])
				except:
					continue

			offset += 200
			time.sleep(1)
