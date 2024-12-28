from django.shortcuts import render

# Create your views here.
import serpapi
import json

# Set your SerpApi API key
api_key = "b215cc4c1e0304fc79d7b7a16c066afbb983f7c317c2b89635e72a495419c118"



def get_search_results(user_query):
    # Initialize a GoogleSearch object
    final_query=f"is it real that{user_query}"
    search = serpapi.GoogleSearch({
        "q": final_query,  # Your search query
        "location": "kerala, india",  # Location for localized results
        "hl": "en",  # Google UI language
        "gl": "us",  # Google country
        "api_key": api_key  # Your SerpApi API key
    })

    # Get search results as a dictionary
    results = search.get_dict()
    return results



def truncate_json(json_data, fraction=1/3):
    """
    Truncate the JSON data by removing the last fraction of the elements.
    """
    if isinstance(json_data, dict):
        keys = list(json_data.keys())
        cutoff = int(len(keys) * (1 - fraction))
        truncated_data = {key: json_data[key] for key in keys[:cutoff]}
        return truncated_data

    elif isinstance(json_data, list):
        cutoff = int(len(json_data) * (1 - fraction))
        return json_data[:cutoff]

    return json_data






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

    # Truncate the JSON data if it exceeds the max_tokens
    if current_tokens > max_tokens:
        json_data = truncate_json(json_data)

    return json_data
