import json
import os
from openai import AzureOpenAI

from test.views import get_search_results, remove_links_and_images

# Set OpenAI API key
client = AzureOpenAI(
    azure_endpoint="https://reels-openai.openai.azure.com/", 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-15-preview"
)

def search_on_web(query):
    messages=[]
    search_result=get_search_results(query)

    # Print the search results (customize as needed)
    filtered_response = remove_links_and_images(search_result)

    # Prepare the input prompt
    prompt = f"analyse the news: {query} and determine whether it is fake or it is real based on the informations: {filtered_response}"
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
verification_result = search_on_web(user_query)
print(verification_result)



'''# Convert back to JSON string for readability
filtered_response_json = json.dumps(filtered_response, indent=2)'''

