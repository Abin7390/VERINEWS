# Import necessary libraries
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import csv
import os
from django.urls import reverse
from httpcore import request
from openai import AzureOpenAI
import openai
from Score.views import analyze_news
from model_demo2 import search_on_web  # Using LLM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from register.models import Users
from LM_studio_class import LMStudioClient


# Set OpenAI API key
# client = AzureOpenAI(
#     azure_endpoint="https://reels-openai.openai.azure.com/", 
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
#     api_version="2024-02-15-preview"
# )
# openai.api_key = 'anything'
# openai.base_url = "https://api.pawan.krd/cosmosrp/v1/chat/completions"
# openai.api_version = ""

#client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
client = LMStudioClient(
    api_url="http://127.0.0.1:1234/v1/chat/completions"  # Modify this if necessary
)

def welcome(request):
    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            user = None
    user_messages = request.session.get('user_messages', [])
    response_history = request.session.get('response_history', [])  # Retrieve response history from session
    messages = request.session.get('messages', [])  # Initialization
    response_text = ""
    new_similarities = []
    new_index = []  # To store response_text with corresponding user_messages
    formatted_list=[]


    if request.method == 'POST':
        message = request.POST.get('msg')
        
        news_results = analyze_news(message)  

        if message == "hi" or message =="hello":
            if user:
                response_text = f"Hey {user.username}, how can I assist you?"
            else:
                response_text = "Hey, how can I assist you?"        
            
        else:
            news_content = [result['news'] for result in news_results.values()]
            vectorizer = TfidfVectorizer()                                      
            tfidf_matrix = vectorizer.fit_transform([message] + news_content)
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
            most_similar_index = similarities.argmax()                                          #returns the index of the maximum value in the similarities array
            most_similar_label = list(news_results.values())[most_similar_index]['is_fake']
            most_similar_content = list(news_results.values())[most_similar_index]['news']
            most_similar_info = list(news_results.values())[most_similar_index]['more_info']
            print(similarities[most_similar_index])

            if similarities[most_similar_index] > 0.7:
                if most_similar_label == 'REAL' or most_similar_label=='1':
                    
                    response_text = f'Is the news you are searching is: "{most_similar_content}"  - (REAL)  : \n '
                    response_text += f'\n{most_similar_info[:100]}... <a href="{reverse("read_more", args=[most_similar_index])}">(Read more)</a>'
                else:
                    response_text = f'The news seems similar to "{most_similar_content}"  - (FAKE)'
            elif similarities[most_similar_index] > 0.35:
                # Add news content to new_similarities list
                
                new_similarities.append(most_similar_content)
                new_index.append(most_similar_label)

                print(new_similarities)
                print(new_index)
                total_tokens = calculate_token_count(messages)
                print("Total tokens in messages:", total_tokens)
                if most_similar_label == 'REAL':
                
                    prompt = f"You are a fake news detector you have to check the given news from the user and give respond as it is fake or real based on the news content . We have a few news articles here. Check the whole sentence meaning of each of the news articles '{new_similarities}' with the input '{message}' and give a response as: the news is '{new_index}'.which is similar to '{new_similarities}'  "
                else:
                    prompt = f"You are a fake news detector you have to check the given news from the user and give respond as it is fake or real based on the news content . We have a few news articles here. Check the whole sentence meaning of each of the news articles '{new_similarities}' with the input '{message}' and give a response as' the news searched is fake and it is similar to an article '{new_similarities}' ':"

                # Generate response from GPT-3.5 
                # messages.append({"role": "system", "content": prompt})
                
                # total_tokens = calculate_token_count(messages)
                # print("Total tokens in messages:", total_tokens)

                # chat_input = {"role": "user", "content": message}
                # messages.append(chat_input)
                # completion = openai.chat.completions.create(
                #     model="gpt-3.5-turbo",   # model = "deployment_name"
                #     messages=messages,
                #     temperature=0.7,
                #     max_tokens=800,
                #     top_p=0.95,
                #     frequency_penalty=0,
                #     presence_penalty=0,
                #     stop=None
                # )
                result = ""
                for chunk in client.send_request(news_text=prompt):
                    result += chunk  # Accumulate the streamed output
                print(result)
                
                # response_text = completion.choices[0].message.content
                response_text = result

                if all(element in response_text for element in new_similarities):
                    response_text += f" \n {most_similar_info[:100]}... <a href='{reverse('read_more', args=[most_similar_index])}'>(Read more)</a>"
                else:
                    response_text=response_text
            else:
                web_result=search_on_web(message)
                #add something to remove the analyzing news message from the front
                response_text=web_result



        assistant_response = {"role": "assistant", "content": response_text}  # Store assistant's response
        input_message = {"role": "user", "content": message}
        messages.append(input_message)
        messages.append(assistant_response)
        
        response_history.append({"user":message, "assistant":response_text})  # Append current response and user messages to history


        formatted_list = []

        for item in response_history:
            if isinstance(item, dict):  # Check if item is a dictionary
                user_message = {"role": "user", "content": item.get('user', '')}
                assistant_message = {"role": "assistant", "content": item.get('assistant', '')}
                formatted_list.append(user_message)
                formatted_list.append(assistant_message)
            elif isinstance(item, str):  # Check if item is a string
                formatted_list.append({"role": "user", "content": item})
                formatted_list.append({"role": "assistant", "content": ""})  # Assuming no assistant response for user's message

        # print(formatted_list)



        request.session['response_history'] = response_history
        request.session['user_messages'] = user_messages
        request.session['message'] = messages  # Save messages back to session
 
        
    
    
    user_id = request.session.get('user1_id')
    
    return render(request, 'welcome.html', {'messages': messages, 'username': user.username if user else None, 'formatted_list': formatted_list})




def read_more(request, news_id):
    news_results = analyze_news("")  # Call analyze_news with an empty string to retrieve all news articles
    news_info = news_results[news_id]['more_info']
    news_content = news_results[news_id]['news']
    return render(request, 'read_more.html', {'news_info': news_info, 'news':news_content})






def calculate_token_count(messages):
    total_tokens = sum(len(message["content"].split()) for message in messages)
    print(total_tokens)
    return total_tokens


