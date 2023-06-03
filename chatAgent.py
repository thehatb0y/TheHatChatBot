from time import sleep
import requests
import json
import messageBuilder

token = "x"
agentEmail = "x"
mB = messageBuilder

def listChat():
    url = "https://api.livechatinc.com/v3.5/agent/action/list_chats"

    payload = json.dumps({})
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',
    'limit': '1'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    save = response.json()
    with open('chat.json', 'w') as f:
        json.dump(save, f)
    

    return response

def sendtext(chat_id, text):
    url = "https://api.livechatinc.com/v3.5/agent/action/send_event"
    payload = json.dumps({
    "chat_id": f"{chat_id}",
    "event": {
        "type": "message",
        "text": f"{text}",
        "visibility": "all"
    }
    })
    headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code

def sendRichtext(chat_id, text, fileName):
    url = "https://api.livechatinc.com/v3.5/agent/action/send_event"
    payload = json.dumps({
    "chat_id": f"{chat_id}",
    "event": {
        "type": "rich_message",
        "visibility": "all", 
        "template_id": "quick_replies",
        "elements": [{
            "title": f'{text}',
            "buttons": mB.assemblyButtons(fileName)
        }]
    }   
    })

    headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code

def getChat(chat_id, thread_id): # Not Usable yet
    url = "https://api.livechatinc.com/v3.5/agent/action/get_chat"

    payload = json.dumps({
    "chat_id": f"{chat_id}",
    "thread_id": f"{thread_id}"
    })
    headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    with open('chat.json', 'w') as f:
        json.dump(response.json(), f)
    return response

def getLastMessage(chat_id):
    response = listChat()
    data = response.json()
    for chat in data['chats_summary']:
        if "last_thread_summary" in chat:
            if chat['last_thread_summary']['active'] == True:
                if chat['id'] == chat_id:
                    return chat['last_event_per_type']['message']['event']['text']

def isChatActive(chat_id):
    response = listChat()
    data = response.json()
    for chat in data['chats_summary']:
        if "last_thread_summary" in chat:
            if chat['last_thread_summary']['active'] == True:
                if chat['id'] == chat_id:
                    return True
    return False

def checkWhoSendLastMessage(chat_id):
    response = listChat()
    data = response.json()
    for chat in data['chats_summary']:
        if "last_thread_summary" in chat:
            if chat['last_thread_summary']['active'] == True:
                if chat['id'] == chat_id:
                    return chat['last_event_per_type']['message']['event']['author_id']

def checkWhoSendLastRichMessage(chat_id):
    response = listChat()
    data = response.json()
    for chat in data['chats_summary']:
        if "last_thread_summary" in chat:
            if chat['last_thread_summary']['active'] == True:
                if chat['id'] == chat_id:
                    return chat['last_event_per_type']['rich_message']['event']['author_id']

def sendTheMessage(message, chat_id):
    if mB.checkMessageType(getLastMessage(chat_id)) == "message":
        sendtext(chat_id, message)
    elif mB.checkMessageType(getLastMessage(chat_id)) == "rich_message":
        sendRichtext(chat_id, message, mB.chooseRichMessageBody(getLastMessage(chat_id)))
        sleep(10)

def chatAgent(chat_id, chatThreadList):
    
    sendRichtext(chat_id, mB.checkMessage("Welcome"), mB.chooseRichMessageBody("Welcome"))
    while(getLastMessage(chat_id) != "bye"):
        lastMessage = getLastMessage(chat_id)
        message = mB.checkMessage(lastMessage) # Devolve a mensagem a ser enviada
        if checkWhoSendLastMessage(chat_id) == agentEmail:
            
            sleep(1)
        else:
            if message != False:
                if message != lastMessage and message != None:
                    sendTheMessage(message, chat_id)

        if isChatActive(chat_id) == False:
            chatThreadList.remove(chat_id)
            break

    sendtext(chat_id, mB.checkMessage("Thank You"))    

def getCustomerList():# Get the Customer list for agentEmail return a list of chat_id
    list = []
    response = listChat()
    if response.status_code == 401:
        print("Token invalido")
        return
    
    data = response.json()
    for chat in data['chats_summary']:
        if "last_thread_summary" in chat:
            if chat['last_thread_summary']['active'] == True:
                for user in chat['users']:
                    if user['email'] == agentEmail and user['type'] == "agent" and user['present'] == True:
                        if chat['users'][0]['email']== "mts.c@live.com":                                                    
                            list.append(chat['id'])
    return list

def main():
    chatList = []
    chatThreadList = []
    response = listChat()

    if response.status_code == 401:
        print("Invalid Token")
        return
        
    while response.status_code == 200:
        chatList = getCustomerList()

        if len(chatList) > 0:
            for chat in chatList:
                if chat not in chatThreadList:
                    chatThreadList.append(chat)
                    print(chatThreadList)
                    chatAgent(chat, chatThreadList)
        sleep(5)            
        response = listChat()

if __name__ == "__main__":
    main()

