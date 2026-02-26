from datetime import datetime
from dotenv import load_dotenv
import pytz
import os

load_dotenv()

def get_fecha_actual():
    timezone_name = os.getenv("TIMEZONE", "UTC")
    zona_horaria = pytz.timezone(timezone_name)
    return datetime.now(zona_horaria)