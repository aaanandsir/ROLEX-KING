import requests
import logging
from time import sleep
import uuid
import os
import webbrowser

API_VERSION = 'v15.0'

HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

LOGO_COLORS = {
    'red': '\033[1;31;40m',
    'green': '\033[1;32;40m',
    'blue': '\033;34;40m',
    'diamond': '\033[1;36;40m',
    'golden': '\033[1;33;40m',
    'shiny': '\033[1;35;40m',
    'glossy': '\033[1;34;40m',
    'glow': '\033[1;37;41m',  # Glow effect (white text on red background)
    'reset': '\033[0m',
    'bold': '\033[1m'
}

LOGO = f"""
{LOGO_COLORS['red']}  
"""

def verify_approval():
    try:
        approval_key = open('ApprovalKey.txt', 'r').read().strip()
    except FileNotFoundError:
        print(LOGO)
        print("[*]_______________________")
        print("  Program not approved. Contact the owner for approval key.")
        print("[*]_______________________")
        exit()

    user_key = input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter your approval key: " + LOGO_COLORS['reset'])

    if user_key != approval_key:
        print(LOGO)
        print("[*]_______________________")
        print("  Invalid approval key. Contact the owner for the correct key.")
        print("[*]_______________________")
        exit()

def verify_cookies(cookies):
    try:
        response = requests.get(f'https://graph.facebook.com/{API_VERSION}/me', headers={'Cookie': cookies})
        response.raise_for_status()
        user_data = response.json()
        return user_data.get('name', 'Unknown User')
    except requests.exceptions.RequestException as e:
        logging.error(f"{LOGO_COLORS['red']}Error verifying cookies: {e}{LOGO_COLORS['reset']}")
        return 'Unknown User'

def generate_token(username, password):
    try:
        response = requests.get(f'https://graph.facebook.com/{API_VERSION}/me?access_token={username}|{password}')
        response.raise_for_status()
        user_data = response.json()
        return user_data.get('name', 'Unknown User')
    except requests.exceptions.RequestException as e:
        logging.error(f"{LOGO_COLORS['red']}Error generating token: {e}{LOGO_COLORS['reset']}")
        return 'Unknown User'

def wait_for_internet():
    while True:
        try:
            response = requests.get("http://www.google.com", timeout=1)
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            pass
        sleep(2)

def authenticate_user():
    wait_for_internet()
    verify_approval()

    try:
        key1 = open('Approval.txt', 'r').read()
    except FileNotFoundError:
        os.system("clear")
        print(LOGO)
        print("[*]_______________________")
        print("  Your Token Is Not Approved Already")
        print("[*]_______________________")
        print("           THIS TOOL IS PAID ")
        print("           THIS IS YOUR KEY BRO")
        print("[*]_______________________")
        print("")
        myid = uuid.uuid4().hex[:10].upper()
        print("          YOUR KEY : " + "MEHRA_KING" + myid)
        print("[*]_______________________")
        kok = open('Approval.txt', 'w')
        kok.close()
        print("")
        print("")
        print("     Copy Key And Sent Me WhatsApp Approval Your Key ")
        print("[*]_______________________")
        sleep(6)

        # Open WhatsApp link with the generated key
        webbrowser.open("https://wa.me/+917643890954?text=Approval%20Key:%20MEHRA_KING" + myid)

        exit()

    r1 = requests.get("https://raw.githubusercontent.com/aaanandsir/MEHRA_KING/main/Approval.txt").text
    if key1 in r1:
        show_menu()
    else:
        print(LOGO)
        print("[*]_______________________")
        print("  Your Token is not approved  ")
        print("[*]_______________________")
        print("THIS IS YOUR KEY BRO")
        print("[*]FIRST APPROVAL KEY THEN RUN")
        print("")
        print("          YOUR KEY : " + "MEHRA_KING" + key1)
        print("[*]_______________________")
        print("     Copy Key And Sent Me WP Approval Your Key ")
        print("[*]_______________________")
        sleep(3.5)
        exit()

def send_message(api_url, cookies, thread_id, full_message):
    try:
        headers = {'Cookie': cookies}
        data = {'message': full_message}
        response = requests.post(api_url, headers=headers, data=data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"{LOGO_COLORS['red']}Error sending message to {thread_id}: {e}{LOGO_COLORS['reset']}")
        return None

