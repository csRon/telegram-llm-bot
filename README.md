# coobot
Telegram bot that lets you interact with ChatGPT with additional context and some implemented agents. 

## Prerequisites
- Linux computer or WSL (tested on Ubuntu 22.04)
- Tested on Python 3.8.10
- Create an OpenAI account and get an API key (see https://beta.openai.com/docs/guides/authentication for reference)
- Create a Telegram bot using BotFather (see https://platform.openai.com/docs/quickstart for reference)
- Enter your secrets and tokens as environment variables (e.g. in an `.env` file or directly in the terminal)
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

## Notes
**I do not take any responsibility for the use of this bot. Use and host it at your own risk.**

