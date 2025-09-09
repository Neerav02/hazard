# nlp_processor.py
from transformers import pipeline

# Initialize pipelines once to avoid reloading models on every call
sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="cardiffnlp/twitter-xlm-roberta-base-sentiment"
)

topic_pipeline = pipeline(
    "text-classification", 
    model="classla/multilingual-IPTC-news-topic-classifier", 
    top_k=1
)

ner_pipeline = pipeline(
    "ner", 
    model="julian-schelb/roberta-ner-multilingual"
)
def process_text_batch(texts: list[str]) -> list[dict]:
    results = []

    # Run pipelines on the entire batch of texts for better performance
    sentiments = sentiment_pipeline(texts)
    topics = topic_pipeline(texts)
    entities = ner_pipeline(texts)

    # Combine the results for each individual text
    for i in range(len(texts)):
        # Find all words/phrases tagged as a Location ('LOC')
        locations = [
            entity['word'] for entity in entities[i] 
            if entity['entity_group'] == 'LOC'
        ]

        processed_data = {
            'sentiment': sentiments[i]['label'],
            'sentiment_score': sentiments[i]['score'],
            'topic': topics[i][0]['label'], # top_k=1 returns a list
            'topic_score': topics[i][0]['score'],
            'extracted_locations': locations
        }
        results.append(processed_data)

    return results