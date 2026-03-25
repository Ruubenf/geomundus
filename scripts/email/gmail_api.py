from email.message import EmailMessage
import mimetypes
import os
import base64
from google_apis import create_service

def send_email(service, to, subject, body, body_type="plain", attachment_paths=None):
    message = EmailMessage()
    message["to"] = to
    message["subject"] = subject

    if body_type.lower() not in ["plain", "html"]:
        raise ValueError("body_type must be either 'plain' or 'html'")

    message.set_content(body)
    message.add_alternative(body, subtype=body_type)

    if attachment_paths:
        for attachment_path in attachment_paths:
            if not os.path.exists(attachment_path):
                raise FileNotFoundError(f"File not found - {attachment_path}")

            filename = os.path.basename(attachment_path)
            mimetype, _ = mimetypes.guess_type(attachment_path)

            maintype, subtype = mimetype.split("/")

            with open(attachment_path, "rb") as attachment:
                attachment_data = attachment.read()

            message.add_attachment(attachment_data, maintype, subtype, filename=filename)
    else:
        raise ValueError("No attachment files")

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

    sent_message = service.users().messages().send(
        userId="me",
        body={"raw": encoded_message}
    ).execute()

    return sent_message

if __name__ == "__main__":
    client_secret_file = "scripts/email/client_secret.json"
    API_SERVICE_NAME = "gmail"
    API_VERSION = "v1"
    SCOPES = ["https://mail.google.com/"]
    service = create_service(client_secret_file, API_SERVICE_NAME, API_VERSION, SCOPES)


    message = EmailMessage()
    message["to"] = "geomunduswebteam@gmail.com"
    message["subject"] = "Testing"
    body = "<h2>just testing</h2> <p>--Validation characters á ñ é è ý @ --<br><br>"
    attachment_path = "scripts/qrs/1 Rubén Femenía Carrascosa.png"

    body_type = "html"

    message.set_content("This is the plain text")
    message.add_alternative("<h2>just testing</h2>", subtype="html")

    if not os.path.exists(attachment_path):
        raise FileNotFoundError(f"File not found - {attachment_path}")

    filename = os.path.basename(attachment_path)
    mimetype, _ = mimetypes.guess_type(attachment_path)

    maintype, subtype = mimetype.split("/")

    with open(attachment_path, "rb") as attachment:
        attachment_data = attachment.read()

    message.add_attachment(attachment_data, maintype, subtype, filename=filename)

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    sent_message = service.users().messages().send(
        userId="me",
        body={"raw": encoded_message}
    ).execute()