def ib_convo_messages():
    try:
        num_cookies = int(input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter the number of sets of Facebook cookies: " + LOGO_COLORS['reset']))
        cookie_list = [input(f"Enter cookies for set {i + 1}: ") for i in range(num_cookies)]

        num_threads = int(input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter the number of thread IDs: " + LOGO_COLORS['reset']))
        thread_ids = [input(f"Enter thread ID {i + 1}: ") for i in range(num_threads)]

        haters_name = input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter your haters name: " + LOGO_COLORS['reset'])
        txt_file_path = input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter the path to your message file (txt): " + LOGO_COLORS['reset'])
        time_interval = int(input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter the time interval between messages (in seconds): " + LOGO_COLORS['reset']))

        for cookies in cookie_list:
            for thread_id in thread_ids:
                with open(txt_file_path, 'r') as file:
                    messages = file.read().splitlines()

                for message in messages:
                    api_url = f'https://graph.facebook.com/{API_VERSION}/t_{thread_id}/'
                    full_message = f'{haters_name} {message}'
                    response = send_message(api_url, cookies, thread_id, full_message)

                    if response and response.status_code == 200:
                        print(LOGO_COLORS['green'] + LOGO_COLORS['bold'] + f"Message sent successfully to {thread_id}: {full_message}" + LOGO_COLORS['reset'])
                    else:
                        logging.error(LOGO_COLORS['red'] + LOGO_COLORS['bold'] + f"Failed to send message to {thread_id}: {full_message}" + LOGO_COLORS['reset'])

                    sleep(time_interval)

    except KeyboardInterrupt:
        logging.info(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "\nScript terminated by user." + LOGO_COLORS['reset'])
    finally:
        return show_menu()

def get_token():
    try:
        username = input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter your Facebook username: " + LOGO_COLORS['reset'])
        password = input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter your Facebook password: " + LOGO_COLORS['reset'])
        token = generate_token(username, password)
        print(LOGO_COLORS['green'] + LOGO_COLORS['bold'] + f"Generated token: {token}" + LOGO_COLORS['reset'])
    except KeyboardInterrupt:
        logging.info(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "\nOperation aborted by user." + LOGO_COLORS['reset'])
    finally:
        return show_menu()

def get_cookies():
    try:
        username = input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter your Facebook username: " + LOGO_COLORS['reset'])
        password = input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter your Facebook password: " + LOGO_COLORS['reset'])
        token = generate_token(username, password)
        cookies = f'c_user={token["c_user"]}; datr={token["datr"]}; fr={token["fr"]}; sb={token["sb"]}; xs={token["xs"]}'
        print(LOGO_COLORS['green'] + LOGO_COLORS['bold'] + f"Generated cookies: {cookies}" + LOGO_COLORS['reset'])
    except KeyboardInterrupt:
        logging.info(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "\nOperation aborted by user." + LOGO_COLORS['reset'])
    finally:
        return show_menu()

def get_token_by_cookie():
    try:
        cookies = input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter Facebook cookies: " + LOGO_COLORS['reset'])
        user = verify_cookies(cookies)
        if user != 'Unknown User':
            print(LOGO_COLORS['green'] + LOGO_COLORS['bold'] + f"User: {user}" + LOGO_COLORS['reset'])
        else:
            print(LOGO_COLORS['red'] + LOGO_COLORS['bold'] + "Invalid cookies. Please check and try again." + LOGO_COLORS['reset'])
    except KeyboardInterrupt:
        logging.info(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "\nOperation aborted by user." + LOGO_COLORS['reset'])
    finally:
        return show_menu()

def get_cookie_by_token():
    try:
        token = input(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "Enter Facebook token: " + LOGO_COLORS['reset'])
        cookies = f'c_user={token["c_user"]}; datr={token["datr"]}; fr={token["fr"]}; sb={token["sb"]}; xs={token["xs"]}'
        print(LOGO_COLORS['green'] + LOGO_COLORS['bold'] + f"Generated cookies: {cookies}" + LOGO_COLORS['reset'])
    except KeyboardInterrupt:
        logging.info(LOGO_COLORS['shiny'] + LOGO_COLORS['bold'] + "\nOperation aborted by user." + LOGO_COLORS['reset'])
    finally:
        return show_menu()

def show_menu():
    while True:
        print(LOGO_COLORS['bold'] + "\nChoose an option:")
        print("1. IB Convo Message")
        print("2. Get Token")
        print("3. Get Cookies")
        print("4. Get Token by Cookie")
        print("5. Get Cookie by Token")
        print("0. Exit" + LOGO_COLORS['reset'])

        option = input(LOGO_COLORS['bold'] + "Enter option (1, 2, 3, 4, 5, or 0): " + LOGO_COLORS['reset'])

        if option == '1':
            return ib_convo_messages()
        elif option == '2':
            return get_token()
        elif option == '3':
            return get_cookies()
        elif option == '4':
            return get_token_by_cookie()
        elif option == '5':
            return get_cookie_by_token()
        elif option == '0':
            print(LOGO_COLORS['bold'] + "Thank you for using the program! Have a nice day." + LOGO_COLORS['reset'])
            exit()
        else:
            print(LOGO_COLORS['red'] + LOGO_COLORS['bold'] + "Invalid option. Try again." + LOGO_COLORS['reset'])

if __name__ == "__main__":
    authenticate_user()
