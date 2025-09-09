import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from nlp_processor import process_text_batch
from social_media_client import fetch_recent_posts

load_dotenv()

def run_ingestion_pipeline():
    db_conn = None
    try:
        db_conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        print("Database connection successful.")
        posts_from_api = fetch_recent_posts()
        if not posts_from_api:
            print("No posts found from the source.")
            return
        
        source_ids = [post['id'] for post in posts_from_api]
        with db_conn.cursor() as cur:
            cur.execute("SELECT source_id FROM public.social_media_posts WHERE source_id = ANY(%s)", (source_ids,))
            existing_ids = {row[0] for row in cur.fetchall()}
        
        new_posts = [post for post in posts_from_api if post['id'] not in existing_ids]
        if not new_posts:
            print("No new posts to process.")
            return

        texts_to_process = [post['text'] for post in new_posts]
        print(f"Processing {len(texts_to_process)} new posts...")
        nlp_results = process_text_batch(texts_to_process)

        records_to_insert = []
        for i, post in enumerate(new_posts):
            result = nlp_results[i]
            records_to_insert.append((
                post['id'], 'twitter', post.get('author'), post['text'], post.get('created_at'),
                result.get('sentiment'), result.get('sentiment_score'),
                result.get('topic'), result.get('topic_score')
            ))

        with db_conn.cursor() as cur:
            insert_query = """
                INSERT INTO public.social_media_posts (
                    source_id, source_platform, author, raw_text, posted_at,
                    sentiment, sentiment_score, topic, topic_score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            psycopg2.extras.execute_batch(cur, insert_query, records_to_insert)
            db_conn.commit()
        
        print(f"Successfully inserted {len(records_to_insert)} new posts.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if db_conn:
            db_conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    run_ingestion_pipeline()
