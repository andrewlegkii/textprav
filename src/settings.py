import os
import psycopg2
from psycopg2 import Error


def get_user_settings(user_id):
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        row = cur.fetchone()
        if row:
            settings = {'grammar': row[1], 'punctuation': row[2], 'spelling': row[3], 'syntax': row[4]}
            return settings
        else:
            return None
    except Error as e:
        print(e)
    finally:
        cur.close()
        conn.close()


def save_user_settings(user_id, settings):
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (id, grammar, punctuation, spelling, syntax) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET grammar=EXCLUDED.grammar, punctuation=EXCLUDED.punctuation, spelling=EXCLUDED.spelling, syntax=EXCLUDED.syntax",
            (user_id, settings.get('grammar', False), settings.get('punctuation', False), settings.get('spelling', False), settings.get('syntax', False))
        )
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()
        conn.close()
