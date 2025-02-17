## Flask 이메일 문의 시스템 프로젝트

### 📝 프로젝트 소개

## Flask와 Gmail SMTP를 활용하여 사용자의 문의사항을 세션에 저장하고 관리자에게 자동으로 이메일을 전송하는 웹 애플리케이션 구현

---

### 🛠 사용 기술

- Python
- Flask: 웹 프레임워크
- Flask-Mail: 이메일 전송
- python-dotenv: 환경변수 관리
- email-validator: 이메일 유효성 검증
- SMTP: Gmail 서버 연동

### ⚙ 주요 기능

#### 사용자 입력 처리

- 사용자명
- 이메일 주소
- 문의 내용
- 입력 데이터 세션 저장

#### 유효성 검증

- 필수 입력 항목 검증
- 이메일 형식 검증
- Flash 메시지를 통한 에러 표시

#### 이메일 전송

- Gmail SMTP 서버 연동
- 자동 응답 메일 발송
- HTML/텍스트 형식 지원

### 💡 기술적 특징

- 환경변수를 통한 보안 정보 관리
- 세션을 활용한 데이터 임시 저장
- SMTP TLS 보안 연결
- 템플릿 기반 이메일 포맷팅

### 📁 프로젝트 구조
```
📦Flask_requestForm
┣ 📂static
┃ ┗ 📜style.css
┣ 📂templates
┃ ┣ 📜contact_complete.html
┃ ┣ 📜contact_mail.html
┃ ┣ 📜contact_mail.txt
┃ ┗ 📜index.html
┣ 📜app.py
┗ 📜smtptest.py
```

### 🔒 보안 설정

- Gmail App Password 사용
- TLS 암호화 통신
- 환경변수를 통한 민감정보 관리

### 실행

```python
flask run
```
