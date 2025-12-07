import sys
import os

# 현재 디렉토리를 sys.path에 추가하여 app 모듈을 찾을 수 있게 함
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.database import SessionLocal
from app.models.bean import Bean
from app.models.inventory_log import InventoryLog  # 관계형 모델 로드를 위해 필요

def check_data():
    db = SessionLocal()
    try:
        count = db.query(Bean).count()
        print(f"Total Beans: {count}")
        if count > 0:
            beans = db.query(Bean).limit(5).all()
            print("First 5 beans:")
            for bean in beans:
                print(f"- {bean.name}")
        else:
            print("No beans found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_data()
