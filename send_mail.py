import smtplib
from email.mime.text import MIMEText


def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'b23ffbb9eec3fa'
    password = '9d3a5e2d041378'
    message = f"<h3> New Feedback Submission</h3> <ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li> </ul>"

    sender_email = 'necula.leonard.gabriel@gmail.com'
    reciver_email = 'bossul1223@gmail.com'

    msg = MIMEText(message, 'html')
    msg['Subject'] = 'L Feedback'
    msg['From'] = sender_email
    msg['To'] = reciver_email


    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, reciver_email, msg.as_string())