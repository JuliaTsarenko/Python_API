from imaplib import IMAP4_SSL
import base64
import email
import time


def getting_email_code():
    connection = IMAP4_SSL(host='imap.gmail.com', port=993)
    connection.login(user='viktor.yahoda', password='anycash15')
    while 1:
        connection.select('INBOX')
        result, data = connection.uid('search', None, '(FROM "AnyMoney")', '(UNSEEN)')
        if bool(data[0]):
            latest_email_uid = data[0].split()[-1]
            result, data = connection.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            for msg in msg.walk():
                if msg.get_content_maintype() == 'text':
                    letter = msg.get_payload().encode('utf-8')
                    print(base64.decodebytes(letter).decode('utf-8'))
                    return base64.decodebytes(letter).decode('utf-8')
            break
        else:
            time.sleep(2)
            print('Waiting for admin email...')
            continue


def equal_list(_list, elem):
    while 1:
        for el in _list:
            if elem == el:
                pass
            else:
                return False
        return True


def bl(numb):
    """ Number for admin  requests. """
    return int(numb * 1000000000)


def orig(numb):
    """ Number from admin response. """
    return numb / 1000000000


def pers(numb):
    """ Percent number for admin requests. """
    return int(numb * 10000000)


if __name__ == '__main__':
    print(pers(15))
