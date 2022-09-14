import threading
import paramiko
from discord.ext import commands
import os
import time
import random

TOKEN = "IM A DISCORD TOwOKEN"

# If are reading this
# HELLO

servers = [
  "IP:PASS",
  "IP:PASS",
  "IP:PASS"
]


bot = commands.Bot(command_prefix='!')

def setup(server, password, lines):
	rand_int = random.randint(123123,31212123233)
	f = open(f"temp/temp-{rand_int}.txt", "w")
	for line in lines:
		f.write(f"{line}\n")
	f.close()

	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=server, username="root",
					   password=password)
	print(f"\033[90m[\033[93m*\033[90m]\033[39m {server}")
	ssh_client.exec_command("mkdir Namechange")
	ftp_client = ssh_client.open_sftp()
	ftp_client.put(os.path.abspath(os.getcwd()).replace(
		"\\", "/") + f"/temp/temp-{rand_int}.txt", "Namechange/accounts.txt")
	ftp_client.close()
	time.sleep(0.5)
	print(f"\033[90m[\033[92m+\033[90m]\033[39m {server}:\n{lines}")

def setup_nc(server, password, name, delay):
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=server, username="root",
					   password=password)
	print(f"\033[90m[\033[93m*\033[90m]\033[39m {server}")
	ssh_client.exec_command("pkill -9 python3")
	ssh_client.exec_command("apt install screen -y --fix-missing")
	ssh_client.exec_command("apt install python3 -y --fix-missing")
	ssh_client.exec_command("apt install python3-pip -y --fix-missing")
	ssh_client.exec_command("mkdir Namechange")
	ftp_client = ssh_client.open_sftp()
	ftp_client.put(os.path.abspath(os.getcwd()).replace(
		"\\", "/") + "/Namechange/main.py", "Namechange/main.py")
	ftp_client.put(os.path.abspath(os.getcwd()).replace(
		"\\", "/") + "/Namechange/requirements.txt", "Namechange/requirements.txt")
	ftp_client.close()
	time.sleep(2.5)
	_, a, _ = ssh_client.exec_command(
		"pip3 install -r Namechange/requirements.txt")
	a.readlines()
	time.sleep(5.5)
	print(f"\033[90m[\033[92m+\033[90m]\033[39m {server} : {delay}")
	_, a, _ = ssh_client.exec_command(
		f"screen python3 Namechange/main.py {name} {delay}", get_pty=True)
	print(a.readlines())

def setup_gc(server, password, name):
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=server, username="root",
					   password=password)
	print(f"\033[90m[\033[93m*\033[90m]\033[39m {server}")
	ssh_client.exec_command("pkill -9 python3")
	ssh_client.exec_command("apt install screen -y --fix-missing")
	ssh_client.exec_command("apt install python3 -y --fix-missing")
	ssh_client.exec_command("apt install python3-pip -y --fix-missing")
	ssh_client.exec_command("mkdir Giftcode")
	ftp_client = ssh_client.open_sftp()
	ftp_client.put(os.path.abspath(os.getcwd()).replace(
		"\\", "/") + "/Giftcode/main.py", "Giftcode/main.py")
	ftp_client.put(os.path.abspath(os.getcwd()).replace(
		"\\", "/") + "/Giftcode/requirements.txt", "Giftcode/requirements.txt")
	ftp_client.close()
	time.sleep(2.5)
	_, a, _ = ssh_client.exec_command(
		"pip3 install -r Giftcode/requirements.txt")
	a.readlines()
	time.sleep(5.5)
	print(f"\033[90m[\033[92m+\033[90m]\033[39m {server}")
	_, a, _ = ssh_client.exec_command(
		f"screen python3 Giftcode/main.py {name} 0.035", get_pty=True)
	print(a.readlines())

@bot.event
async def on_ready():
	global s
	print(f"{bot.user} is now online")

@bot.command(name="configure_nc", help="Configure servers")
async def conf_nc(ctx):
	await ctx.send(f"Preparing...")
	f = open("accounts.txt", "r")
	lines = f.read().split("\n")
	f.close()

	the_list = []

	for i in range(len(lines)):
		try:
			acc1 = lines[i]
		except:
			break
		try:
			acc2 = lines[i + 1]
			the_list.append([acc1, acc2])
			i+=2
		except:
			the_list.append([acc1])
			i+=1

	i = 0
	for server in servers:
		try:
			ip = server.split(":")[0]
			passwd = server.split(":")[1]
			lines = the_list[i]
			threading.Thread(target=setup, args=(ip, passwd, lines,)).start()
			i += 1
		except:
			break

	await ctx.send(f"All servers have been prepared")

@bot.command(name="giftcode", help="GC Snipes a given name, usage: !giftcode <name>")
async def giftcode(ctx, name: str):
	await ctx.send(f"Preparing to snipe {name}...")
	for server in servers:
		ip = server.split(":")[0]
		passwd = server.split(":")[1]
		threading.Thread(target=setup_gc, args=(ip, passwd, name,)).start()
	await ctx.send(f"All servers have been prepared to snipe {name}")

@bot.command(name="namechange", help="NC Snipes a given name, usage: !namechange <name>")
async def namechange(ctx, name: str):
	await ctx.send(f"Preparing to snipe {name}...")
	i = 0
	for server in servers:
		ip = server.split(":")[0]
		passwd = server.split(":")[1]
		delay = 0.069 + (0.0005*i)
		threading.Thread(target=setup_nc, args=(ip, passwd, name, delay,)).start()
		i+=1
	await ctx.send(f"All servers have been prepared to snipe {name}")

bot.run(TOKEN)
