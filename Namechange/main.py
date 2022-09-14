import socket
import time
import datetime
import asyncio
import requests
import os
from requests import Session
from msmcauth import XboxLive, UserProfileInformation, Microsoft
import httpx
import sys
import threading
from queue import Queue
import colorama

bearers = []

lock = threading.Lock()


def microsoft_login(email, password) -> UserProfileInformation:
    print(email, password)
    try:
        client = Session()

        xbx = XboxLive(client)
        mic = Microsoft(client)

        login = xbx.user_login(email, password, xbx.pre_auth())

        xbl = mic.xbl_authenticate(login)
        xsts = mic.xsts_authenticate(xbl)

        access_token = mic.login_with_xbox(xsts.token, xsts.user_hash)
    except Exception as e:
        print(f"  [Auth] [{email}:{password}] An Error Occured, {e}")
        return "Bearer None"

    token = "Bearer " + access_token
    return token


def get_droptime(name):
    if name == "Notch":
        return time.time()+10
    return requests.get("https://api.star.shopping/droptime/"+name, headers={"User-Agent": "Sniper"}).json()["unix"]


async def snipe_worker(droptime, target, delay):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while time.time() < droptime-4:
        time.sleep(1)

    profile_json = {
        "profileName": target
    }

    async with httpx.AsyncClient() as session:
        tasks = []
        for bearer in bearers:
            headers = {
                "Authorization": bearer,
                "Content-Type": "application/json"
            }

            for _ in range(3):
                tasks.append(send_request(session, headers, target))

        while droptime-(time.time()+delay) >= 0:
            pass
        print(" ", datetime.datetime.utcfromtimestamp(time.time()))
        await asyncio.gather(*tasks)


async def send_request(session, headers, target):
    r = await session.put(f"https://api.minecraftservices.com/minecraft/profile/name/{target}", headers=headers)
    end = datetime.datetime.utcfromtimestamp(time.time())

    requests.post("owo webhook", json={"embeds": [{
         "title": "Log",
         "description": f"`{target} {end} {r.status_code}`"}]})

    if r.status_code == 200:
        print(" ", r.status_code, end)
        print("  Successfully sniped "+target+"!")
        requests.post("uwwwwwu webhook", json={"embeds": [{
         "title": "Sniped",
         "description": f"`{target}`"}]})
    elif r.status_code == 400:
        print(" ", r.status_code, end, r.json()[
              'errorMessage'], r.headers["Date"])
    else:
        print(" ", r.status_code, end)


def main():
    colorama.init()
    os.system("clear")
    print("  \033[32mOblivion\033[91mSniper\033[39m (owo)")
    target = sys.argv[1]
    delay = float(sys.argv[2])

    droptime = get_droptime(target)
    drop_time = datetime.datetime.utcfromtimestamp(droptime)
    print(f"  {drop_time}")
    print()

    print("  Setting Up...")

    f = open("Namechange/accounts.txt", "r")
    accounts = f.read().split("\n")
    if '' in accounts:
        accounts.remove('')
    f.close()

    print(f"  Authenticating {len(accounts)} accounts...")

    i = 0
    for account in accounts:
        if i == 2:
            time.sleep(65)
            i = 0
        email = account.split("#-:-#")[0]
        password = account.split("#-:-#")[1]
        bearers.append(microsoft_login(
            email, password))
        i += 1

    print("  Finished Authentication.")
    print()

    asyncio.run(snipe_worker(droptime, target, delay))


main()
