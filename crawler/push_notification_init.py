import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("../assets/firebase-key.json")
# cred = credentials.Certificate("firebase-key.json")

firebase_admin.initialize_app(cred)

db = firestore.client()

notices_ref = db.collection("notices")
docs = notices_ref.stream()

batch = db.batch()
count = 0

for doc in docs:
    data = doc.to_dict()

    # push_sent 필드가 없거나 False인 경우만 처리
    if data.get("push_sent") is not True:
        batch.update(doc.reference, {
            "push_sent": True
        })
        count += 1

    # Firestore batch는 최대 500개
    if count % 450 == 0:
        batch.commit()
        batch = db.batch()

if count % 450 != 0:
    batch.commit()

print(f"초기화 완료: {count}개 문서 업데이트")
