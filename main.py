from fastapi import FastAPI, HTTPException, Request
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configuración de las API keys
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


# URL de la API de WhatsApp
WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

# Función para enviar mensajes a WhatsApp
def send_whatsapp_message(phone_number, message):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    # print(f"Enviando mensaje a {phone_number}: {message}")  # Para depuración
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
    # print(f"Respuesta de WhatsApp: {response.text}")  # Para depuración
    return response.json()

# Función para interactuar con GPT-4
def get_gpt4_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "user", "content": prompt},
        {"role":"system", "content":"""You are JuanAssistant a virtual assistant specialized in education, designed to help parents with their children's academic performance. Your goal is to provide practical guidance, useful advice, and effective strategies to support student academic success.
        
        Your responsibilities include:
        - Interpreting grades and school reports
        - Suggesting effective study methods according to the student's age and level
        - Offering advice for improvement in specific subjects
        - Proposing ways to motivate students and establish realistic goals
        - Recommending how to communicate effectively with teachers and school
        - Addressing common problems such as procrastination or lack of concentration
        - Suggesting extracurricular activities that complement learning

        When interacting with parents:
        - Ask for specific information about the student (age, grade, problematic subjects, etc.)
        - Offer clear, concise, and tailored responses
        - Use a friendly and encouraging tone
        - Provide concrete examples and actionable steps
        - If necessary, suggest when to seek additional professional help

        Remember that each student is unique. Adapt your advice to individual needs and foster a positive approach to learning and academic growth.
        
        Important: Always provide short and simple answers. Limit your responses to brief, easy-to-understand explanations and suggestions. Avoid long, complex responses.
        """}
    ]
    data = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.6
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    # print(f"Respuesta de GPT-4: {response.text}")  # Para depuración
    return response.json()['choices'][0]['message']['content']

# Endpoint para recibir mensajes de WhatsApp
@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    # print(json.dumps(data, indent=4))  # Para depuración

    # Verifica si el mensaje es válido
    if 'entry' in data:
        for entry in data['entry']:
            for change in entry.get('changes', []):
                value = change.get('value', {})
                if 'messages' in value:
                    for message in value['messages']:
                        phone_number = message.get('from')
                        message_body = message.get('text', {}).get('body')

                        if phone_number and message_body:
                            # Obtén la respuesta de GPT-4
                            # print(f"Mensaje de {phone_number}: {message_body}")  # Para depuración
                            gpt_response = get_gpt4_response(message_body)
                            # gpt_response = "Hola soy el GPT-4o de FacInnova"

                            # Envía la respuesta a WhatsApp
                            send_whatsapp_message(phone_number, gpt_response)
    return {"status": "ok"}

# Endpoint para verificar el webhook (requerido por WhatsApp)
@app.get("/")
async def verify_webhook(request: Request):
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get("hub.challenge"):
        if not request.query_params.get("hub.verify_token") == os.getenv("VERIFY_TOKEN"):
            raise HTTPException(status_code=403, detail="Invalid verification token")
        return int(request.query_params.get("hub.challenge"))
    raise HTTPException(status_code=400, detail="Invalid request!!!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)