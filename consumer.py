import pika
from models import Contact
from connect import connect

def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        # Тут міг би бути код для реальної відправки email
        print(f"Email sent to {contact.email}")
        contact.message_sent = True
        contact.save()

def send_sms(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        # Тут міг би бути код для реальної відправки SMS
        print(f"SMS sent to {contact.phone}")
        contact.message_sent = True
        contact.save()

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')
    channel.queue_declare(queue='sms_queue')

    def callback(ch, method, properties, body):
        contact_id = body.decode('utf-8')
        if method.routing_key == 'email_queue':
            print(f"Received email task for {contact_id}")
            send_email(contact_id)
        elif method.routing_key == 'sms_queue':
            print(f"Received SMS task for {contact_id}")
            send_sms(contact_id)

    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()
