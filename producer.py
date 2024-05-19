import pika
from models import Contact
from connect import connect
from faker import Faker
from random import choice

fake = Faker()

def create_fake_contacts(n):
    contacts = []
    for _ in range(n):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            notify_by=choice(['sms', 'email']),
            additional_info=fake.text()
        )
        contact.save()
        contacts.append(contact)
    return contacts

def send_to_email_queue(contact_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact_id))
    connection.close()

def send_to_sms_queue(contact_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sms_queue')
    channel.basic_publish(exchange='', routing_key='sms_queue', body=str(contact_id))
    connection.close()

def main():
    contacts = create_fake_contacts(20)  # Генерація 10 фейкових контактів
    for contact in contacts:
        if contact.notify_by == 'sms':
            send_to_sms_queue(contact.id)
        else:
            send_to_email_queue(contact.id)


if __name__ == "__main__":
    main()
