from transformers import pipeline

print("Loading NLP models into memory...")
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
topic_pipeline = pipeline("text-classification", model="classla/multilingual-IPTC-news-topic-classifier", top_k=1)
ner_pipeline = pipeline("ner", model="julian-schelb/roberta-ner-multilingual")
print("NLP models loaded successfully.")

def process_text_batch(texts: list[str]) -> list[dict]:
    if not texts: return []
    sentiments = sentiment_pipeline(texts)
    topics = topic_pipeline(texts)
    entities = ner_pipeline(texts)
    results = []
    for i in range(len(texts)):
        locations = [entity['word'] for entity in entities[i] if entity['entity_group'] == 'LOC']
        results.append({
            'sentiment': sentiments[i]['label'], 'sentiment_score': round(sentiments[i]['score'], 4),
            'topic': topics[i][0]['label'], 'topic_score': round(topics[i][0]['score'], 4),
            'extracted_locations': locations
        })
    return results