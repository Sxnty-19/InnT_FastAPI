from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)

if __name__ == "__main__":
    try:
        print("Probando conexión a Supabase...")
        supabase = get_supabase_client()
        print("Conexión exitosa")
    except Exception as e:
        print("Conexión fallida:", e)