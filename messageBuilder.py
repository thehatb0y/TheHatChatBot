import json

def createButtons(L):
    button_template = '''
        {
            "type": "message",
            "text": "Text Placeholder",
            "postback_id": "send_message",
            "user_ids": [],
            "value": "Value Placeholder"
        }
    '''

    buttons = []

    if L == None:
        return False
    
    for item in L:
        button = json.loads(button_template)
        button['text'] = item['text']
        button['value'] = item['value']
        buttons.append(button)
    return buttons
    
def assemblyButtons(fileName):
    with open(fileName, 'r') as f:
        buttons = json.load(f)
    result = createButtons(buttons)
    return result

def checkMessage(id):
    with open('livechatJson/conversation.json', 'r') as f:
        messages = json.load(f) 

    for item in messages:
        if item['conversation'] != "False":
            for message in item['conversation']:
                if message['cvID'] == id:
                    return message['message']
        else:
            if item['id'] == id:
                return item['message']

def checkMessageType(id):
    with open('livechatJson/conversation.json', 'r') as f:
        messages = json.load(f) 

    for item in messages:
        if item['conversation'] != "False":
            for message in item['conversation']:
                if message['cvID'] == id:
                    return message['type']
        else:
            if item['id'] == id:
                return item['type']  

def chooseRichMessageBody(id):
    with open('livechatJson/Rich_message.json', 'r') as f:
        messages = json.load(f) 

    for item in messages:
        if item['id'] == id:
            return item['value']
        
    return False