# telegram-llm-bot
Telegram bot that lets you interact with ChatGPT with additional context and some implemented agents. 

![Demo](./video/llm-demo.gif)

## Prerequisites
- Linux computer or WSL (tested on Ubuntu 22.04)
- Tested on Python 3.10
1. Create an OpenAI account and get an API key (see https://platform.openai.com/docs/quickstart for reference)
2. Create a Telegram bot using BotFather (see https://core.telegram.org/bots/tutorial for reference)
3. Enter your secrets and tokens as environment variables (e.g. in an `.env` file or directly in the terminal)
    ```bash
    export OPENAI_API_KEY=<your OpenAI API key>
    export BOT_TOKEN=<your Telegram bot token>
    export BOT_PASSWORD=<your Telegram bot password>
    ```

## Getting started
Create a virtual environment and install dependencies (requires sudo):
```bash
python3 -m venv .venv
source .venv/bin/activate
bash setup.sh
```
To run the bot:
```bash
python3 coobot.py
```

## Available Agents
To access the agents you need to use write a command (delimeted by "/" e.g. `/assistant`). The publicly available agents are:
- `/assistant`: This is the default agent which gives acces to ChatGPT with additional context 
- `/scan`: Send a picture of a text and get a summary
- `/docsearch`: Searches for similar content in the provided document (concept known as "semantic search" or "Retrieval augmented generation - RAG")
- `/docsum`: Summarizes available documents page by page

For more details regarding the software design and how to add new agents see [DETAILS.md](DETAILS.md).

## Known Issues
- No user management: If several users use the bot at the same time, the context is shared between them. 

## Notes
Before ChatGPT announced multimodal features, this project was pretty cool and newish. Many functions are now also implemented in ChatGPT. However, the project is still a good starting point to learn how to interact with the OpenAI API and how to build a Telegram bot.

**I do not take any responsibility for the use of this bot. Use and host it at your own risk.**

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

