from extensions import mail
from flask_mail import Message
from dotenv import load_dotenv
import os

load_dotenv()

def s_code(email: str, code: str)-> tuple:
    try:
        msg = Message(subject= "RecetasAPI verification code",
                            sender= os.getenv("M_USERNAME"),
                            recipients=[email],
                            body=f""" Hello,

                            Your verification code to update your recipe in RecetasAPI is: {code}

                            Thank you!""")
        
        mail.send(msg)
        return True, "If the email address is valid and exists, you will receive a verification code within the next few minutes. Please check your inbox and spam folder."
    except Exception as e:
        print("SENDING EMAIL", e)
        return False, "There was an issue sending your email. Please, check all the details are correct."