import web 
listap = dir(web.application.run.__delattr__.__cmp__)
for t in listap:
	print t