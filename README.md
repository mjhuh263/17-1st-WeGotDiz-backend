![다운로드](https://user-images.githubusercontent.com/65124480/109489263-f0173500-7ac9-11eb-850c-062b9f1a828d.jpg)

# WeGotDiz
<br>

## 팀 구성원
프론트엔드  3명, 백엔드 3명
<br>

## 프로젝트 기간
2021.02.15 ~ 2021.02.26
<br>

## 기술 스택
Python, Django, MySQL, AWS
<br>

---

## 구현 기능 

### 모델링

- ERD(관계형 모델링 설계) 및 model 생성 / Aquery Tool을 활용한 항공, 숙박 모델링 구현 및 models.py 생성
- DB CSV 파일 작성
- db_uploader.py 작성

<br>

### 회원가입 및 로그인 (SignUp & SignIn)

- bcrypt를 사용한 암호화
- 자체 로그인 기능 구현 및 unit test 
- jwt access token 전송 및 유효성 검사 기능 구현
- 비회원, 회원 decorator 기능 구현 

<br>

### 마이페이지

- 회원 좋아요 목록 기능 구현
- 회원 펀딩한 목록 기능 구현

<br>

### 카테고리/메인

- 상품 전체 리스트 및 Django ORM(Q객체)을 활용한 특정 카테고리 리스트 기능 구현
- 기획전 별 상품 리스트 기능 구현

<br>

### 프로덕트(Product)


- 회원 비회원 구분 없이 프로덕트 상세 정보 확인 기능 구현
- 로그인한 회원만 프로덕트 좋아요 기능 반영되도록 기능 구현  

<br>

### 결제/주문(Order) 

- 결제 진행할 프로덕트의 세부 상품 리스트 나열 기능 및 정보 입력, 결제 기능 구현 
- 사용자 결제 금액과 수량에 따라 프로덕트의 총 펀딩 금액, 총 리워드 구매 수량 업데이트 기능 구현

<br>
