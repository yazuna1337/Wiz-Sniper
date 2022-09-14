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

# Replace lines 18, 67, 69

proxies = [
    "proxy-ip1-here",
    "proxy-ip2-here",
    "etc"
]

bearers = Queue()
lock = threading.Lock()


def microsoft_login(email, password) -> UserProfileInformation:
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
    return requests.get("https://api.star.shopping/droptime/"+name, headers={"User-Agent": "Sniper"}).json()["unix"]


async def snipe_worker(proxy, droptime, target, delay):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while time.time() < droptime-4:
        time.sleep(1)

    bearer = bearers.get()

    headers = {
        "Authorization": bearer,
        "Content-Type": "application/json"
    }

    bearers.task_done()

    proxy_list = {
        "http://": f"http://[USERNAME:PASSWORD]@{proxy}:[PROXY-PORT]",
        "https://": f"http://[USERNAME:PASSWORD]@{proxy}:[PROXY-PORT]",
    }

    tasks = []

    profile_json = {
        "profileName": target
    }

    async with httpx.AsyncClient(proxies=proxy_list) as session:
        try:
            futures = [await send_request(session, headers, profile_json)
                       for _ in range(2)]

            while droptime-(time.time()+delay) >= 0:
                pass

            print(" ", datetime.datetime.utcfromtimestamp(time.time()))
            # loop.run_until_complete(asyncio.gather(*futures))
            await asyncio.gather(*tasks)

        except:
            print(f"Exception in {proxy}")


async def send_request(session, headers, json_body):
    r = await session.post("https://api.minecraftservices.com/minecraft/profile", headers=headers, json=json_body)
    end = datetime.datetime.utcfromtimestamp(time.time())
    if r.status_code == 200:
        print(" ", r.status_code, end)
        print("  Successfully sniped "+json_body["profileName"]+"!")
    elif r.status_code == 400:
        print(" ", r.status_code, end, r.json()[
              'errorMessage'], r.headers["Date"])
    else:
        print(" ", r.status_code, end)


def main():
    colorama.init()
    os.system("clear")
    print("  \033[32mOblivion\033[91mSniper\033[39m #COOLEDITION")
    target = sys.argv[1]
    delay = float(sys.argv[2])

    droptime = get_droptime(target)
    drop_time = datetime.datetime.utcfromtimestamp(droptime)
    print(f"  {drop_time}")
    print()

    print("  Setting Up...")

    f = open("accounts.txt", "r")
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
        email = account.split(":")[0]
        password = account.split(":")[1]
        bearers.put(microsoft_login(
            email, password))
        i += 1

    print("  Finished Authentication.")
    print()

    for proxy in proxies:
        threading.Thread(target=asyncio.run, args=(
            snipe_worker(proxy, droptime, target, delay),), daemon=True).start()

    while droptime-(time.time()) >= 0:
        time.sleep(1)


main()
