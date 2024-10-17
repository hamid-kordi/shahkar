from celery import shared_task
from .models import User


@shared_task
def find_user_by_phone(phone_number):
    try:
        user = User.objects.get(phonenumber=phone_number)
        return {
            "national_id": user.natoinal_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "birth_date": user.birthday.strftime("%Y-%m-%d"),
            "address": user.address,
            "message": "Success",
        }
    except User.DoesNotExist:
        return {"message": "User not found"}
