import pika
from mongoengine import connect
from Mongo import password
from faker import Faker
from model import Contact

fake = Faker('uk_UA')
connect(db="web_19", host=f"mongodb+srv://{password.user}:{password.password}@goitlearn.x6ks5fo.mongodb.net/?retryWrites=true&w=majority")
def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')
    channel.queue_declare(queue='sms_queue')

    for _ in range(10000):
        full_name = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()
        preferred_method = fake.random_element(elements=('email', 'sms'))
        contact = Contact(full_name=full_name, email=email, phone_number=phone_number,
                          preferred_method=preferred_method)
        contact.save()
        print(f"Contact {full_name} ({email}) successfully added to database")

        message_body = str(contact.id)
        if preferred_method == 'email':
            channel.basic_publish(exchange='', routing_key='email_queue', body=message_body)
            print(f"Message for contact {full_name} ({email}) has been added to email_queue")
        else:
            channel.basic_publish(exchange='', routing_key='sms_queue', body=message_body)
            print(f"Message for contact {full_name} ({phone_number}) has been added to sms_queue")

    connection.close()


if __name__ == "__main__":
    main()





