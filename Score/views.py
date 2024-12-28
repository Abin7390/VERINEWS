import csv
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from openai import AzureOpenAI

from test.views import get_search_results, remove_links_and_images

# Set OpenAI API key
# client = AzureOpenAI(
#     azure_endpoint="https://reels-openai.openai.azure.com/", 
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
#     api_version="2024-02-15-preview"
# )
openai.api_key = 'anything'
openai.base_url = "https://api.pawan.krd/cosmosrp/v1/chat/completions"
openai.api_version = ""


def filter_stop_words(text):
    # Define your list of stop words
    stop_words = ["is", "was", "else", "and", "so", "on"]  # Add more words as needed
    
    # Tokenize the text
    words = text.split()
    
    # Filter out stop words
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    # Reconstruct the filtered text
    filtered_text = " ".join(filtered_words)
    
    return filtered_text

def analyze_news(message):
    # Step 1: Read the news article input by the user and filter stop words
    
    filtered_user_news = filter_stop_words(message)

    # Step 2: Read the CSV data 
    news_content = []
    labels = []
    news_info = []
    csv_filepaths = ["C:/Users/abinv/OneDrive/Desktop/PROJECTS/VeriNews/Datasets/fake_or_real_news.csv", "C:/Users/abinv/OneDrive/Desktop/PROJECTS/VeriNews/Datasets/fake1.csv"]

    for csv_filepath in csv_filepaths:
        with open(csv_filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Extract the content and label (real or fake) from each row and filter stop words
                content = row['title']  # Adjust 'content_column' to match your CSV structure
                filtered_content = filter_stop_words(content)
                label = row['label']  # Adjust 'label_column' to match your CSV structure
                info = row['text']
                news_content.append(filtered_content)
                labels.append(label)
                news_info.append(info)

    # Step 3: Compute TF-IDF vectors for user input and news articles
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([filtered_user_news] + news_content)
    
    # Step 4: Compute cosine similarity between user input and each news article
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

    # Step 5: Create a dictionary to store scores for each news article
    scores = {}
    for i, sim in enumerate(similarities):
        scores[i] = {'is_fake': labels[i],'news': news_content[i], 'score': sim,'more_info':news_info[i]}

    return scores


def search_on_web(query):
    messages=[]
    search_result=get_search_results(query)

    # Print the search results (customize as needed)
    filtered_response = remove_links_and_images(search_result)

    # Prepare the input prompt
    prompt ="You are an AI specialized in analyzing news. Act as an AI that only knows to respond in JSON format. Your function is to respond strictly in the JSON format prescribed. No '*' should be in the response. Respond with '{ 'result' : 'value' }', where 'value' is either 'fake' or 'real', based on the analysis. Provide the response in pure JSON format, without additional commentary or Markdown formatting. The JSON output should be your only response. For example, if the news is fake, respond with '{ 'result' : 'fake' }'. Follow this structure rigorously."

    prompt += f"also tell me the reason for your classification as your given value as real or fake"
    prompt += f"Based on the provided information: {filtered_response}, assess the authenticity of the news related to {query}. Respond strictly with a keyterm as either 'Fake' or 'Real'. if the news is incorrect the news must be fake and otherwise it you must respond as real."
    # prompt += "dont add any sentence or phrases like analyzing in front of the main answer "
    messages.append({"role": "system", "content": prompt})
    
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # model = "deployment_name"
        messages=messages
    )

    # Get the result from completion
    result = completion.choices[0].message.content

    return result



  
