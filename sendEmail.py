import smtplib
import os
from dotenv import load_dotenv


def sendEmail(email_receive):
    load_dotenv()
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        # server.starttls()
        server.login(email, password)
        subjectToMe = f"You've got new Message from {email_receive}"
        subjectToUser = f"Thanks for contacting me.."
        bodyToUser = f"Hello {email_receive} !! This website will help you to process your images and you can also download its image"
        bodyToMe = f"{email_receive} has just subscribed to your website"
        messageToUser = f"Subject: {subjectToUser}\n\n{bodyToUser}"
        messageToMe = f"Subject: {subjectToMe}\n\n{bodyToMe}"
        server.sendmail(email, email_receive, messageToUser)
        server.sendmail(email_receive, email, messageToMe)
        server.quit()
    except Exception as err:
        print(err)
