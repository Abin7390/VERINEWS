import os
from openai import AzureOpenAI

# Set OpenAI API key
client = AzureOpenAI(
    azure_endpoint="https://reels-openai.openai.azure.com/", 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-15-preview"
)

def search_on_web(query):
    messages=[]

    # Prepare the input prompt
    prompt = f" {query} "

    messages.append({"role": "system", "content": prompt})
    
    completion = client.chat.completions.create(
        model="gpt-35-turbo",  # model = "deployment_name"
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    # Get the result from completion
    result = completion.choices[0].message.content

    return result

# Take user input
user_query = input("Enter your search query: ")

# Call the search function
search_result = search_on_web(user_query)

# Display the search result
print("Search result:")
print(search_result)