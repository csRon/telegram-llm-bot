from PIL import Image
import pytesseract
import re

import assistant
import config

def handle_user_text(update, context):
    '''
    This function is called when the user sends a text message.
    '''
    print(f"Text message from user {update.message.from_user.first_name} received.")
    user_text = update.message.text

    text_to_llm(update, context, user_text)
    
def handle_user_voice(update, context):
    '''
    This function is called when the user sends a voice message.
    '''
    print(f"Voice message from user {update.message.from_user.first_name} received.")
    user_text = assistant.voice_to_text(update, context)

    text_to_llm(update, context, user_text)

def handle_user_document(update, context):
    '''
    This function is called when the user sends a photo.
    '''
    print(f"Photo from user {update.message.from_user.first_name} received.")
    
    text_of_pictures = []

    scan = update.message.document.get_file()
    path_to_scan = "scans/" + update.message.document.file_name
    scan.download(path_to_scan)

    # Open the scanned image using Pillow (PIL)
    image = Image.open(path_to_scan)

    # Perform OCR to extract text
    text_of_pictures.append(pytesseract.image_to_string(image))
                
    print(text_of_pictures)

    # combine all text to one string  
    user_text = "This is the scanned text: \n\n \"\"\"" + "Page break \n\n\n ".join(text_of_pictures) + "\n\n\"\"\""

    text_to_llm(update, context, user_text)

def text_to_llm(update, context, user_text):
    
    bot_response = assistant.call_llm(update, user_text)

    # check if the user request is finished by the bot
    scan_dict = check_for_scan_results(update, bot_response)
    if scan_dict is not None:
        print("Scan dict will be proceeded: \n")
        print(scan_dict)
        scan_dict=None

        # call this function again to go on with the next step defined in the persona
        text_to_llm(update, context, "Go on with the next step.")
        pass
    else: 
        # Send the ChatGPT response to the user
        assistant.send_telegram_message(update, context, bot_response)
       
def check_for_scan_results(update, bot_response) -> dict:
    '''
    This function checks if the bot response contains json for scan results.
    It returns a dict or None if not finished.
    '''
    # check if the conversation of the llm ended
    if "{" in bot_response and "image_name" in bot_response:
        # find the document name in the bot response
        scan_str = re.findall(r"\{.*\}", bot_response, re.DOTALL)[0]
        scan_dict = eval(scan_str)

        # update.message.reply_text("The mail will be sent.")
        return scan_dict
    else:
        return None
    