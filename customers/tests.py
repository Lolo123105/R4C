import datetime as dt

from django.test import TestCase
from django.core import mail


from customers.models import Customer
from customers.views import send_robot_available_email
from orders.models import Order
from robots.models import Robot


class SendEmailTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = Customer.objects.create(email='test@email.com')
        cls.robot = Robot.objects.create(serial='TE-ST',
                                         model='TE',
                                         version='ST',
                                         created=dt.datetime.now())
        cls.order = Order.objects.create(customer=cls.customer,
                                         robot_serial=cls.robot.serial)

    def test_send_robot_available_email(self):
        send_robot_available_email(sender=None,
                                   instance=self.robot,
                                   created=True)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to[0], 'test@email.com',
                         ('Проверь, что получатель получает',
                          ' письмо на свою почту'))
        self.assertEqual(email.subject, 'Уведомление о наличии робота.',
                         'Проверь, что тема письма работает правильно.')
        self.assertIn('модели TE, версии ST',
                      email.body, ('Проверь, что модель и версия',
                                   ' робота отправляются верно.'))
