




import urllib.request

webUrl  = urllib.request.urlopen('https://china-testing.github.io/address.html')


print ("result code: " + str(webUrl.getcode()))


data = webUrl.read()
print (data)