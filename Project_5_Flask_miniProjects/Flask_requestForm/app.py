import os
from email_validator import validate_email, EmailNotValidError
from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = "움하하하하하하!"

# Mail클래스 컨피그 추가
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 확장을 등록한다
mail = Mail(app)


# 시작페이지를 /conatct로 보이기 위해 리다이렉트
@app.route("/")
def home():
    return redirect("contact")


@app.route("/contact")
def contact():
    return render_template("index.html")


@app.route("/contact_save", methods=["POST"])
def contact_save():
    description = request.form.get("description", "")
    username = request.form.get("username", "")
    mail = request.form.get("mail", "")

    # 세션에 저장
    session["description"] = description
    session["username"] = username
    session["mail"] = mail

    # 사용자의 입력 유효성 체크
    is_valid = True
    if not username:
        flash("사용자 명은 필수입니다.")
        is_valid = False

    # 사용자의 입력 체크
    if not mail:
        flash("메일 주소는 필수입니다.")
        is_valid = False

    # 메일 주소 검증 체크
    try:
        validate_email(mail)
    except EmailNotValidError:
        flash("메일 주소 형식으로 입력해주세요. 예시) abc@abc.com")
        is_valid = False
    # 사용자의 입력 체크
    if not description:
        flash("문의 내용은 필수입니다.")
        is_valid = False

    # 사용자의 입력 체크 중 하나라도 통과못하면 false => 최초 페이지로 redirection
    if not is_valid:
        return redirect(url_for("contact"))

    # 위의 모든 사항이 문제가 없다면 complete로 엔드포인트 설정
    return redirect(url_for("complete"))


@app.route("/complete", methods=["POST", "GET"])
def complete():
    description = session.get("description", "")  # 세션에 저장한 값 가지고 오기
    username = session.get("username", "")
    mail = session.get("mail", "")
    # 유효성 검증 => session에 저장된 값이 없다면 처음페이지로 redirection
    if (
        not session.get("description")
        or not session.get("username")
        or not session.get("mail")
    ):
        return redirect("contact")

    flash(
        f"{username}님 문의내용이 정상적으로 전달되었습니다. 문의해주셔서 감사합니다."
    )

    # 작성 내용을 메일로 전달
    send_email(
        mail,
        "문의 감사합니다.",
        "contact_mail",
        username=username,
        description=description,
    )

    # 세션 저장정보 삭제
    session.pop("description", None)
    return render_template("contact_complete.html", description=description)


def send_email(to, subject, template, **kwargs):
    # 메일을 송신하는 함수
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


if __name__ == "__main__":
    app.run(port=4000, debug=True)
