import config
import assistant
import re

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def handle_user_text(update, context):
    '''
    This function is called when the user sends a text message.
    '''
    print(f"Text message from user {update.message.from_user.first_name} received.")
    user_text = update.message.text
    bot_response = assistant.call_llm(update, user_text)
   
    # check if the user request is finished by the bot
    docsearch_dict = check_for_docsearch_results(update, bot_response)
    if docsearch_dict is not None:
        create_embeddings(update, docsearch_dict)
    else:
        # Send the ChatGPT response to the user
        assistant.send_telegram_message(update, context, bot_response)
        
def create_embeddings(update, docsearch_dict):

    embedding = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)

    documents = []

    for document_name in docsearch_dict['documents']:
        document_path = "documents/" + document_name

        # load document
        document_loader = PyPDFLoader(document_path)
        documents.extend(document_loader.load())

    # Split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 600,
        chunk_overlap = 200
    )        
    splits = text_splitter.split_documents(documents)  

    #print(splits)
    # split splits into chunks of 166
    splits = [splits[i:i + 166] for i in range(0, len(splits), 166)]

    # Embeddings
    vectorstore_directory = 'vectorstore/'
    for split in splits:
        vectordb = Chroma.from_documents(
            documents=split,
            embedding=embedding,
            persist_directory=vectorstore_directory
        )

    # similarity search
    #similar_splits = vectordb.similarity_search(docsearch_dict['query'],k=3)
    similar_splits = vectordb.similarity_search_with_score(docsearch_dict['query'],k=3)
    print(similar_splits)
    for similar in similar_splits:
        update.message.reply_text(similar[0].page_content)
        update.message.reply_text(similar[0].metadata["page"]) 
        update.message.reply_text(similar[1])

    
def check_for_docsearch_results(update, bot_response) -> dict:
    '''
    This function checks if the bot response contains a json with the documents and the search query (the bot procedure is finished).
    It return a dict with the documents and the search query or None if not finished.
    '''

    # check if the conversation of the llm ended
    if "{" in bot_response:
        # find the docsearch_result json in the bot response
        docsearch_string = re.findall(r"\{.*\}", bot_response, re.DOTALL)[0]
        # convert json string to dict
        docsearch_dict = eval(docsearch_string)

        update.message.reply_text("The documents will be searched for the query.")

        return docsearch_dict
    else:
        return None

    