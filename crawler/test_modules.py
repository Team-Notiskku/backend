from configs.config_topic_map import mapper, keywords_list

def send_notice(keywords, title):
    for keyword in keywords:
        mapped_topic = mapper[keyword]
        topic_type = mapped_topic[0:2]
        topic_details = mapped_topic[2:4]

        if topic_type == "00":
            message = messaging.Message(
                data={
                    "title": title,
                    "body": f"‘{keyword}’ 관련 공지가 새로 업데이트 되었어요!",
                },
                topic=topic_details
            )
            # 실제 전송
            response = messaging.send(message)
            print("전송 완료:", response)
    

title = "AI캡스톤프로젝트 교과목 WE-Meet 프로젝트 수업 수강신청 안내"

found = [k for k in keywords_list if k in title]

if found:
    send_notice(found, title)
else:
    print("포함된 키워드 없음")