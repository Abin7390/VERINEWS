import requests
import json



class LMStudioClient:
    def _init_(self, api_url='http://127.0.0.1:1234/v1/chat/completions', model=None):
        self.api_url = api_url
        self.model = model if model else "lmstudio-community/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q4_K_M.gguf"
        self.default_params = {
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": True
        }

    def send_request(self, messages, retrieved_text=None, temperature=None, max_tokens=None, stream=None):
        # If retrieved_text is provided, we incorporate it into the messages
        if retrieved_text:
            context_message = "Here are some relevant training examples:\n"
            for query, response in retrieved_text:
                context_message += f"Query: {query}\nResponse: {response}\n"

            # Add the context message as a system message to provide background information
            messages.append({"role": "system", "content": context_message})

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
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8').strip()
                        print(f"Received line: {decoded_line}")
                        if decoded_line.startswith('data: '):
                            decoded_line = decoded_line[6:]
                        if decoded_line:
                            try:
                                message = json.loads(decoded_line)
                                content = message.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                yield content  # Yield content instead of returning a complete response
                            except json.JSONDecodeError:
                                continue
            else:
                return response.json()

        except requests.exceptions.RequestException as e:
            yield f"Error: {e}"  # yield the error for the streamlit app to handle



# client = LMStudioClient()
# stream = client.send_request(
#     history,
#     retrieved_text= retrieved_text,
#     temperature=temperature,
#     max_tokens=max_tokens,
#     stream=True
# )