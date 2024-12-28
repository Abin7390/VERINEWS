import os
from LM_studio_class import LMStudioClient
from test.views import get_search_results, remove_links_and_images

#using it chat.views
#LMStudioClient class is already defined and imported

client = LMStudioClient(
    api_url="http://127.0.0.1:1234/v1/chat/completions"  # Modify this if necessary
)


def extract_titles(json_data):
    titles = []
    if isinstance(json_data, dict):
        # If 'title' or 'snippet' is present, add it to titles list
        if 'title' in json_data:
            titles.append(json_data['title'])
        if 'snippet' in json_data:
            titles.append(json_data['snippet'])
        if 'date' in json_data:
            titles.append(json_data['date'])
                
        # Recursively check the values for more 'title' or 'snippet' entries
        for key, value in json_data.items():
            titles.extend(extract_titles(value))
    elif isinstance(json_data, list):
        # Recursively check each item in the list
        for item in json_data:
            titles.extend(extract_titles(item))
    
    # Return the accumulated titles
    print(f'{titles}')
    return titles



def search_on_web(query):
    messages = []

    # Get web search results for the given query
    search_result = get_search_results(query)

    # Filter out any unwanted links or images from the search results
    # filtered_response = remove_links_and_images(search_result)
    titles = remove_links_and_images(search_result)
    # titles = extract_titles(search_result)
    # me = ['IND vs NZ: India All Out For 46 Against New Zealand, Record Lowest Ever  Test Total At Home |Breaking', 'India vs New Zealand Highlights: 1st Time In 91 Years, IND All Out For 46  Against NZ', 'Pakistan Position Strong Against England | Indian Team All Out In 46 Runs  Against NZ | G Sports', 'India all out only 46 runs against New Zealand,King Koli,0,Rohat Sharma ,2,', 'India all out for 46 in first innings vs New Zealand in ...', 'Indian batting sinks to new low, ALL OUT for 46 vs NZ, records WORST ever  total in...', 'India 46 all out against New Zealand. Lowest total ever recorded in India.  👀', 'India All Out for 46 Runs | NZ vs IND Test #india #newzealand #test #shorts  #ytshorts #arynews', 'India vs New Zealand 1st Test Day 2: India All Out For 46 Runs', "India's SHOCKING 10 Wickets for 46 Against New Zealand ...", 'Cricket: India all out for 46 | 7NEWS', 'All out for 46?! FIVE ducks as Black Caps THUMP India in ...', 'IND vs NZ: India All Out For 46 Against New Zealand, Record ...', 'India vs New Zealand head-to-head in Tests', '36', 'Indian cricket team in New Zealand in 2008–09 - Wikipedia', "Lowest Test scores: A look at India's Top 10 worst batting performances ...", 'India vs New Zealand Live Score, 1st Test Day 3', 'India all out for 46 in first innings vs New Zealand in lowest ...', 'New Zealand leads by 134 after India bowled out for 46 ...', 'India crumble to 46 against New Zealand for lowest Test ...', 'India Vs New Zealand LIVE score: NZ 260/7 after 71 ... - Mint', 'Aakash Chopra backs India to score 450 in 2nd innings ...', 'A great fall: 46 all out | Latest News India', 'India all out for 46 in first cricket Test match against New Zealand', 'India vs New Zealand Highlights, 1st Test Day 2: NZ 180/3 Rachin Ravindra and Daryl Mitchell unbeaten at stumps in Bengaluru', '46 all out: Records rewritten as India register lowest Test total at home', 'India vs New Zealand highlights, 1st Test Day 2: New Zealand 180/3 at stumps, lead by 134 runs in Bengaluru', "'At least you have got past 36...': Cricket fraternity reacts as India bundled out on 46 during 1st Test against New Zealand in Bengaluru"]
    # Prepare the input prompt for the LLM
    prompt = f"Assess the Authenticity of the news: {query} by analyzing the article: {titles} and verify {query} is fake or not. give an answer in atmost of two lines. "
    # retrieved_text = [(me)]  # Here we're wrapping the filtered response in a list as tuples

    # Send the prompt along with the retrieved context to the LLM
    result = ""
    for chunk in client.send_request(news_text=prompt):
        result += chunk  # Accumulate the streamed output
    print(result)
    return result

# Take user input
# user_query = input("Enter  search query: ")

# # Call the search function
# verification_result = search_on_web(user_query)
# print(verification_result)
