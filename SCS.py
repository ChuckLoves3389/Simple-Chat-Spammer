from telethon import TelegramClient, events
import asyncio
from telethon.tl.types import MessageMediaPhoto
import pyfiglet

# authorisation
API_ID = "" 
API_HASH = ""  
SESSION_NAME = "default" 

def print_ascii_art():
    ascii_art = pyfiglet.figlet_format("palera11n")
    print(ascii_art)
    print("hello, im palera11n, this script for educational purposes only\n")


client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage)
async def handle_rassilka(event):
    if not event.text or not event.text.startswith(".send"):
        return

    try:
        command = event.text[10:].strip() 
        parts = command.split(",", 2)  

        if len(parts) < 3:
            await event.reply("Command settings: `.send <interval>,<message>,<how much messages to send>`")
            return

        interval = float(parts[0].strip())  
        rassilka_message = parts[1].strip()  
        count = int(parts[2].strip())  

        if interval <= 0 or count <= 0:
            await event.reply("Numbers must")
            return

        photo = None
        if event.message.media and isinstance(event.message.media, MessageMediaPhoto):
            photo = event.message.media

        topic_id = event.message.reply_to.reply_to_msg_id if event.message.is_reply else None

        for i in range(count):
            if topic_id:
                await client.send_message(
                    event.chat_id,
                    rassilka_message,
                    file=photo,  
                    reply_to=topic_id
                )
            else:
                await client.send_message(
                    event.chat_id,
                    rassilka_message,
                    file=photo
                )
            await asyncio.sleep(interval)

        await event.reply("Spam ended!")
    except ValueError:
        await event.reply("Value Error")
    except Exception as e:
        await event.reply(f"Error: {e}")

if __name__ == "__main__":
    print_ascii_art()  
    client.start()
    client.run_until_disconnected()
