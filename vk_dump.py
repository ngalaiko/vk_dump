import argparse
import func
import sys
import os

def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-vl', '--vk-login', default = None)
	parser.add_argument('-vp', '--vk-password', default = None)
	parser.add_argument('-vt', '--vk-token', default = None)
	parser.add_argument('-id', '--id', default = None)

	return parser

if __name__ == '__main__':
	parser = create_parser()
	namespace = parser.parse_args(sys.argv[1:])

	if (not namespace.vk_login and not namespace.vk_password) and (not namespace.vk_token):
		print('You should use login and password or token!')
		sys.exit()

	vk_api = func.auth(
		namespace.vk_token,
		namespace.vk_login,
		namespace.vk_password)

	# first, get user id 
	user_id = func.me(vk_api)

	if not os.path.exists('./result'):
		os.makedirs('./result')

	if namespace.id:
		user = vk_api.users.get(user_ids=namespace.id)[0]
		fullname = user['first_name'] + ' ' + user['last_name']

		if not os.path.exists('./result/' + fullname):
			os.makedirs('./result/' + fullname)

		func.dump_dialog_history(vk_api, namespace.id, False, './result/' + fullname)
		sys.exit()

	func.dump_friends(vk_api, user_id)
	func.dump_dialogs(vk_api, user_id)
