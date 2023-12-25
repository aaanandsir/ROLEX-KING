import requests
import logging
from time import sleep
import hashlib
import webbrowser
import os

API_VERSION = 'v15.0'

# Headers remain unchanged
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

# Specify colors for the logo
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

# ASCII art for the logo
LOGO = f"""
{LOGO_COLORS['red']}  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣶⣶⣶⣶⣦⣴⣶⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣬⢿⣿⣿⣿⣿⣿⣿⡙⢿⣿⣿⣿⣿⣿⣶⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣷⡍⠻⢷⠿⢿⠿⢧⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣆⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣆⣰⣶⣆⣀⣾⣿⣿⣿⣿⣿⣿⣿⡿⠿⣥⣾⣿⡀⠀⠀⠀⠀
⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠘⠻⣿⣿⣿⣦⡀⠀⠀
⠀⠿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⠻⣿⣿⣿⣿⣿⣿⣿⣏⣡⣼⣿⣦⣄⠘⢿⣿⣿⣿⣿⡄⠀
⠀⣬⣿⣃⢨⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣼⣿⣿⣿⣿⡷⠀
⠀⠹⣿⣽⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⡿⠛⠉⠉⠙⢿⣿⣿⣿⠁⠀
⠀⠀⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣽⣿⣿⣿⣇⠀⠀⠀⠀⢸⣿⣿⣿⠂⠀
⠀⠀⢹⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢲⣿⣿⣿⣿⣿⣿⣿⣶⠦⠀⣼⣿⣿⣿⣀⡀
⠀⢰⣧⣼⣿⣿⣿⠃⠀⢀⣠⡀⠀⠀⠀⠀⠀⠀⣆⢸⣿⣿⣿⣿⣿⠿⣷⣶⣶⡄⠈⣿⣿⣿⣸⣿
⠀⠘⣿⣿⡞⣿⡏⠀⠚⠛⠉⠙⣧⡀⠀⠀⠈⣦⣻⣾⣿⣿⣻⣿⢏⡴⠋⠁⠀⠀⠀⣿⣿⣿⣿⡿
⠀⠀⠙⢠⣷⢿⣧⠀⠀⢲⣿⣶⣿⣿⣦⡀⢀⣾⣿⣿⣿⣯⣟⣷⣯⣷⣶⣶⣾⣿⣦⣿⡏⣿⡔⠁
⠀⠀⢠⡼⣧⠘⡏⠀⠀⠀⠁⢹⣂⣤⣼⡿⢻⡟⠻⣿⣿⣿⣿⣹⠯⠖⣁⣿⣿⣿⠛⢻⢃⣿⠷⠀
⠀⠀⠀⢣⡨⠿⠉⠀⠀⠀⠀⣀⣈⠉⠁⠀⠀⠀⠀⢿⡃⢸⣿⣿⣿⣿⣿⣿⠋⠉⠀⠈⠾⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⡿⠷⠖⠀⠀⠀⠀⢻⣿⣿⣿⣭⣿⣻⣿⣿⣶⡤⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣯⣇⠀⠀⠀⠀⣀⠀⠀⢸⣿⠇⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠀⠈⠘⣿⣿⣶⣦⣄⣉⠳⠤⣿⣾⣿⣿⣿⠿⣿⡿⢫⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠸⣿⡄⠈⠙⠛⠟⢿⠿⠏⠛⠉⠀⢠⣿⠁⡾⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠸⣄⠀⠀⠹⣿⡓⠲⠤⠀⠀⢀⡤⠴⠞⣻⣿⠃⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠢⠀⠀⠹⣷⣄⡀⡀⣀⢠⢠⣶⣷⡿⠃⠀⢀⢰⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡆⠈⢆⠀⠈⢿⣿⣶⣾⣿⣿⣿⡿⠀⠀⢀⡏⢸⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠘⣆⠀⢀⡈⣻⣿⣿⣿⣷⣦⡀⠀⣾⠇⣼⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣆⠀⠘⣆⠀⠙⠛⠛⣻⠿⣿⣿⠇⣼⡟⣲⠋⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠘⢦⣀⣀⣴⣧⣴⣿⣟⣼⣿⡷⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⢦⣈⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣟⡛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{LOGO_COLORS['glossy']} •========>TH3 L3G3NT K1NG AN9ND M3HR9 🖤 <======•
{LOGO_COLORS['glow']} £ TRUST ME, YOU CAN'T BEAT ME. X —————
"""

