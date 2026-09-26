# Lab 16 — Building the LLM Service

### Step 1 — Sending a request to the model
**File:** app/services/llm_service.py
**Lang:** python

```python
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


class LLMService:
    """Thin wrapper around the local Ollama model."""

    def __init__(self, model: str = "llama3"):
        self.model = model

    def send_request(self, message: str, system: str | None = None) -> str:
        payload = {
            "model": self.model,
            "prompt": message,
            "stream": False,
        }
        if system:
            payload["system"] = system

        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if response.status_code != 200:
            raise RuntimeError(f"Model request failed: {response.status_code}")

        data = response.json()
        return data.get("response", "").strip()

    def is_ready(self) -> bool:
        return bool(self.model)
```

**Walkthrough:**
@ send_request
Inside this file, we are going to add a new function called send request. This function is responsible for taking the user's message and sending it to our local model through Ollama, and then returning the model's reply back to the caller.

@ "def send_request"
Look at the signature first. The first parameter gives us the user's message. The second parameter lets us pass an optional system prompt, so we can shape how the model behaves.

@ 13-17
Here, we build the payload that will be sent to the model. We set the model name, we pass the user's message as the prompt, and we turn off streaming so that we receive the full response in one piece.

@ "if system:"
This part is optional. If a system prompt was provided, we add it to the payload so the model follows those instructions.

@ "response = requests.post"
Now we actually send the request. We post our payload to the Ollama endpoint and wait for the model to respond.

@ "if response.status_code != 200:"
This condition protects us from continuing when the request fails. If the status code is not two hundred, we raise a clear error instead of returning something broken.

@ 25-26
Finally, we read the JSON response, pull out the generated text, and return it to the caller. Now that this function is ready, our Streamlit application can use it to get answers from the model.

### Step 2 — Calling the service from the chatbot
**File:** app/chatbot.py
**Lang:** python

```python
import streamlit as st
from app.services.llm_service import LLMService

service = LLMService()


def handle_user_message(message: str) -> str:
    st.session_state.history.append({"role": "user", "content": message})

    reply = service.send_request(message)

    st.session_state.history.append({"role": "assistant", "content": reply})
    return reply
```

**Walkthrough:**
@ handle_user_message
Now that our service can talk to the model, we need to call it from the chatbot. This function runs every time the user sends a message in the Streamlit interface.

@ "role": "user"
We first store the user's message in the session history, so the conversation is remembered across turns.

@ "service.send_request"
Then we call send request on our service, passing the user's text, and we get the model's reply back.

@ 12-13
When the reply comes back, we append it to the history as well, and we return it so the interface can display it. This is the bridge between our user interface and our model service.
