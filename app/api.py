import requests
import os
from utils import get_redis_client

redis_client = get_redis_client()

async def generate_text(prompt):
    cached_response = redis_client.get(prompt)
    if cached_response:
        return cached_response.decode('utf-8')
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/generate",
            headers={"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"},
            json={"prompt": prompt, "max_tokens": 100}
        )
        response.raise_for_status()
        ai_text = response.json()['choices'][0]['text']
        redis_client.set(prompt, ai_text, ex=3600)
        return ai_text
    except Exception as e:
        print(f"Ошибка: {e}")
        return "Произошла ошибка при генерации текста."

async def generate_image(prompt):
    try:
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers={"Authorization": f"Token {os.getenv('REPLICATE_API_KEY')}"},
            json={
                "version": "stability-ai/stable-diffusion",  # Модель Stable Diffusion
                "input": {"prompt": prompt}
            }
        )
        response.raise_for_status()
        prediction_id = response.json()['id']

        # Ожидаем завершения генерации
        image_url = None
        while not image_url:
            status_response = requests.get(
                f"https://api.replicate.com/v1/predictions/{prediction_id}",
                headers={"Authorization": f"Token {os.getenv('REPLICATE_API_KEY')}"}
            )
            status_response.raise_for_status()
            status_data = status_response.json()
            if status_data['status'] == 'succeeded':
                image_url = status_data['output'][0]
            else:
                await asyncio.sleep(2)  # Ждем 2 секунды перед повторной проверкой

        return image_url
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
