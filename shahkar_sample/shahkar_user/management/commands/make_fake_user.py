import os
import uuid
from faker import Faker
from shahkar_user.models import UserProfile, UserAnalyzer
from django.utils import timezone
from django.core.management.base import BaseCommand
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
fake = Faker("fa_IR")


class Command(BaseCommand):
    help = "Add 100 thousand user data "

    def handle(self, *args, **options):
        user_profiles = []

        for i in range(3000000):
            user_profiles.append(
                UserProfile(
                    phonenumber=fake.phone_number()[:13],
                    natoinal_id=fake.ssn()[:10],
                    first_name=fake.first_name()[:50],
                    last_name=fake.last_name()[:50],
                    birthday=fake.date_of_birth(),
                    address=fake.address()[:255],
                )
            )
            if (i + 1) % 1000 == 0:
                logger.info(f"Created {i + 1} user profiles")

        batch_size = 10000
        for i in range(0, len(user_profiles), batch_size):
            logger.info(f"Appending user data {i} - {i + batch_size} to db . . . ")
            UserProfile.objects.bulk_create(user_profiles[i : i + batch_size])
            logger.info(
                f"Appended batch {i // batch_size + 1} of {len(user_profiles) // batch_size}"
            )
