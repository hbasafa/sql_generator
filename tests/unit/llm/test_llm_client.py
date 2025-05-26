import requests
from openai import OpenAI
from src.app import settings


def test_ollama_client():

    client = OpenAI(api_key="key", base_url=f"{settings.TEST_LLM_BASE_URL}")

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Just Say hello!"}
            ],
            model=settings.TEST_LLM_MODEL_NAME,
        )
        assert "Hello" in response.choices[0].message.content
    except Exception as e:
        raise Exception("Error generating SQL query!")


def test_ollama_api():
    response = requests.post(f"http://{settings.TEST_LLM_HOST}:{settings.TEST_LLM_CONTAINER_PORT}/api/generate", json={
            "model": settings.TEST_LLM_MODEL_NAME,
            "prompt": "Just say hello!",
            "stream": False
        })
    assert "response" in response.json()
