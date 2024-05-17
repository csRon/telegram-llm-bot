import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

import config
import assistant
import fallbacks
import docsearch
import docsum
import scan

def start(update, context):
    '''
    This function is called after starting the bot.
    '''
    print(f'Bot started by {update.message.from_user.first_name}')
    
    # check if user is already authorized
    user_id = update.message.from_user.id
    if user_id in config.AUTHORIZED_USERS:
        return fallbacks.change_state_to_assistant(update, context)

    update.message.reply_text("Please enter the password to access the bot.")
    return config.PASSWORD

def ask_for_password(update, context):
    '''
    This function is called after starting and asks the user for the password.
    '''
    user_input = update.message.text

    if (user_input == config.BOT_PASSWORD):
        print(f"User {update.message.from_user.first_name} entered correct password")
        update.message.reply_text("Access granted. You can now use the bot.")
        
        # add user to authorized users
        config.AUTHORIZED_USERS.append(update.message.from_user.id)

        return fallbacks.change_state_to_assistant(update, context)
    else:
        print(f"User {update.message.from_user.first_name} entered incorrect password")
        update.message.reply_text("Incorrect password. Please try again.")
        return config.PASSWORD

def main():
    print(f"Server started. Bot name is {config.bot.get_me().username}")
    
    updater = telegram.ext.Updater(token=config.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            config.PASSWORD: [MessageHandler(Filters.text & ~Filters.command, ask_for_password)],
            config.ASSISTANT: [
                MessageHandler(Filters.text & ~Filters.command, assistant.text_to_llm), 
                MessageHandler(Filters.voice & ~Filters.command, assistant.voice_to_llm),
                MessageHandler(Filters.document & ~Filters.command, assistant.save_file_in_documents)

            ],
            config.DOCSEARCH: [
                MessageHandler(Filters.text & ~Filters.command, docsearch.handle_user_text)
            ],
            config.DOCSUM: [
                MessageHandler(Filters.text & ~Filters.command, docsum.handle_user_text)
            ],
            config.SCAN: [
                MessageHandler(Filters.text & ~Filters.command, scan.handle_user_text),
                MessageHandler(Filters.voice & ~Filters.command, scan.handle_user_voice),
                MessageHandler(Filters.document & ~Filters.command, scan.handle_user_document)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', fallbacks.cancel),
            CommandHandler('assistant', fallbacks.change_state_to_assistant),
            CommandHandler("docsearch", fallbacks.change_state_to_docsearch),
            CommandHandler("docsum", fallbacks.change_state_to_docsum),
            CommandHandler("scan", fallbacks.change_state_to_scan),
            CommandHandler('voice', fallbacks.change_to_voice_output),
            CommandHandler('text', fallbacks.change_to_text_output)
        ]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()