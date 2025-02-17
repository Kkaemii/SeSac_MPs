import smtplib

smtp_server = "smtp.gmail.com"
port = 587  # TLS 포트
sender_email = "your mail"
password = " app password"

try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  # TLS 보안 연결
    server.login(sender_email, password)
    print("SMTP 서버 연결 성공!")
except Exception as e:
    print(f"오류 발생: {e}")
finally:
    server.quit()
