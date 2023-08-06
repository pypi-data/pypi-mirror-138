from whatsappy import Whatsapp
from rich.console import Console

whatsapp = Whatsapp()
console = Console()

whatsapp.login(visible=True)

group = whatsapp.chat("__Python__Iniciantes")
console.print(group.last_message)

whatsapp.close()
