import smtplib
import os
from dotenv import load_dotenv


# TODO: I'll be back for smtp server

class SendEmail:
    def __init__(self, st):
        self.st = st

    def sendEmail(self, email_receive):
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
            self.st.success(
                "Email sent successfully !! Let's take a look at the Image Processing"
            )
            self.st.balloons()
        except Exception:
            if email_receive == "":
                self.st.error("Please fill in the fields")
            else:
                a = os.system("ping www.google.com")
                if a == 1:
                    self.st.error("Please connect your internet connection !")
                else:
                    self.st.error("Wrong Email")
