from google_apis import create_service
from pathlib import Path
from gmail_api import send_email
import pandas as pd

client_secret_file = "client_secret.json"
API_SERVICE_NAME = "gmail"
API_VERSION = "v1"
SCOPES = ["https://mail.google.com/"]
service = create_service(client_secret_file, API_SERVICE_NAME, API_VERSION, SCOPES)

df = pd.read_csv("scripts/attendees.csv", sep=";", encoding="utf-8")
df = df[["fullName", "email", "id"]] 
df["id"] = df["id"] - 1 # id has to be -1 because the qr code file names starts from 0, and the id starts from 1

subset_ids = [1]
subset = df[df["id"].isin(subset_ids)] # Change to 'subset = df.copy()' to send the emails to all attendees

index = 0
while index < len(subset):
    row_index = subset_ids[index] # In case there are gaps in the 'id' column
    to_address = subset.loc[row_index, "email"]
    attendee = subset.loc[row_index, "fullName"]
    id = subset.loc[row_index, "id"]
    qr_file = f"{id} {attendee}.png"

    email_subject = "GeoMundus 2025 – Information for Participation"
    email_body = f"""
    Dear {attendee},<br><br>
    We are delighted to welcome you to the <b>GeoMundus 2025 Conference – Geospatial Technologies for Smart Cities</b>, which will take place from <b>October 17th to 18th</b> at Universidade NOVA de Lisboa, Information Management School (IMS), Campus Campolide, 1070-312, Lisboa, Portugal.<br><br>
    <b>The conference will begin at 9:00 am on October 17th</b>, so please plan to arrive early to complete your check-in (<u>registration will start at 8:30 am</u>) and make the most of the opening session.<br><br>
    We are also pleased to invite you to join our <b>Walking Tour on October 16th from 16:30 - 18:30 pm</b> for participants arriving early. We will explore the city’s most iconic landmarks. Details on the meeting point and route will be sent soon via WhatsApp Community. If you haven’t joined yet, here is the group link: <br>https://chat.whatsapp.com/DubVNXoXCv9Dc4DwetIEKu 
    <br><br>Attached to this email, <b>you will find your personalized conference QR code</b>. Please note that:<br>
    <ul>
        <li>The QR code serves as your official access pass to all conference sessions, workshops and social events.</li>
        <li>You must present it on your mobile device at the registrations desk on the first day, where we are going to give you the printed version.</li>
        <li>The QR code is personal and non-transferable.</li>
        <li>The QR code gives you access to dinner and lunch.</li>
        <li>You can scan with your phones the QR code from the participants to connect with them on LinkedIn or to see their personal webpage.</li>
    </ul>
    <br>
    We invite you to review the full conference program on our website: https://geomundus.org/ <br><br>
    In case of any questions or required assistance, please do not hesitate to contact us or to look for GeoTech Staff at the day of the conference.<br><br>
    We look forward to see you soon!<br><br>
    Best Regards,<br><br>
    GeoMundus 2025 - Program and Web Teams<br>
    """

    attachment_dir = "scripts/qrs"
    attachment_files = [f"{attachment_dir}/{qr_file}"]

    print(attachment_files)

    # Send the email
    response_mail_sent = send_email(
        service,
        to_address,
        email_subject,
        email_body,
        body_type="html",
        attachment_paths=attachment_files
    )
    print(response_mail_sent)

    index += 1