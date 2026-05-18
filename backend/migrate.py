"""
migrate.py — roda uma vez para corrigir o banco.
Adiciona colunas que faltam na tabela ads.

Uso:
    cd backend
    python migrate.py
"""
import psycopg2

DATABASE_URL = "postgresql://postgres:Do30503!@localhost:5432/adintel"

COLUMNS_TO_ADD = [
    ("score",      "FLOAT DEFAULT 0"),
    ("body",       "TEXT"),
    ("image_url",  "TEXT"),
    ("media_type", "VARCHAR(100)"),
    ("cta",        "VARCHAR(255)"),
    ("headline",   "TEXT"),
    ("page_name",  "VARCHAR(255)"),
    ("ad_id",      "VARCHAR(255)"),
    ("analyzed_at","TIMESTAMP"),
    ("urgency_score",       "INTEGER DEFAULT 0"),
    ("trust_score",         "INTEGER DEFAULT 0"),
    ("speed_score",         "INTEGER DEFAULT 0"),
    ("accessibility_score", "INTEGER DEFAULT 0"),
]

def migrate():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Garante que a tabela existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            id SERIAL PRIMARY KEY,
            ad_id VARCHAR(255) UNIQUE,
            page_name VARCHAR(255),
            headline TEXT,
            body TEXT,
            cta VARCHAR(255),
            media_type VARCHAR(100),
            image_url TEXT,
            score FLOAT DEFAULT 0,
            urgency_score INTEGER DEFAULT 0,
            trust_score INTEGER DEFAULT 0,
            speed_score INTEGER DEFAULT 0,
            accessibility_score INTEGER DEFAULT 0,
            analyzed_at TIMESTAMP
        )
    """)

    # Adiciona colunas que faltam sem derrubar dados
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='ads'")
    existing = {row[0] for row in cur.fetchall()}

    for col, col_type in COLUMNS_TO_ADD:
        if col not in existing:
            print(f"[+] Adicionando coluna: {col}")
            cur.execute(f"ALTER TABLE ads ADD COLUMN {col} {col_type}")
        else:
            print(f"[ok] Coluna já existe: {col}")

    conn.commit()
    cur.close()
    conn.close()
    print("\n✅ Migração concluída.")

if __name__ == "__main__":
    migrate()