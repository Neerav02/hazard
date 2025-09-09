# pipeline.py
from nlp_processor import process_text_batch

# In a real scenario, this would come from a social media API call
def fetch_recent_posts():
    print("Fetching mock data...")
    return [
        {'id': 'post1', 'text': 'There is a terrible storm hitting the coast of Chennai.'},
        {'id': 'post2', 'text': 'The weather today in Mumbai is beautiful and sunny.'},
        {'id': 'post3', 'text': 'A major accident was reported on the highway near Delhi.'},
    ]
def run_ingestion_pipeline():
    # 1. Fetch new posts from the source
    posts = fetch_recent_posts()

    # In a real script, you would filter out posts already in the DB here

    # 2. Extract the text content to be processed
    texts_to_process = [post['text'] for post in posts]

    # 3. Process the texts using the NLP module
    if texts_to_process:
        print(f"Processing {len(texts_to_process)} new posts...")
        nlp_results = process_text_batch(texts_to_process)

        # This is where you'll add the database insertion logic in the next sprint
        print("--- NLP Results ---")
        for i, post in enumerate(posts):
            print(f"Original Post: {post['text']}")
            print(f"Processed Data: {nlp_results[i]}\n")
    else:
        print("No new posts to process.")

# This makes the script runnable from the command line
if __name__ == "__main__":
    run_ingestion_pipeline()