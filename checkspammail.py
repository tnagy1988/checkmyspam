import imaplib
import email

# IMAP server details for net.hr
IMAP_SERVER = 'imap.net.hr'
IMAP_PORT = 993

# Net.hr email account credentials
EMAIL_ADDRESS = 'toster1337@net.hr'
PASSWORD = 'Toster123456789'

def process_spam_emails():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # Login to the email account
    mail.login(EMAIL_ADDRESS, PASSWORD)

    # Select the mailbox (inbox by default)
    mail.select()

    # Search for all emails
    _, data = mail.search(None, 'ALL')

    # Get a list of email IDs
    email_ids = data[0].split()

    # Loop through the email IDs and fetch the corresponding emails
    for email_id in email_ids:
        _, email_data = mail.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1].decode('utf-8')

        # Parse the email object
        email_message = email.message_from_string(raw_email)

        # Extract the email subject
        subject = email_message['Subject']

        if "OVO JE SPAM" in subject:
            print('Subject:', subject)

            # Extract the sender email address
            sender_email = email.utils.parseaddr(email_message['From'])[1]
            print('Sender Email:', sender_email)

            print('------------------------------------')

            # Delete the email
            mail.store(email_id, '+FLAGS', '\\Deleted')

    # Permanently remove deleted emails from the mailbox
    mail.expunge()

    # Logout from the email account
    mail.logout()

# Call the function to process spam emails
process_spam_emails()
