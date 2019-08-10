
사전과제 3. 주택 금융 서비스 API 개발
======================

사양서 https://github.com/jungseok/api1/blob/master/서버개발_사전과제3_주택금융API개발_v.1.1.pdf
MacOS, Python3.7 에서 테스트 되었습니다.

## Requirement
```
Python3+
Flask
SQLAlchemy : Python ORM (Object Relational Mapping)
Pandas : 데이터분석
PyJWT : JSON Web Token
bcrypt : salting, keystretching 이 구현된 암호 알고리즘 - 사용자 암호 저장시 사용
```

## Source File
+api.py - API 소스파일로 configuration, database entity, api logic, routing 으로 구성됨
+test.py - test file


## Quick start
1. 개발에 필요한 모듈을 설치합니다.
```
pip3 install flask Flask-SQLAlchemy sqlite3 pandas PyJWT bcrypt
```
2. Server start
```
python3 api.py
```
3. Run test (새 터미널)
```
python3 test.py
```

## API List (명세순)

[기본 문제 필수] 데이터 파일에서 각 레코드를 데이터베이스에 저장하는 API
```
url: /signup
method: POST
```
+ 파일은 서버에 저장되어 있다고 가정하고 업로드 기능은 구현하지 않음.
+ 파일에서 읽은 금융기관의 수를 리턴함

[기본 문제 필수] 주택금융 공급 금융기관(은행) 목록을 출력하는 API
```
url: /lists
method: POST
```
[기본 문제 필수] 년도별 각 금융기관의 지원금액 합계를 출력하는 API
```
url: /annual_total
method: POST
```
[기본 문제 필수] 각 년도별 각 기관의 전체 지원금액 중에서 가장 큰 금액의 기관명을 출력하는 API
```
url: /max_inst
method: POST
```
[기본 문제 필수] 전체 년도(2005 ~2016)에서 외환은행의 지원금액 평균 중에서 가장 작은 금액과 큰 금액을 출력하는 API
```
url: /foreign
method: POST
```
[ 선택 문제 (옵션)] 특정 은행의 특정 달에 대해서 2018년도 해당 달에 금융지원 금액을 예측하는 API
```
url: /predict
method: POST
```
+ Institution 에 "주택도시기금1)" 도 포함된 것으로 보았음.
+ 농협수협은 하나의 기관명으로 입력하여야 함.
    - 입력 값: ﻿주택도시기금1), ﻿국민은행, ﻿우리은행, ﻿신한은행, ﻿한국시티은행, ﻿하나은행, ﻿농협은행/수협은행, ﻿외환은행, ﻿기타은행

[추가 제약사항 옵션] signup 계정생성 API
```
url: /signup
method: POST
```
[추가 제약사항 옵션] signin 로그인 API
```
url: /signin
method: POST
```
[추가 제약사항 옵션] refresh 토큰 재발급 API
```
url: /refresh_token
method: POST
```

## Postman documentation
https://documenter.getpostman.com/view/8400950/SVYupwU9?version=latest#2e47c5c7-924b-432c-bde7-0e5ac82aab9d





