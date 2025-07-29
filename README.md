# WhatsApp Desktop Contact Adder (v2)

This script automates adding multiple contacts to WhatsApp Desktop by following these exact steps:
1. Clicks the edit/pencil icon (top right)
2. Selects "New Contact" from the dropdown
3. Fills in first name, last name, and phone number
4. Saves the contact

## Prerequisites

1. Python 3.7 or higher
2. WhatsApp Desktop installed and logged in
3. Required Python packages (install using `pip install -r requirements.txt`)

## How to Use

1. **Prepare your phone numbers file**:
   - Create a file named `phone_numbers.txt` in the same directory as the script
   - Add one phone number per line, with country code (e.g., +8801712345678)
   - You can use the existing `phone_numbers.txt` file as an example

2. **Run the script**:
   ```
   python whatsapp_add_contacts_v2.py
   ```

3. **Important**:
   - Make sure WhatsApp Desktop is open and visible on your screen
   - The script will start after a 5-second countdown
   - Keep your mouse and keyboard idle while the script is running
   - Each contact will be added with a random first and last name

## Adjusting the Script

If the script can't find the correct UI elements, you may need to adjust these values in the script:

1. `edit_icon_x` and `edit_icon_y`: The position of the edit/pencil icon
2. `new_contact_y`: The position of the "New Contact" option relative to the edit icon

## Troubleshooting

- If the script gets stuck, move your mouse to a corner to stop it
- Check the console for any error messages
- Make sure WhatsApp Desktop is the active window
- The script includes delays between actions - you can adjust these if needed

## Requirements

- pyautogui
- pillow (for image recognition)

Install all requirements with:
```
pip install -r requirements.txt
```
