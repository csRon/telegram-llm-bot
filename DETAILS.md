# Details
In this file a more detailed description of the software design and how to add new agents is given.

## Software Design
I tried to design the software modular that anyone can easily add new agents with specific context (with medium to bad success admittedly). Generally an agent has a source code (in `src` folder) and a specific context (in `personas` folder). But to add a new agents several changes are necessary.

## Adding new agents
To add a new agent you need make modifications in the following files and folders:
- `personas`-folder: Add a new persona file, e.g. use `new_agent.template.md`  where you describe the persona of the agent. Learn some prompt engineering to get the best results.
- `src`-folder: Add a new source code file, e.g. `new_agent.py` where you implement the agent. You can use the `new_agent.template.py` file as a template. The most important is to add your personal code in the `new_agent_specific_task()` function. This only works when a formal input is given by the llm (e.g. a json).
- `config.py`: In line 24 add the new agent and its name (e.g. NEW_AGENT) and the number of agents (currently 5 - sorry this is not good code but currently no time to fix it) 
- `coobot.py`: Add a new state, e.g.:
    ```python
    config.NEW_AGENT: [
                MessageHandler(Filters.text & ~Filters.command, new_agent.handle_user_text)
            ]
    ```
    and a new fallback command, e.g.:
    ```python
    CommandHandler('new_agent', fallbacks.change_state_to_new_agent)
    ```
- `src/fallback.py`: Add the change state function, e.g.:
    ```python
    def change_state_to_new_agent(update, context):
        '''
        This function is called when the user sends the /new_agent command.
        '''   
        reset_conversation_history()  
        set_language() 
    
        # set the persona to the text in the assistant.md file in the persona folder
        persona = open("personas/new_agent.md", "r").read()  
        set_persona(persona)

        bot_response = assistant.call_llm(update, "Introduce yourself.")
        assistant.send_telegram_message(update, context, bot_response)

        return config.NEW_AGENT
    ```