import openai
import whisper
from gtts import gTTS
import os

import config

def voice_to_text(update, context):
    '''
    This function is called when the user sends a voice message and converts to text
    '''
    whisper_model = whisper.load_model("base")
    voice_file = config.bot.get_file(update.message.voice.file_id) 
    voice_file.download("voice_message.ogg")
    # use default language
    user_text = whisper_model.transcribe("voice_message.ogg", language=config.LANGUAGE)['text']
    update.message.reply_text(f"Your voice message was: {user_text}")
    return user_text

def voice_to_llm(update, context):
    '''
    This function is called when the user sends a voice message.
    The voice message is downloaded and transcribed using the whisper library.
    '''
    print(f"Voice message from user {update.message.from_user.first_name} received.")
    user_text = voice_to_text(update, context)

    bot_response = call_llm(update, user_text)

    # Send the ChatGPT response to the user
    # update.message.reply_text(bot_response)
    send_telegram_message(update, context, bot_response)
 
def text_to_llm(update, context):        
    '''
    This function is called when the user sends a text message.
    '''
    print(f"Text message from user {update.message.from_user.first_name} received.")
    user_text = update.message.text
    
    bot_response = call_llm(update, user_text)

    # Send the ChatGPT response to the user
    # update.message.reply_text(bot_response)
    send_telegram_message(update, context, bot_response)

def call_llm(update, user_text):
    '''
    This function sends the user input to the ChatGPT API and returns the response.
    '''
    # Append the user's message to the conversation history
    config.conversation_history.append({"role": "user", "content": user_text})

    # Send the conversation history to ChatGPT
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",  # You can use "gpt-3.5-turbo" for faster responses
        messages = config.conversation_history,
        temperature=0,
    )

    # Get the bot's reply from the response
    bot_response = response.choices[0].message["content"]

    # Append the bot's reply to the conversation history
    config.conversation_history.append({"role": "system", "content": bot_response})

    return bot_response

def save_file_in_documents(update, context):
    '''
    This function is called when the user sends a document.
    '''
    # save the file in the documents folder
    file = update.message.document.get_file()
    file.download("documents/" + update.message.document.file_name)

    update.message.reply_text("File saved in documents folder.")

def send_telegram_message(update, context, message):
    '''
    This function sends a message to the user.
    '''
    if config.VOICE==True:
        # answer with voice message
        tts = gTTS(message, lang=config.LANGUAGE)
        tts.save("voice_message.mp3")
        config.bot.send_voice(chat_id=update.message.chat_id, voice=open('voice_message.mp3', 'rb'))
        # delete voice message file
        os.remove("voice_message.mp3")
    
    # answer with text message no matter if voice mode is activated or not
    update.message.reply_text(message)