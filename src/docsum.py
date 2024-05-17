import assistant
import config
import PyPDF2
import re


def handle_user_text(update, context):
    '''
    This function is called when the user sends a text message.
    '''
    print(f"Text message from user {update.message.from_user.first_name} received.")
    user_text = update.message.text
    bot_response = assistant.call_llm(update, user_text)

    # check if the user request is finished by the bot
    document_path = check_for_docsearch_results(update, bot_response)
    if document_path is not None:
        extracted_text = get_document_text(document_path)
        summarize_text_by_page(update, extracted_text)
   
    else:
        # Send the ChatGPT response to the user
        assistant.send_telegram_message(update, context, bot_response)

def summarize_text_by_page(update, extracted_text):
    '''
    This function summarizes the text of a document by page and sends the summary to the user.
    '''
    # call llm with the extracted text by page
    for page_number, page_text in enumerate(extracted_text):
        bot_response = assistant.call_llm(update, "Text of Page number %d\n\n"%page_number + page_text)
        update.message.reply_text("Page number %d summary: \n\n"%page_number + bot_response)

def get_document_text(document_path) -> list:
    '''
    This function returns the text of a document separated by pages in a list of strings.
    '''
    pdf_file = open(document_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    pdf_pages = pdf_reader.pages 
    extracted_page_text = []
    for page in pdf_pages:
        extracted_page_text.append(page.extract_text())
    
    # join text to one string with page number at the top of each page
    #extracted_page_text = ["Page number %d:\n\n"%page_number + page_text for page_number, page_text in enumerate(extracted_page_text)][0]
    return extracted_page_text

def check_for_docsearch_results(update, bot_response) -> str:
    '''
    This function checks if the bot response contains a document path (the bot procedure is finished).
    It return a string with the path to the document or None if not finished.
    '''

    # check if the conversation of the llm ended
    if "DOCUMENT_REQUEST" in bot_response:
        # find the document name in the bot response
        document_name = re.findall(r"\'.*\'", bot_response)[0][1:-1]
        document_path = "documents/" + document_name

        update.message.reply_text("Document %s will be summarized."%document_path)

        return document_path
    else:
        return None

