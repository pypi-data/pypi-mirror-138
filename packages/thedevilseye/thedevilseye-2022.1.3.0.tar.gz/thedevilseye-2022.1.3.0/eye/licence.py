def licence():
        with open('LICENSE', 'r') as file:
        	content = file.read()
        	file.close()
        	return content