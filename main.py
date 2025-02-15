from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from send_email import SendMessage
from utils import logging
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define email request schema
class EmailRequest(BaseModel):
    sender_name: str
    sender_email: EmailStr
    subject: str
    message: str

@app.post("/send_mail")
async def contact(email_data: EmailRequest):
    try:
        mail_object = SendMessage(
            sender_name=email_data.sender_name,
            sender_email=email_data.sender_email,
            sender_subject=email_data.subject,
            sender_message=email_data.message,
        )
        
        result = mail_object.send_email()
        
        if result["status"] == "success":
            logging.info("Email sent successfully.")
            return {"status": "success", "message": "Email sent successfully."}
        else:
            raise HTTPException(status_code=500, detail=result["message"])

    except Exception as e:
        logging.error(f"Could not send email due to: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
