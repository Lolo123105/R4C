from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def send_robot_available_email(sender, instance, created, **kwargs):
    """Send an email when the ordered robot is available."""

    if created:
        orders = Order.objects.filter(robot_serial=instance.serial)

        for order in orders:
            customer_email = order.customer.email

            subject = 'Уведомление о наличии робота.'
            message = ('Здравствуйте! Недавно вы интересовались нашим роботом'
                       f' модели {instance.model}, версии {instance.version}.'
                       ' Этот робот теперь в наличии. Если вам подходит этот '
                       'вариант - пожалуйста, свяжитесь с нами.')

            send_mail(subject,
                      message,
                      'emailbot@R4C.com',
                      [customer_email],
                      fail_silently=False)
