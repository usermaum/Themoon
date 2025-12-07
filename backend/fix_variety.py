"""
품종(variety) 데이터 수정 스크립트 v3
- recreate_db.py 원본 데이터 기반으로 "한글 (영문)" 형식으로 통일
"""
import sqlite3

conn = sqlite3.connect('themoon.db')
cursor = conn.cursor()

# recreate_db.py 원본 데이터 기반 품종 매핑
# ID | 원두명 | 원본 variety -> 새 variety (한글 (영문))
variety_updates = [
    # 에티오피아
    (1, '예가체프 (Yirgacheffe)'),      # 원본: Yirgacheffe
    (2, '모모라 (Mormora)'),             # 원본: Mormora (유저 요청)
    (3, '코케허니 (Koke Honey)'),        # 원본: Koke Honey
    (4, '우라가 (Uraga)'),               # 원본: Uraga
    (5, '시다모 (Sidamo)'),              # 원본: Sidamo
    
    # 케냐
    (6, '마사이 (Masai)'),               # 원본: Masai
    (7, '키리냐가 (Kirinyaga)'),         # 원본: Kirinyaga
    
    # 중남미
    (8, '후일라 (Huila)'),               # 원본: Huila
    (9, '안티구아 (Antigua)'),           # 원본: Antigua
    (10, '엘탄케 (El Tanque)'),          # 원본: El Tanque
    (11, '파젠다 카르모 (Fazenda Carmo)'), # 원본: Fazenda Carmo
    (12, '산토스 (Santos)'),             # 원본: Santos
    
    # 디카페인
    (13, '디카페 SDM (Decaf SDM)'),      # 원본: Decaf SDM
    (14, '디카페 SM (Decaf SM)'),        # 원본: Decaf SM
    (15, '스위스워터 (Swiss Water)'),   # 원본: Swiss Water
    
    # 스페셜티
    (16, '게이샤 (Geisha)'),             # 원본: Geisha
]

print("=== 수정 전 현재 DB 상태 ===")
cursor.execute('SELECT id, name, variety FROM beans ORDER BY id')
for row in cursor.fetchall():
    print(f"ID: {row[0]:2}, Name: {row[1]}, Variety: {row[2]}")

print("\n=== 업데이트 실행 ===")
for bean_id, new_variety in variety_updates:
    cursor.execute('UPDATE beans SET variety = ? WHERE id = ?', (new_variety, bean_id))
    print(f"  Updated ID {bean_id}: {new_variety}")

conn.commit()

print("\n=== 수정 후 결과 ===")
cursor.execute('SELECT id, name, variety FROM beans ORDER BY id')
for row in cursor.fetchall():
    print(f"ID: {row[0]:2}, Name: {row[1]}, Variety: {row[2]}")

conn.close()
print("\n✅ 완료!")
