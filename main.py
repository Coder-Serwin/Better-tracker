from flask import Flask, request, redirect
from bot import *
import random
from subprocess import run
import time

os.environ['IP_ADDR'] = "None"
app = Flask(__name__)
ip_address = None
D_TOKEN = os.getenv('D_TOKEN')


@app.route('/')
def home():
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR',request.remote_addr)
    os.environ['IP_ADDR'] = ip_address
    run(["python", "bot.py"])
    time.sleep(1)
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(str(D_TOKEN))
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
