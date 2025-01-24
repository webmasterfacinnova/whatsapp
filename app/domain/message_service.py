import json  
import requests
from app.domain.agents.routing_agent import RoutingAgent  
from app.schema import User  

def respond_and_send_message(user_message: str, user: User):  
    agent = RoutingAgent()  
    response = agent.run(user_message, user.id)  
    send_whatsapp_message(user.phone, response, template=False)