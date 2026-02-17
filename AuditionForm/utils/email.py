import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings


def send_email(to_email, subject, content):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        subject=subject,
        html_content=f"<html><body><p>{content}</p></body></html>",
        sender={
            "name": "SAE India",
            "email": settings.DEFAULT_FROM_EMAIL
        }
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        print("Email sent successfully")
    except ApiException as e:
        print("Brevo API error:", e)
        raise e
