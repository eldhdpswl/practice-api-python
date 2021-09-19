# news api 기본 사용
import json
import requests


def get_news(keywords, client_id, client_secret):
    """
    - 네이버 검색 뉴스 API 사용해 특정 키워드들의 뉴스 검색
    - 수집 데이터를 기반으로 Naver News 페이지 존재 여부를 
    뉴스 item 항목에 추가
    :params list keywords: 키워드 리스트
    :params str client_id: 인증정보
    :params str client_secret: 인증정보
    :return news_items : API 검색 결과 중 뉴스 item들
    :rtype list
    """
    news_items = []

    for keyword in keywords:
        # B. API Request
        # B-1. 준비하기 - 설정값 세팅
        url = 'https://openapi.naver.com/v1/search/news.json'

        sort = 'date'  # sim: similarity 유사도, date: 날짜
        display_num = 100
        start_num = 1

        params = {'display': display_num, 'start': start_num,
                  'query': keyword.encode('utf-8'), 'sort': sort}
        headers = {'X-Naver-Client-Id': client_id,
                   'X-Naver-Client-Secret': client_secret, }

        # B-2. API Request
        r = requests.get(url, headers=headers,  params=params)

        # C. Response 결과
        # C-1. 응답결과값(JSON) 가져오기
        # Request(요청)이 성공하면
        if r.status_code == requests.codes.ok:
            result_response = json.loads(r.content.decode('utf-8'))

            result = result_response['items']
            for item in result:
                originallink = item['originallink']
                link = item['link']

                # ===naver news 페이지 여부 항목 추가====
                # naver news 페이지가 없다면
                if originallink == link:
                    item['naverNews'] = 'N'
                # naver news 페이지가 있다면
                else:
                    item['naverNews'] = 'Y'

        # Request(요청)이 성공하지 않으면
        else:
            print('request 실패!')
            failed_msg = json.loads(r.content.decode('utf-8'))
            print(failed_msg)

        news_items.extend(result)

    return news_items


# =======TEST==========
# API Request 설정값
client_id = '내 client id'
client_secret = '내 client secret'
keywords = ['KOVO', '여자 배구']  # 뉴스 검색할 키워드

news_items = get_news(keywords, client_id, client_secret)
print(len(news_items))  # 총 뉴스 갯수 출력
print(news_items[0])  # 뉴스 정보 출력
print(news_items[1])  # 뉴스 정보 출력
