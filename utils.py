from rest_framework.response import Response
from rest_framework import status
from usibras_admin import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sentry_sdk
import smtplib

import threading

def send_email(email, subject, body):
    try:
        # create message object instance
        msg = MIMEMultipart()

        message = body

        msg['From'] = settings.EMAIL_FROM
        msg['To'] = email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'html'))

        # create server
        server = smtplib.SMTP(settings.EMAIL_HOST + ": " + settings.EMAIL_PORT.__str__())

        server.starttls()

        # Login Credentials for sending the mail
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()

        return 200

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return 500


def send_email_to_owner(owner_email, type_payment):
    if type_payment not in owner_email.available_in_libraries.type_payments_accepted.all():
        return Response(
            {'message': 'Método de pagamento não aceito pela biblioteca! '},
            status=status.HTTP_400_BAD_REQUEST)

    for email in owner_email.available_in_libraries.owner_library.all():
        send_email(email.email, 'Nova compra feita!', f'Compra feita na biblioteca {owner_email.available_in_libraries}')


def send_email_of_purchase(books_purchase, type_payment):
    threads = []

    for owner_email in books_purchase.books.all():
        thread = threading.Thread(target=send_email_to_owner, args=(owner_email, type_payment))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
