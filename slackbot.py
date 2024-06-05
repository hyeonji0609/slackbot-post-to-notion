import os
import dotenv 
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_for_slack import ChatGPT
from notion import Notion

# loading env
dotenv.load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.command("/create_db")
def app_command_handler(ack, body, respond): 
    # Acknowledge command request
    ack()
    
    try:
        text = body["text"].split('/')
        
        '''
        input example
        -------------
        page_id : [page_id] / title : [title]
        '''
        page_id = text[0].split(':')[1].strip()
        title = text[1].split(':')[1].strip()

        create_db_json_path = './json/create_db.json'

        notion = Notion(create_db_json_path)
        result = notion.create_db(page_id, title)

        respond("Database created successfully")

    except Exception as e:
        say(f"Error: {str(e)}")

@app.message(".*")
def message_handler(body, message, say):
    event_ts = body["event"]["ts"]
    text = body["event"]["text"]
    
    try:
        # summarize content
        chatgpt = ChatGPT()
        summary, url = chatgpt.langchain(text)
        
        say(text = summary, thread_ts=event_ts)

        # update to notion
        update_db_json_path = './json/update_db.json'
        
        notion = Notion(update_db_json_path)
        result = notion.update_db(summary, url)

        say(text="Database update completed successfully.", thread_ts=event_ts)


    except Exception as e:
        say(f"Error: {str(e)}")
        say(text = "Sorry, but it's down.", thread_t=event_ts)

# Start app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()