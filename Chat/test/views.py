from django.shortcuts import render

# Create your views here.
import serpapi
import json

# Set your SerpApi API key
api_key = "b215cc4c1e0304fc79d7b7a16c066afbb983f7c317c2b89635e72a495419c118"



def get_search_results(user_query):
    # Initialize a GoogleSearch object
    search = serpapi.GoogleSearch({
        "q": user_query,  # Your search query
        "location": "kerala, india",  # Location for localized results
        "hl": "en",  # Google UI language
        "gl": "us",  # Google country
        "api_key": api_key  # Your SerpApi API key
    })

    # Get search results as a dictionary
    results = search.get_dict()
    return results


def extract_titles(json_data):
    titles = []

    if isinstance(json_data, dict):
        # If 'title' is present, add it to titles list
        if 'title' in json_data:
            titles.append(json_data['title'])
        
        # Recursively check the values for more 'title' entries
        for key, value in json_data.items():
            titles.extend(extract_titles(value))

    elif isinstance(json_data, list):
        # Recursively check each item in the list
        for item in json_data:
            titles.extend(extract_titles(item))

    # Return the accumulated titles
    return titles 



def remove_links_and_images(json_data, max_tokens=500, current_tokens=0):
    if current_tokens >= max_tokens:
        return {}  # Return an empty dictionary if the maximum token count is reached

    if isinstance(json_data, dict):
        # Remove links and images from dictionary keys
        keys_to_remove = [key for key in json_data.keys() if 'link' in key.lower() or 'image' in key.lower()]
        for key in keys_to_remove:
            json_data.pop(key)

        # Recursively remove links and images from dictionary values
        for key, value in json_data.items():
            json_data[key] = remove_links_and_images(value, max_tokens, current_tokens)

    elif isinstance(json_data, list):
        # Recursively remove links and images from list elements
        json_data = [remove_links_and_images(item, max_tokens, current_tokens) for item in json_data]

    # Increment token count
    current_tokens += len(json.dumps(json_data))

    return json_data





poda = input("enter your search: ")
me = get_search_results(poda)
me1 = extract_titles(me)
# print(me1)