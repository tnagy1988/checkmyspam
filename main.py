import imaplib
import email
# import ipaddress
import tldextract

# IMAP server details for net.hr
IMAP_SERVER = 'imap.net.hr'
IMAP_PORT = 993

# Net.hr email account credentials
EMAIL_ADDRESS = 'toster1337@net.hr'
PASSWORD = 'Toster123456789'

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

        # Extract the email subject
        subject = email_message['Subject']

        sender_email = email.utils.parseaddr(email_message['From'])[1]

        # Extract the sender domain from the sender email address
        sender_domain = sender_email.split('@')[-1]

        # Extract the TLD (top-level domain) from the sender domain
        tld = tldextract.extract(sender_domain).suffix
        
        spf_header = email_message.get('Received-SPF')
        
        geolocation = email_message.get('X-GEO')

        if subject == 'NOOB' or tld == 'ru':

            # Extract the client IP from the headers
            # client_ip = email_message.get('Client-Ip')

            # Extract the SPF information if available
            
            # client_ip = ''
            # if spf_header:
            #     spf_fields = spf_header.split(';')
            #     for field in spf_fields:
            #         if 'client-ip=' in field:
            #             client_ip = field.split('=')[1].strip()

            # Extract the geolocation if available
            

            print('Subject:', subject)
            print('Sender Email:', sender_email)
            # print('Client-Ip', client_ip)
            print('TLD:', tld)
            print('Geolocation:', geolocation)
            print('SPF:', spf_header)
            print('------------------------------------')


            # Move the email to the "NEMOZE" folder
            # mail.copy(email_id, 'NEMOZE')

            # Delete the email
            # mail.store(email_id, '+FLAGS', '\\Deleted')
        else:
            # Set the email as unread
            mail.store(email_id, '-FLAGS', '\\Seen')
    # Permanently remove deleted emails from the mailbox
    # mail.expunge()

    # Logout from the email account
    mail.logout()

# Call the function to process emails
process_emails()