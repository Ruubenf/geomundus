import qrcode
import qrcode.constants
from qrcode.image.styles.moduledrawers.pil import VerticalBarsDrawer
from qrcode.image.styledpil import StyledPilImage
from urllib.parse import urlparse, urlunparse
import pandas as pd

# Insert attendee with this email if he didn't registerd with one
DEFAULT_EMAIL = "geomunduswebteam@gmail.com"

def clean_linkedin_url(url):
    # Return linkedin personal page without the social media sharing params
    if len(url) > 28 and url[:28] == "https://www.linkedin.com/in/":         
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
    
    return url # If the website is not from linkedin, do nothing

def get_registration_df():

    # 1. Read csv
    df = pd.read_csv("scripts/Confirmed List.csv", encoding="utf-8", sep=";")

    # 3. Keep only required columns
    df = df[["fullName", "website", "email"]]

    # 4. Rename the columns according to the final name
    df = df.rename(columns={"fullName": "name"})

    # 5. Remove linkedin webpage unnecesary params
    df["website"] = df["website"].apply(clean_linkedin_url)

    return df

def generate_qr(id, name, link):

    # 1. Insert geomundus_id to the provided link
    # 1.1 If the link has no params:
    if '?' not in link:
        data = f"{link}?gmcid={id}" # Start param list with '?'
    else:
        data = f"{link}&gmcid={id}" # Append gmcid param with '&'

    # 2. Build the qr code image name
    file_name = f"{id} {name}.png" # Example: '1 Rubén Femenía Carrasocosa.png'

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # H for high redundancy
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Style QR the code
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=VerticalBarsDrawer()) 

    # Store the qr picture with the attendee id and name
    img.save("./scripts/qrs/"+file_name)

    return data



if __name__ == '__main__':

    attendees = get_registration_df() 

    with open('scripts/db/2-insert_attendees.sql', 'w', encoding = "utf-8") as attendees_inserts:
    # Output example in file: INSERT INTO attendees (id, name) VALUES (1, 'Rubén Femenía Carrascosa');
        for i in range(len(attendees)):
            attendee = attendees.iloc[i]
            attendee_name = attendee['name']
            attendee_email = attendee['email'] if attendee['email'] is not None else DEFAULT_EMAIL
            
            qr_text = generate_qr(i, attendee_name, attendee['website'])
            
            # TODO Warning: check for SQL Injection
            attendees_inserts.write(f"INSERT INTO attendees (id, name, email) VALUES ({i}, '{attendee_name}', '{attendee_email}');\n")
            
