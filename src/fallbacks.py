from telegram.ext import ConversationHandler
import config
import glob
import os
import assistant

def change_state_to_assistant(update, context):
    '''
    This function is called when the user sends the /assistant command.
    '''   
    reset_conversation_history()  
    set_language() 
 
    # set the persona to the text in the assistant.md file in the persona folder
    persona = open("personas/assistant.md", "r").read()  
    set_persona(persona)

    bot_response = assistant.call_llm(update, "Introduce yourself.")
    assistant.send_telegram_message(update, context, bot_response)

    return config.ASSISTANT

def change_state_to_docsearch(update, context):
    '''
    This function is called when the user sends the /docsearch command.
    '''
    reset_conversation_history()
    set_language()

    # set the persona to the text in the assistant.md file in the persona folder
    persona = open("personas/docsearch.md", "r").read() 
    set_persona(persona)

    # add the document list to the persona
    # list just the pdf files in the documents folder
    files = glob.glob("documents/*.pdf")
    
    # create a string with the list of files and number them
    files_string = "\n".join([f"{index+1}: {file[10:]}" for index, file in enumerate(files)])

    set_persona("This is the list of available documents: <<<\n" + files_string + "\n>>>")

    bot_response = assistant.call_llm(update, "Follow the given procedure.")
    assistant.send_telegram_message(update, context, bot_response)

    return config.DOCSEARCH    

def change_state_to_docsum(update, context):
    '''
    This function is called when the user sends the /docsum command.
    '''
    reset_conversation_history()
    set_language()

    # set the persona to the text in the assistant.md file in the persona folder
    persona = open("personas/docsum.md", "r").read() 
    set_persona(persona)

    # add the document list to the persona
    # list just the pdf files in the documents folder
    files = glob.glob("documents/*.pdf")
    
    # create a string with the list of files and number them
    files_string = "\n".join([f"{index+1}: {file[10:]}" for index, file in enumerate(files)])

    set_persona("This is the list of available documents: <<<\n" + files_string + "\n>>>")

    bot_response = assistant.call_llm(update, "Follow the given procedure.")
    assistant.send_telegram_message(update, context, bot_response)

    return config.DOCSUM

def change_state_to_scan(update, context):
    '''
    This function is called when the user sends the /scan command.
    '''
    reset_conversation_history()
    set_language()

    # set the persona to the text in the assistant.md file in the persona folder
    persona = open("personas/scan.md", "r").read() 
    set_persona(persona)

    bot_response = assistant.call_llm(update, "Follow the given procedure.")
    assistant.send_telegram_message(update, context, bot_response)

    return config.SCAN

def change_to_voice_output(update, context):
    '''
    This function is called when the user sends the /voice command.
    '''
    config.VOICE = True
    update.message.reply_text("Voice mode activated.")
    # state should not be changed
    return None

def change_to_text_output(update, context):
    '''
    This function is called when the user sends the /text command.
    '''
    config.VOICE = False
    update.message.reply_text("Text mode activated.")
    # state should not be changed
    return None

def cancel(update, context):
    '''
    This function is called in fallbacks and ends the conversation.
    '''
    update.message.reply_text("Bot access canceled.")
    return ConversationHandler.END

def reset_conversation_history():
    '''
    This function resets the conversation history.
    '''
    config.conversation_history = []

def set_language():
    '''
    This function sets the default language.
    '''
    set_persona("Always answer in the following language: %s"%config.LANGUAGE)

def set_persona(persona):
    '''
    This function sets the persona.
    '''
    config.conversation_history.append({"role": "system", "content": persona})