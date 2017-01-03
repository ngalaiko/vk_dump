import argparse
import func
import sys

def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-vl', '--vk-login', default = None)
	parser.add_argument('-vp', '--vk-password', default = None)
	parser.add_argument('-vt', '--vk-token', default = None)

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

	print(vk_api)