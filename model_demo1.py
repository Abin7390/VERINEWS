import requests
import json

class LMStudioClient:
    def __init__(self, api_url='http://127.0.0.1:1234/v1/chat/completions', model=None):
        self.api_url = api_url
        self.model = model if model else "lmstudio-community/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q4_K_M.gguf"
        self.default_params = {
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": True
        }

    def send_request(self, news_text, retrieved_text=None, temperature=None, max_tokens=None, stream=None):
        # Prepare the system prompt asking the model to check the news authenticity
        system_message = {
            "role": "system",
            "content": "You are a fact-checking assistant. Determine whether the following news is credible or likely fake. Provide reasoning for your assessment."
        }

        # Create user message with the news text to be analyzed
        user_message = {
            "role": "user",
            "content": news_text
        }

        # Add context information (if available)
        if retrieved_text:
            context_message = "Here are some relevant sources for your assessment:\n"
            for query, response in retrieved_text:
                context_message += f"Source: {query}\nContent: {response}\n"
            messages = [system_message, {"role": "system", "content": context_message}, user_message]
        else:
            messages = [system_message, user_message]

        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.default_params["temperature"],
            "max_tokens": max_tokens if max_tokens is not None else self.default_params["max_tokens"],
            "stream": stream if stream is not None else self.default_params["stream"]
        }

        try:
            response = requests.post(self.api_url, headers={"Content-Type": "application/json"}, data=json.dumps(params), stream=params["stream"])
            response.raise_for_status()

            if params["stream"]:
                final_output = ""
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8').strip()
                        if decoded_line.startswith('data: '):
                            decoded_line = decoded_line[6:]
                        if decoded_line:
                            try:
                                message = json.loads(decoded_line)
                                content = message.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                final_output += content
                                yield content  # Yield content as it is generated
                            except json.JSONDecodeError:
                                continue
                yield final_output  # Finally yield the complete output
            else:
                return response.json()

        except requests.exceptions.RequestException as e:
            yield f"Error: {e}"  # yield the error for the app to handle


client = LMStudioClient()

news = input("query:")
for response in client.send_request(news_text=news):
    print(response)