# Function to generate a unique key for each user
def generate_user_key():
    return hashlib.sha256(os.urandom(32)).hexdigest()

# Function to open WhatsApp with generated key for approval
def open_whatsapp_for_approval(owner_whatsapp_link, user_key):
    message = f"Anand sir, please approve my key: {user_key}"
    webbrowser.open(f"{owner_whatsapp_link}?text={message}")

# Function to open a GitHub repository link for users to get approval
def open_github_link():
    github_link = "https://github.com/aaanandsir/Approval/blob/main/Anand.txt"
    webbrowser.open(github_link)

# Function to check if the user's key is approved on GitHub
def is_key_approved_on_github(user_key):
    # Implementation to check if the user's key is approved on GitHub
    # Placeholder, replace with actual logic
    return True

# Function to send a message
def send_message(api_url, cookies, thread_id, message):
    parameters = {'message': message}
    try:
        response = requests.post(api_url, data=parameters, headers={'Cookie': cookies})
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending message: {e}")
        return None

def authenticate_user():
    print(LOGO)
    print(LOGO_COLORS['bold'] + "[✓] AUTHOR: ANAND MEHRA" + LOGO_COLORS['reset'])
    print(LOGO_COLORS['bold'] + "[✓] TOOL      : IB CONVO" + LOGO_COLORS['reset'])
    print(LOGO_COLORS['bold'] + "[✓] STATUS :  FREE" + LOGO_COLORS['reset'])
    print(LOGO_COLORS['bold'] + "[✓] FACEBOOK: ANAND MEHRA" + LOGO_COLORS['reset'])
    print(LOGO_COLORS['bold'] + "[✓] WHAT'S APP :+917643890954" + LOGO_COLORS['reset'])
    print(LOGO_COLORS['bold'] + "    ()⁠☞CONTACT FOR PRIVATE SERVER" + LOGO_COLORS['reset'])
    print(LOGO_COLORS['bold'] + "          AND TOOL <3" + LOGO_COLORS['reset'])

    user_key = generate_user_key()
    print(LOGO_COLORS['bold'] + f"Your key: {user_key} dear." + LOGO_COLORS['reset'])
    open_whatsapp_for_approval(owner_whatsapp_link= "https://wa.me/917643890954", user_key=user_key)

    print(LOGO_COLORS['bold'] + "Wait for owner approval on WhatsApp..." + LOGO_COLORS['reset'])
    input("Press Enter after getting approval...")

    return show_menu()

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
    username = input("Enter your Facebook username: ")
    password = input("Enter your Facebook password: ")
    user_name = generate_token(username, password)
    print(LOGO_COLORS['golden'] + LOGO_COLORS['bold'] + f"User Name: {user_name}" + LOGO_COLORS['reset'])
    return f'{username}|{password}', show_menu()

def get_cookies():
    cookies = input("Enter your Facebook cookies: ")
    user_name = verify_cookies(cookies)
    print(LOGO_COLORS['golden'] + LOGO_COLORS['bold'] + f"User Name: {user_name}" + LOGO_COLORS['reset'])
    return cookies, show_menu()

def get_token_by_cookies():
    cookies = input("Enter your Facebook cookies: ")
    user_name = generate_token(*cookies.split('|'))
    print(LOGO_COLORS['golden'] + LOGO_COLORS['bold'] + f"User Name: {user_name}" + LOGO_COLORS['reset'])
    return cookies, show_menu()

def show_menu():
    while True:
        option = input(LOGO_COLORS['bold'] + "\nChoose an option:\n1. Main Menu\n2. Back\n0. Exit\nEnter option (1, 2, or 0): " + LOGO_COLORS['reset'])
        if option == '1':
            return authenticate_user()
        elif option == '2':
            return ib_convo_messages()
        elif option == '0':
            print(LOGO_COLORS['bold'] + "Thank you for using the program! Have a nice day." + LOGO_COLORS['green'])
            exit()
        else:
            print(LOGO_COLORS['red'] + LOGO_COLORS['bold'] + "Invalid option. Try again." + LOGO_COLORS['reset'])

if __name__ == "__main__":
    credentials, _ = authenticate_user()
