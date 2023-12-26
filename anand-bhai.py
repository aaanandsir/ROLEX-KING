import requests
import logging
from time import sleep

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
    'bold': '\033[1m',
    'reset': '\033[0m',
    'red': '\033[91m',
    'green': '\033[92m'
}

def verify_cookies(cookies):
    try:
        api_url = f'https://graph.facebook.com/{API_VERSION}/me/'
        response = requests.get(api_url, headers={'Cookie': cookies})
        response.raise_for_status()
        user_data = response.json()
        return user_data.get('name', 'Unknown User')
    except requests.exceptions.RequestException as e:
        logging.error(f"{LOGO_COLORS['red']}Error verifying cookies: {e}{LOGO_COLORS['reset']}")
        return 'Unknown User'

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
        num_cookies = int(input(LOGO_COLORS['bold'] + "Enter the number of sets of Facebook cookies: " + LOGO_COLORS['reset']))
        cookie_list = [input(f"Enter cookies for set {i + 1}: ") for i in range(num_cookies)]

        num_threads = int(input(LOGO_COLORS['bold'] + "Enter the number of thread IDs: " + LOGO_COLORS['reset']))
        thread_ids = [input(f"Enter thread ID {i + 1}: ") for i in range(num_threads)]

        haters_name = input(LOGO_COLORS['bold'] + "Enter your haters name: " + LOGO_COLORS['reset'])
        txt_file_path = input(LOGO_COLORS['bold'] + "Enter the path to your message file (txt): " + LOGO_COLORS['reset'])
        time_interval = int(input(LOGO_COLORS['bold'] + "Enter the time interval between messages (in seconds): " + LOGO_COLORS['reset']))

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
        logging.info(LOGO_COLORS['bold'] + "\nScript terminated by user." + LOGO_COLORS['reset'])
    finally:
        return show_menu()

def get_token():
    try:
        username = input(LOGO_COLORS['bold'] + "Enter your Facebook username: " + LOGO_COLORS['reset'])
        password = input(LOGO_COLORS['bold'] + "Enter your Facebook password: " + LOGO_COLORS['reset'])
        token = generate_token(username, password)
        print(LOGO_COLORS['green'] + LOGO_COLORS['bold'] + f"Generated token: {token}" + LOGO_COLORS['reset'])
    except KeyboardInterrupt:
        logging.info(LOGO_COLORS['bold'] + "\nOperation aborted by user." + LOGO_COLORS['reset'])
    finally:
        return show_menu()

def get_cookies():
    try:
        username = input(LOGO_COLORS['bold'] + "Enter your Facebook username: " + LOGO_COLORS['reset'])
        password = input(LOGO_COLORS['bold'] + "Enter your Facebook password: " + LOGO_COLORS['reset'])
        cookies = generate_cookies(username, password)
        print(LOGO_COLORS['green'] + LOGO_COLORS['bold'] + f"Generated cookies: {cookies}" + LOGO_COLORS['reset'])
    except KeyboardInterrupt:
        logging.info(LOGO_COLORS['bold'] + "\nOperation aborted by user." + LOGO_COLORS['reset'])
    finally:
        return show_menu()

def get_token_by_cookie():
    try:
        cookies = input(LOGO_COLORS['bold'] + "Enter Facebook cookies: " + LOGO_COLORS['reset'])
        user = verify_cookies(cookies)
        if user != 'Unknown User':
            print(LOGO_COLORS['green'] + LOGO_COLORS['bold'] + f"User: {user}" + LOGO_COLORS['reset'])
        else:
            print(LOGO_COLORS['red'] + LOGO_COLORS['bold'] + "Invalid cookies. Please check and try again." + LOGO_COLORS['reset'])
    except KeyboardInterrupt:
        logging.info(LOGO_COLORS['bold'] + "\nOperation aborted by user." + LOGO_COLORS['reset'])
    finally:
        return show_menu()

def get_cookie_by_token():
    try:
        token = input(LOGO_COLORS['bold'] + "Enter Facebook token: " + LOGO_COLORS['reset'])
        cookies = generate_cookies_from_token(token)
        print(LOGO_COLORS['green'] + LOGO_COLORS['bold'] + f"Generated cookies: {cookies}" + LOGO_COLORS['reset'])
    except KeyboardInterrupt:
        logging.info(LOGO_COLORS['bold'] + "\nOperation aborted by user." + LOGO_COLORS['reset'])
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
    show_menu()
