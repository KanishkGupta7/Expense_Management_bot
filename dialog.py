import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "whatsapp-bot-lhheau-858b33cc8788.json"
#from webhook import reply_whatsapp
import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "whatsapp-bot-lhheau"

def detect_intent_from_text(text, session_id, language_code='en'):
    print(text)
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    #print(response)
        
    return  response.query_result.fulfillment_text   
        


def fetch_reply(query, session_id):
	response = detect_intent_from_text(query,session_id)
	return response

