from pyngrok import ngrok

HTTPTUNNEL = ngrok.connect()
print(HTTPTUNNEL.public_url)
while 1:
    pass