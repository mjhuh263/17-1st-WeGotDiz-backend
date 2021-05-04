![다운로드](https://user-images.githubusercontent.com/75108432/116838439-4d824c00-ac09-11eb-81db-0832c30d643a.png)

# WeGotDiz

## 팀 구성원
프론트엔드 3명, 백엔드 3명
<br>

## 프로젝트 기간
2021.02.15 ~ 2021.02.26
<br>

## 기술 스택
Python, Django, MySQL
<br>

## 프로젝트 설명 
와디즈를 모티브로 진행한 크라우드 펀딩 웹사이트 프로젝트입니다.
<br>

## Document

[API Document](https://www.notion.so/Wegotdiz-API-Document-49c065fa5a024232a744a4e160eef3bd, "API Document")

<br>

## 프로젝트 결과 시연 영상

[Youtube](https://www.youtube.com/watch?v=EJ8G5lN2NZs&t=26s)

## 프로젝트 구조
프로젝트 구조는 아래와 같습니다.
<br>

Project: 
- WeGotDiz


Apps:
- community
- product
- purchase
- user

<br>

```
.
├── WeGotDiz
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── community
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── product
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── pull_request_template.md
├── purchase
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements.txt
└── user
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── utils.py
    ├── validators.py
    └── views.py
```
<br>

## ERD

![](https://user-images.githubusercontent.com/75108432/116532170-ec156100-a91a-11eb-841f-84d6c6b3f380.png)

## 구현 기능 

### 모델링

- ERD(관계형 모델링 설계) 및 model 생성 / Aquery Tool을 활용한 항공, 숙박 모델링 구현 및 models.py 생성
- DB CSV 파일 작성
- db_uploader.py 작성

### 회원가입 및 로그인 (SignUp & SignIn)

- bcrypt를 사용한 암호화
- 자체 로그인 기능 구현 및 unit test 
- jwt access token 전송 및 유효성 검사 기능 구현
- 비회원, 회원 decorator 기능 구현 

### 마이페이지

- 회원 좋아요 목록 기능 구현
- 회원 펀딩한 목록 기능 구현

### 카테고리/메인

- 상품 전체 리스트 및 Django ORM(Q객체)을 활용한 특정 카테고리 리스트 기능 구현
- 기획전 별 상품 리스트 기능 구현

### 프로덕트(Product)

- 회원 비회원 구분 없이 프로덕트 상세 정보 확인 기능 구현
- 로그인한 회원만 프로덕트 좋아요 기능 반영되도록 기능 구현  

### 결제/주문(Order) 

- 결제 진행할 프로덕트의 세부 상품 리스트 나열 기능 및 정보 입력, 결제 기능 구현 
- 사용자 결제 금액과 수량에 따라 프로덕트의 총 펀딩 금액, 총 리워드 구매 수량 업데이트 기능 구현

<br>

## 프로젝트 Set- Up 

1. **Miniconda(가상환경 tool) 설치** <br>
[제 블로그 게시물](https://velog.io/@mjhuh263/TIL-47-Python-Installing-Miniconda3-and-creating-virtual-envs-%EB%AF%B8%EB%8B%88%EC%BD%98%EB%8B%A4-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0)에 적어 놓았습니다.

<br>

2. **Database 생성**
```
$ mysql server start
$ mysql -u root -p 
$ mysql> create database wegotdiz character set utf8mb4 collate utf8mb4_general_ci;
```
<br>

3. **프로젝트에 필요한 python package 설치**
```
$ pip install django
$ pip install django-cors-headers
$ pip install mysqlclient
```
<br>

3. **Django Project, App 생성**
```
$ django-admin startproject WeGotDiz
$ cd project
$ python manage.py startapp community
$ python manage.py startapp product
$ python manage.py startapp purchase
$ python manage.py startapp user
```
<br>

4. **.gitignore 생성** <br>
```
cd wegotdiz -> project folder name
touch .gitignore
vi .gitignore -> ignore하고 싶은 키워드 추가하고 저장
```
5. **보안 파일 생성** <br>
프로젝트 파일 settings.py 속 secret key 및 database 정보를 `my_settings.py`으로 따로 관리한다.

my_settings.py 생성:
```
cd wegotdiz -> project folder name
touch my_settings.py
vi my_settings.py
```
+) my_settings.py를 꼭 .gitignore에 추가한다.

my_settings.py 속 정보:
```
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wegotdiz',
        'USER': 'DB 계정명',
        'PASSWORD': 'DB 비밀번호',
        'HOST': 'DB 주소',
        'PORT': '포트번호',
    }
}

SECRET = 'django에서 생성한 시크릿키'
```
<br>
