import imaplib
import email
import tldextract
from blacklist import BLACKLISTED
from credentials import (EMAIL_ADDRESS, PASSWORD)
import smtplib
from email.mime.text import MIMEText

# IMAP server details for net.hr
IMAP_SERVER = 'imap.net.hr'
IMAP_PORT = 993

# Net.hr email account credentials
EMAIL_ADDRESS = EMAIL_ADDRESS
PASSWORD = PASSWORD

def process_emails():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # Login to the email account
    mail.login(EMAIL_ADDRESS, PASSWORD)

    # Select the mailbox (inbox by default)
    mail.select()

    # Search for unread emails with the specified subject
    _, data = mail.search(None, 'UNSEEN')

    # Get a list of email IDs
    email_ids = data[0].split()

    # Loop through the email IDs and fetch the corresponding emails
    for email_id in email_ids:
        _, email_data = mail.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1].decode('utf-8')

        # Parse the email object
        email_message = email.message_from_string(raw_email)

        sender_email = email.utils.parseaddr(email_message['From'])[1]

        # Extract the sender domain from the sender email address
        sender_domain = sender_email.split('@')[-1]

        # Extract the TLD (top-level domain) from the sender domain
        tld = tldextract.extract(sender_domain).suffix

        # Extract the SPF header
        spf_header = email_message.get('Received-SPF')

        if spf_header and not 'Pass' in spf_header or tld in BLACKLISTED:
            try:
                sender_email = 'tostiranje@gmail.com'
                receiver_email = 'tostiranje@gmail.com'
                subject = 'Test Email'
                message = 'This is a test email.'
                msg = MIMEText(message)
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = receiver_email
                smtp = smtplib.SMTP('smtp.freesmtpservers.com', 25)
                smtp.sendmail(sender_email, receiver_email, str(msg))
                smtp.quit()
                print("Email sent successfully")
            except smtplib.SMTPException as e:
                print("Error sending email:", str(e))

            # Delete the email
            mail.store(email_id, '+FLAGS', '\\Deleted')
        else:
            # Set the email as unread
            mail.store(email_id, '-FLAGS', '\\Seen')

    # Permanently remove deleted emails from the mailbox
    mail.expunge()

    # Logout from the email account
    mail.logout()


# Call the function to process emails
process_emails()