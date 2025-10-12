import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("assets/firebase-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

keywords = [
    {"id": "0001", "keyword": "기숙사", "defined": "developer"},
    {"id": "0002", "keyword": "등록금", "defined": "developer"},
    {"id": "0003", "keyword": "수강신청", "defined": "developer"},
    {"id": "0004", "keyword": "공모전", "defined": "developer"},
    {"id": "0005", "keyword": "장학금", "defined": "developer"},
    {"id": "0006", "keyword": "복학", "defined": "developer"},
    {"id": "0007", "keyword": "성적", "defined": "developer"},
    {"id": "0008", "keyword": "휴학", "defined": "developer"},
    {"id": "0009", "keyword": "졸업", "defined": "developer"},
    {"id": "0010", "keyword": "봉사", "defined": "developer"},
    {"id": "0011", "keyword": "해외", "defined": "developer"},
    {"id": "0012", "keyword": "인턴", "defined": "developer"},
    {"id": "0013", "keyword": "계절", "defined": "developer"},
]

for kw in keywords:
    doc_ref = db.collection("topic").document(kw["id"])
    doc_ref.set({
        "topic": kw["keyword"],
        "defined": kw["defined"]
    })
    print(f"Uploaded {kw['id']} → {kw['keyword']}")

print("All keywords uploaded successfully!")

majors = [
    {"id": "0101", "department": "학부대학", "major": "사회과학계열"},
    {"id": "0102", "department": "학부대학", "major": "인문사회계열"},
    {"id": "0103", "department": "학부대학", "major": "공학계열"},
    {"id": "0104", "department": "학부대학", "major": "자연과학계열"},
    {"id": "0201", "department": "유학대학", "major": "유학동양학과"},
    {"id": "0301", "department": "문과대학", "major": "국어국문학과"},
    {"id": "0302", "department": "문과대학", "major": "독어독문학과"},
    {"id": "0303", "department": "문과대학", "major": "러시아어문학과"},
    {"id": "0304", "department": "문과대학", "major": "문헌정보학과"},
    {"id": "0305", "department": "문과대학", "major": "사학과"},
    {"id": "0306", "department": "문과대학", "major": "영어영문학과"},
    {"id": "0307", "department": "문과대학", "major": "중어중문학과"},
    {"id": "0308", "department": "문과대학", "major": "철학과"},
    {"id": "0309", "department": "문과대학", "major": "프랑스어문학과"},
    {"id": "0310", "department": "문과대학", "major": "한문학과"},
    {"id": "0401", "department": "사회과학대학", "major": "글로벌리더학부"},
    {"id": "0402", "department": "사회과학대학", "major": "미디어커뮤니케이션학과"},
    {"id": "0403", "department": "사회과학대학", "major": "사회복지학과"},
    {"id": "0404", "department": "사회과학대학", "major": "사회학과"},
    {"id": "0405", "department": "사회과학대학", "major": "소비자학과"},
    {"id": "0406", "department": "사회과학대학", "major": "심리학과"},
    {"id": "0407", "department": "사회과학대학", "major": "아동·청소년학과"},
    {"id": "0408", "department": "사회과학대학", "major": "정치외교학과"},
    {"id": "0409", "department": "사회과학대학", "major": "행정학과"},
    {"id": "0501", "department": "경제대학", "major": "경제학과"},
    {"id": "0502", "department": "경제대학", "major": "글로벌경제학과"},
    {"id": "0503", "department": "경제대학", "major": "통계학과"},
    {"id": "0601", "department": "경영대학", "major": "경영학과"},
    {"id": "0602", "department": "경영대학", "major": "글로벌경영학과"},
    {"id": "0701", "department": "사범대학", "major": "교육학과"},
    {"id": "0702", "department": "사범대학", "major": "수학교육과"},
    {"id": "0703", "department": "사범대학", "major": "컴퓨터교육과"},
    {"id": "0704", "department": "사범대학", "major": "한문교육과"},
    {"id": "0801", "department": "예술대학", "major": "디자인학과"},
    {"id": "0802", "department": "예술대학", "major": "무용학과"},
    {"id": "0803", "department": "예술대학", "major": "미술학과"},
    {"id": "0804", "department": "예술대학", "major": "연기예술학과"},
    {"id": "0805", "department": "예술대학", "major": "의상학과"},
    {"id": "0806", "department": "예술대학", "major": "영상학과"},
    {"id": "0901", "department": "자연과학대학", "major": "물리학과"},
    {"id": "0902", "department": "자연과학대학", "major": "생명과학과"},
    {"id": "0903", "department": "자연과학대학", "major": "수학과"},
    {"id": "0904", "department": "자연과학대학", "major": "화학과"},
    {"id": "1001", "department": "정보통신대학", "major": "반도체시스템공학과"},
    {"id": "1002", "department": "정보통신대학", "major": "반도체융합공학과"},
    {"id": "1003", "department": "정보통신대학", "major": "소재부품융합공학과"},
    {"id": "1004", "department": "정보통신대학", "major": "전자전기공학부"},
    {"id": "1005", "department": "정보통신대학", "major": "차세대반도체공학연계전공"},
    {"id": "1101", "department": "소프트웨어융합대학", "major": "글로벌융합학부 공통"},
    {"id": "1102", "department": "소프트웨어융합대학", "major": "데이터사이언스융합전공"},
    {"id": "1103", "department": "소프트웨어융합대학", "major": "소프트웨어학과"},
    {"id": "1104", "department": "소프트웨어융합대학", "major": "인공지능융합전공"},
    {"id": "1105", "department": "소프트웨어융합대학", "major": "자기설계융합전공"},
    {"id": "1106", "department": "소프트웨어융합대학", "major": "지능형소프트웨어학과"},
    {"id": "1107", "department": "소프트웨어융합대학", "major": "컬쳐앤테크놀로지융합전공"},
    {"id": "1201", "department": "공과대학", "major": "건설환경공학부"},
    {"id": "1202", "department": "공과대학", "major": "건축학과(건축학계열)"},
    {"id": "1203", "department": "공과대학", "major": "기계공학부"},
    {"id": "1204", "department": "공과대학", "major": "나노공학과"},
    {"id": "1205", "department": "공과대학", "major": "신소재공학부"},
    {"id": "1206", "department": "공과대학", "major": "시스템경영공학과"},
    {"id": "1207", "department": "공과대학", "major": "화학공학/고분자공학부"},
    {"id": "1301", "department": "약학대학", "major": "약학과"},
    {"id": "1401", "department": "생명공학대학", "major": "바이오메카트로닉스학과"},
    {"id": "1402", "department": "생명공학대학", "major": "식품생명공학과"},
    {"id": "1403", "department": "생명공학대학", "major": "융합생명공학과"},
    {"id": "1501", "department": "스포츠과학대학", "major": "스포츠과학과"},
    {"id": "1601", "department": "의과대학", "major": "의학과"},
    {"id": "1701", "department": "성균융합원", "major": "글로벌바이오메디컬공학과"},
    {"id": "1702", "department": "성균융합원", "major": "에너지학과"},
    {"id": "1703", "department": "성균융합원", "major": "응용AI융합학부"},
]

for mj in majors:
    doc_ref = db.collection("topic").document(mj["id"])
    doc_ref.set({
        "department": mj["department"],
        "topic": mj["major"]
    })
    print(f"Uploaded {mj['id']} → {mj['department']} / {mj['major']}")

print("All majors uploaded successfully!")