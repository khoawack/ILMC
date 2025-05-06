from app.database import SessionLocal
from sqlalchemy import text

# run this :  python -m test.test_db 

def test_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Connected to Supabase DB!")
    except Exception as e:
        print("❌ Connection failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
