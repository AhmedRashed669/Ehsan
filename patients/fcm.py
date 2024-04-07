# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from firebase_admin.messaging import Message
# from fcm_django.models import FCMDevice
# from django.db import transaction

# # Your model
# from .models import PatientCase

# @receiver(post_save, sender=PatientCase)
# def send_fcm_message(sender, instance, created, **kwargs):
#     if created:
#             print(created)
#             # only for new instances
#             message_obj = Message(
#                 data={
#                     "body" : "great match!",
#                 },
#             )

# message_obj = Message(
#                 data={
#                     "body" : "great match!",
#                 },
#             )
# device = FCMDevice.objects.all().first()
# device.send_message(message_obj)
from firebase_admin.messaging import Message,WebpushNotification,WebpushConfig
from fcm_django.models import FCMDevice
def send_message():
    try:
        title = "Your notification title"
        body = "Your notification body"
        click_action = "https://google.com"
        notification = WebpushNotification(
            title=title,
            body=body,
        )
        message = Message(
            webpush=WebpushConfig(
                notification=notification,
            )
        )
        device = FCMDevice.objects.all().first()
        response = device.send_message(message)
        print(device.registration_id)
        print(f"Message ID: {response.message_id}")
        print(f"Message was sent successfully: {response.success}")
    except Exception as e:
        print(f"Exception in send_message: {e}")
        # Boom!




