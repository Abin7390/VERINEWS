import json
serp_results= 
data = json.loads(serp_results)

# Extract relevant fields from each result
questions_snippets_titles = []
for result in data.get('organic_results', []):
    extracted_info = {
        "title": result.get("title", ""),
        "snippet": result.get("snippet", ""),
        "question": result.get("question", ""),
        "link": result.get("link", "")
    }
    questions_snippets_titles.append(extracted_info)

# Print or use the extracted information
for item in questions_snippets_titles:
    print(f"Title: {item['title']}")
    print(f"Snippet: {item['snippet']}")
    print(f"Question: {item['question']}")
    print(f"Link: {item['link']}\n")