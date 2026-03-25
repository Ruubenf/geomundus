# 📌 Geomundus QRcodes

**Geomundus QRcodes** is a **client–server application** that helps the Geomundus staff track attendance at the conference, send updates via email, and issue participation certificates.  

---

## ⚙️ Server

- **Framework:** 🐘 PHP
- **Database:** 💾 Remote mySQL database
- **Core functionalities:**  
  - ✅ Register conference attendance  
  - 🧩 Track workshops participation
  - 📑 Know to whom the certificates should be issued

---

## 💻 Client

- **Technologies:** 🌐  JS + HTML + CSS
- **Responsibility:** Send actions to the server (e.g. register attendees, fetch info).

---

## 🛠️ Scripts

Located in the `**scripts/`** folder:  

- 🖼️ Generate QR codes images  
- 🗄️ Create SQL insert statements from a `attendees.csv` file 
- 🚀 Send automated conference updates via email
- 📂 Generated outputs:  
  - QR codes → `scripts/qrs/`  
  - SQL inserts → `scripts/db/2-insert_attendees.sql`

---


## 🚀 How to run the project

1. Create the database
  - Open phpMyAdmin and create a database db
  - Execute `scripts/db/1-create-tables.sql`

2. Populate the database and generate QR files
  - Run `geenrate_qrs&db_inserts.py`
  - Execute `scripts/db/2-insert_attendees.sql` in the database

3. Generate the badges pdf
  - Run `generate_badges_pdf.py`

4. Send the QR codes trough email
  - Generate `client_secret.json` from the gogole developer console
  - Fill the information in the `email/` scripts.
  - Run `google_apis.py` for testing and token_files generation
  - Finaly run `send_emails.py`

5. Website deployment
  - Fill database information in `webapp/database.php`
  - Upload all files inside `webapp/` to the server
