from whatsappy import Whatsapp

whatsapp = Whatsapp()

whatsapp.login(visible=True)

chat = whatsapp.chat("Bleimdah")
last_message = chat.last_message

with open("audio.ogg", "wb+") as f:
    f.write(last_message.file.content)

print(last_message)

whatsapp.close()