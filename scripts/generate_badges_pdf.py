from fpdf import FPDF
import pandas as pd

BADGE_BLUEPRINT = "badge.jpg"
ATTENDEES_CSV = "attendees.csv"

def add_badge(pdf, x, y):
    # Add blueprint badge picture to the pdf
    pdf.image(BADGE_BLUEPRINT, x=x, y=y, w=105)

def add_qr(pdf, qr, x, y):
    # Add QR code image
    pdf.image(qr, x=x+35, y=y+69, w=35)

def add_name(pdf, name, x, y):
    # Add the attendant's name
    pdf.set_text_color(0,0,0)
    pdf.set_font('liberation', '', 20)

    pdf.set_xy(x+4, y+47)
    pdf.cell(95, 12, name, align="center")

def add_affiliation(pdf, university, x, y):
    # Add the attendant's university
    pdf.set_text_color(55,55,55)
    pdf.set_font('liberation','', 14)

    pdf.set_xy(x+4, y+55)
    pdf.cell(95, 12, university, align="center")

pdf = FPDF('P', 'mm', 'A4')

# Add a page
pdf.add_page()
pdf.set_text_color(0,0,0)

# Import data
df = pd.read_csv(ATTENDEES_CSV, encoding="utf-8", sep=";")

# Filter columns
df = df[["fullName", "affiliation"]]

# Set a grid 
x_offset = pdf.w / 2
y_offset = pdf.h / 2

# Set badge text font family
pdf.add_font(family="liberation", style="", fname="LiberationSans-BaDn.ttf")

# Each page will have 4 badges
row_index = 0
while row_index < len(df):
    for i in range(2):
        for j in range(2):
            
            if row_index >= len(df): # Stop if there are no remaining badges to generate
                break

            # Gather all attendee data
            name = df.loc[row_index, "fullName"]
            affiliation = df.loc[row_index, "affiliation"]
            affiliation = affiliation.replace("Ã¼", "ü") # MÃ¼nster to Münster
            qr = f"qrs/{row_index} {name}.png"

                
            # Add badge picture
            add_badge(pdf, x_offset * j, y_offset * i)

            # Add attendant's name and university/affiliation
            add_name(pdf, name, x_offset * j, y_offset * i)
            
            add_affiliation(pdf, affiliation, x_offset * j, y_offset * i)

            # Add qr code
            add_qr(pdf, qr, x_offset * j, y_offset * i)

            row_index += 1
    
    pdf.add_page()

# Store the generated pdf with all attendees badges
pdf.output('badges.pdf')