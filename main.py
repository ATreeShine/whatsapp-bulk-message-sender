import pyautogui
import time
import random
import re
import os
import sys
import pyperclip

# Disable PyAutoGUI failsafe for automation
pyautogui.FAILSAFE = False

class WhatsAppNameNumberSender:
    def __init__(self, edit_icon_path, contact_template_path, message_box_template_path):
        self.delay = 1.5
        self.edit_icon_path = edit_icon_path
        self.contact_template_path = contact_template_path
        self.message_box_template_path = message_box_template_path
        self.contact_names = [
            "tets", "saf", "Hassadgan", "adg", "adg", "adg", "Rashsfhid", "sfh",
            "adg", "vn", "dgk", "zcbz", "dkh", "dudg", "vcnnnsf",
            "jxgh", "sgj", "dhk", "dggghd", "dghsh", "sfhsh", "esr"
        ]

    def find_and_click(self, image_path, timeout=10, confidence=0.7, click=True):
        """Wait for an image on screen, click it, and return its location."""
        print(f"  -> Searching for image: {os.path.basename(image_path)}")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location:
                    center = pyautogui.center(location)
                    if click:
                        pyautogui.click(center)
                        time.sleep(self.delay)
                    return center
            except Exception as e:
                print(f"DEBUG: Error locating image: {e}")
            time.sleep(0.5)
        print(f"  -> Error: Could not find '{os.path.basename(image_path)}' on screen after {timeout} seconds.")
        return None

    def type_text(self, text, interval=0.05):
        pyautogui.typewrite(text, interval=interval)
        time.sleep(0.5)

    def paste_text(self, text):
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

    def press_key(self, key):
        pyautogui.press(key)
        time.sleep(0.5)

    def send_single_message(self, phone_number, message):
        """Sends a message using the 'name+number' format."""
        try:
            # 1. Generate a random name and format the string
            random_name = random.choice(self.contact_names)
            search_string = f"{random_name}{phone_number}"
            print(f"  Using search string: {search_string}")

            # 2. Click the 'New Chat' (edit) icon
            if not self.find_and_click(self.edit_icon_path):
                return False

            # 3. Type the 'name+phonenumber' string
            self.type_text(search_string)
            time.sleep(2)  # Wait for search results

            # 4. Find the 'Not in your contacts' text
            print(f"  Looking for 'Not in your contacts' text...")
            contact_label_pos = self.find_and_click(self.contact_template_path, timeout=5, click=False)

            if not contact_label_pos:
                print(f"  Contact for {phone_number} not found. Skipping.")
                self.press_key('esc') # Clear the search field
                return False

            # 5. Click below the found text to select the contact
            click_x = contact_label_pos.x
            click_y = contact_label_pos.y + 50 # Adjust this offset if needed
            print(f"  Contact label found. Clicking at ({click_x}, {click_y}) to open chat.")
            pyautogui.click(click_x, click_y)
            time.sleep(2)  # Wait for chat to open

            # 6. Find and click the message input field
            print("  Looking for message input field...")
            if not self.find_and_click(self.message_box_template_path, timeout=5):
                print("  Could not find message input field. Skipping.")
                self.press_key('esc')
                return False

            # 7. Paste the message and send
            self.paste_text(message)
            self.press_key('enter')

            print(f"\u2713 Message sent to {phone_number}")
            return True

        except Exception as e:
            print(f"\u2717 Failed to send to {phone_number}: {e}")
            self.press_key('esc') # Try to escape any dialogs
            return False

    def read_phone_numbers(self, file_path):
        try:
            with open(file_path, 'r') as f:
                numbers = [line.strip() for line in f if line.strip()]
            return [re.sub(r'[^0-9+]', '', num) for num in numbers]
        except FileNotFoundError:
            return []

    def read_message(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""

    def run(self, phone_file, msg_file):
        print("=== WhatsApp Name+Number Sender ===\n")
        print("IMPORTANT: Make sure WhatsApp Desktop is open and active!")
        print("Starting in 5 seconds...\n")
        for i in range(5, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)

        phone_numbers = self.read_phone_numbers(phone_file)
        message = self.read_message(msg_file)

        if not phone_numbers or not message:
            print("Error: Check phone_numbers.txt and message.txt files.")
            return

        print(f"\nFound {len(phone_numbers)} numbers. Starting process...\n")
        successful, failed = 0, 0

        for i, number in enumerate(phone_numbers, 1):
            print(f"[{i}/{len(phone_numbers)}] Processing: {number}")
            if self.send_single_message(number, message):
                successful += 1
            else:
                failed += 1
            if i < len(phone_numbers):
                time.sleep(3)

        print("\n=== Summary ===")
        print(f"Total: {len(phone_numbers)}, Successful: {successful}, Failed: {failed}")
        print("\nProcess completed!")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    edit_icon_file = os.path.join(current_dir, 'edit_icon.png')
    contact_template_file = os.path.join(current_dir, 'not_in_contacts.png')
    message_box_file = os.path.join(current_dir, 'send_msg_chat.png')
    phone_file = os.path.join(current_dir, 'phone_numbers.txt')
    msg_file = os.path.join(current_dir, 'message.txt')

    # Check for all required image files
    required_images = {
        "New Chat Icon": edit_icon_file,
        "'Not in Contacts' Label": contact_template_file,
        "Message Box": message_box_file
    }
    for name, path in required_images.items():
        if not os.path.exists(path):
            print(f'Error: {name} image not found at "{path}"')
            sys.exit(1)

    try:
        sender = WhatsAppNameNumberSender(edit_icon_file, contact_template_file, message_box_file)
        sender.run(phone_file, msg_file)
    except KeyboardInterrupt:
        print("\nProcess stopped by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        print("\nPress Enter to exit...")
        input()
