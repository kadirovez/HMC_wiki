
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from email.utils import formataddr
from fastapi import HTTPException
from starlette import status

from src.core.settings import settings


# async def send_email(
#         receiver_email: str,
#         subject: str,
#         body: str
# ) -> None:
#     """Send email via SMTP. Native async using aiosmtplib."""
#     try:
#         msg = MIMEMultipart()
#         msg["From"] = formataddr((settings.smtp_sender_name, settings.smtp_sender_email))
#         msg["To"] = receiver_email
#         msg["Subject"] = subject
#         msg.attach(MIMEText(body, "html"))
#
#         ssl_context = ssl.create_default_context()
#         ssl_context.check_hostname = False
#         ssl_context.verify_mode = ssl.CERT_NONE
#
#         await aiosmtplib.send(
#             msg,
#             hostname=settings.smtp_server,
#             port=settings.smtp_port,
#             username=settings.smtp_user,
#             password=settings.smtp_password,
#             start_tls=True,
#             tls_context=ssl_context,
#         )
#
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Failed to send email: {str(e)}"
#         )

async def send_email(generated_otp):
    print(generated_otp)
    return generated_otp

