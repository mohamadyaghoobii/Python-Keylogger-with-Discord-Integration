# Python Keylogger with Discord Integration

This is an advanced Python keylogger for ethical hacking demonstrations. It logs keystrokes, tracks the active window, and periodically sends encrypted logs to a Discord channel using a webhook.

## Features:
- Logs keystrokes and records the active window.
- Encrypts logs before sending them to Discord.
- Sends periodic reports of keystrokes and system information to a Discord webhook.
- Cross-platform support (Windows, Linux, macOS).

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mohamadyaghoobii/Python-Keylogger-with-Discord-Integration.git
   cd Python-Keylogger-with-Discord-Integration


2.Install dependencies:
pip install -r requirements.txt

3.Set up a Discord webhook and replace the WEBHOOK_URL in main.py with your own webhook URL.

4.Run the keylogger:
python main.py

5.(Optional) To run the keylogger in the background without a console, convert it to an executable (for Windows):
pyinstaller --noconsole --onefile main.py

Ethical Use
This project is intended for educational purposes only. Ensure that you have permission to run it on any system. Unauthorized use of keyloggers is illegal.

Ikarus web
