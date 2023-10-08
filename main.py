import os, time, json
import undetected_chromedriver as undetected
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

page = 1

def clear():
    os.system("cls")

def banner():
    informations = """
# Use the script calmly, I didn't program it to detect the ratelimit of disboard and discord. #
# Script made by: Aryoutic #
# Categories: gaming, community, anime-manga, music, technology, language, movies, other. #
# Languages: en, es, fr, it, pt-br, pt-pt, pl, de, tr, ru, ar. #
"""
    print(informations)

def start():
    with open("config.json", "r") as config:
        data = json.load(config)

    categorie = data["Categorie"]
    language = data["Language"]

    global page

    chrome = webdriver.Chrome(options=options)
    chrome.set_window_size(1,1)
    chrome.get(f"https://disboard.org/servers/category/{categorie}/{page}?fl={language}")

    server_list = chrome.find_elements(By.CLASS_NAME, "server-name")
    servers = []

    for content in server_list:
        server_name = content.find_element(By.TAG_NAME, "a")
        server_id = (server_name.get_attribute("href").replace("https://disboard.org/server/", ""))
        servers.append(server_id)
        print(f"# Server found: {server_name.text} [{servers.index(server_id)}] #")

    while 1:
        decide = input(f"\n# Enter the server number, or type N to go to the next page (Page {page} of 50): ")

        if decide in ['n', 'N']:
            if page == 50:
                print("# Cannot continue, you have already reached page 50. #")
            else:
                chrome.quit()
                page += 1
                clear()
                start()
                break
        else:
            try:
                convert = int(decide)

                if convert <= len(servers):
                    server_id = servers[convert]

                    safe_options = undetected.ChromeOptions()
                    safe_options.headless = False
                    safe_chrome = undetected.Chrome(options=safe_options)
                    safe_chrome.set_window_size(1, 1)
                    safe_chrome.get(f"https://disboard.org/server/join/{server_id}")

                    time.sleep(7)

                    title = safe_chrome.find_element("tag name", "h1")

                    if title == "Discord App Launched":
                        print("# The server has been opened on your discord. #")
                    elif title == "Invite Invalid":
                        print("# The server invite is invalid. #")
                    else:
                        pass
                    safe_chrome.quit()
            except:
                pass  
    else:
        print("\n# The server number you entered does not exist. #")

clear()
banner()
start()