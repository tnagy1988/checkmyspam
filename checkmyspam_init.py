from main import process_emails
import time

if __name__ == '__main__':
    while True:
        process_emails()
        time.sleep(2)