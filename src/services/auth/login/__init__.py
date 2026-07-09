
from src.services.auth.login.cancel_login import cancel_login
from src.services.auth.login.complete_login import complete_login
from src.services.auth.login.confirm_email_otp import confirm_email_otp
from src.services.auth.login.send_email_otp import send_email_otp
from src.services.auth.login.validate_email import validate_email
from src.services.auth.login.validate_password import validate_password


class LoginServices:
    validate_email = staticmethod(validate_email)
    validate_password = staticmethod(validate_password)
    complete_login = staticmethod(complete_login)
    cancel_login = staticmethod(cancel_login)


login_service = LoginServices()
