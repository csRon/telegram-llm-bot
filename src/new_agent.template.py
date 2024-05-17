import assistant
import config
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
        new_agent_specific_task()   
    else:
        # Send the ChatGPT response to the user
        assistant.send_telegram_message(update, context, bot_response)

def new_agent_specific_task():
    pass

def check_for_docsearch_results(update, bot_response) -> str:
    '''
    This function checks if the bot response contains a document path (the bot procedure is finished).
    It return a string with the path to the document or None if not finished.
    '''

    # check if the conversation of the llm ended
    if "FINISHED" in bot_response:
        update.message.reply_text("Document %s will be summarized."%document_path)
        return "Done"
    else:
        return None

