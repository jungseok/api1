
import requests
import json
import time

HOST = "http://localhost:5000"
#HOST = "http://127.0.0.1:5000/"
JWT_TOKEN = ""


def test_create():
    url = HOST + '/create'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': JWT_TOKEN
    }
    response = requests.request('POST', url, headers = headers, data=json.dumps(payload))
    print(response.text)

    url = HOST + '/create'
    payload = {
        "filename" : "서버개발_사전과제3_주택금융신용보증_금융기관별_공급현황.csv"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': JWT_TOKEN
    }
    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
    print(response.text)


def test_lists():
    url = HOST + '/lists'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': JWT_TOKEN
    }
    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
    print(response.text)


def test_annual_total():
    url = HOST + '/annual_total'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': JWT_TOKEN
    }
    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
    print(response.text)


def test_foreign():
    url = HOST + '/foreign'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': JWT_TOKEN
    }
    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
    print(response.text)


def test_max_inst():
    url = HOST + '/max_inst'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': JWT_TOKEN
    }
    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
    print(response.text)


def test_predict():
    url = HOST + '/predict'
    payload = {
        "bank": "국민은행",
        "month": 2
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': JWT_TOKEN
    }
    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))

    print(response.text)


def test_signup():
    url = HOST + '/signup'
    payload = {
        "username": "test2",
        "password": "test1"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': JWT_TOKEN
    }
    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))

    print(response.text)


def test_login():
    url = HOST + '/login'
    payload = {
        "username": "test1",
        "password": "test33"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': JWT_TOKEN
    }
    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()


def test_refresh_token():
    url = HOST + '/refresh_token'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + JWT_TOKEN
    }
    response = requests.request('POST', url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()


if __name__ == '__main__':

    # [추가 제약사항 옵션] signup 계정생성 API
    #    새 아이디를 등록한다. 기존 아이디가 있으면 에러가 나므로 테스트 함수의 아이드를 수정한다.
    test_signup()

    # [추가 제약사항 옵션] signin 로그인 API
    tok = test_login()
    if 1: # 0 으로 바꾸면 API 호출이 되지 않음
        JWT_TOKEN = tok['token']
        print("initial token: " + JWT_TOKEN)

    # [추가 제약사항 옵션] refresh 토큰 재발급 API
    time.sleep(2)   # 시간이 1초 보다 빨리 갱신하려고 하면 같은 토큰이 나온다.
    retok = test_refresh_token()
    JWT_TOKEN = retok['token']
    print("refresh token: " + JWT_TOKEN)

    # [기본 문제 필수] 데이터 파일에서 각 레코드를 데이터베이스에 저장하는 API
    test_create()

    # [기본 문제 필수] 주택금융 공급 금융기관(은행) 목록을 출력하는 API
    test_lists()

    # [기본 문제 필수] 년도별 각 금융기관의 지원금액 합계를 출력하는 API
    test_annual_total()

    # [기본 문제 필수] 각년도별각기관의전체지원금액중에서가장큰금액의기관명을출력하는API
    test_max_inst()

    # [기본 문제 필수] 전체 년도(2005 ~2016)에서 외환은행의 지원금액 평균 중에서 가장 작은 금액과 큰 금액을 출력하는 API
    test_foreign()

    # [ 선택 문제 (옵션)] 특정 은행의 특정 달에 대해서 2018년도 해당 달에 금융지원 금액을 예측하는 API
    test_predict()

