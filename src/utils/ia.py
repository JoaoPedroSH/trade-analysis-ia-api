from fastapi import HTTPException
from openai import OpenAI, APIError, AuthenticationError
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def enviar_prompt_ia(prompt):
    try:
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"), 
            base_url=os.getenv("DEEPSEEK_API_URL")
        )
        
        response = client.chat.completions.create(
            model=os.getenv("DEEPSEEK_MODEL_TYPE"),
            messages= prompt,
            temperature=0.5,
            max_tokens=300,
            stream=False
        )
        return response.choices[0].message.content
    
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail="Erro de autenticação: " + str(e))
    except APIError as e:
        raise HTTPException(status_code=500, detail="Erro na API: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro inesperado: " + str(e))
