import os
import uuid
from faker import Faker
from shahkar_user.models import UserProfile, Analyzer
from django.utils import timezone
from django.core.management.base import BaseCommand
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
fake = Faker("fa_IR")


class Command(BaseCommand):
    help = "Add 10 million user data and 2 thousand analyzers"

    def handle(self, *args, **options):
        user_profiles = []

        for i in range(10000000):
            user_profiles.append(
                UserProfile(
                    phonenumber=fake.phone_number(),
                    natoinal_id=fake.ssn(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    birthday=fake.date_of_birth(),
                    address=fake.address(),
                )
            )
            if (i + 1) % 1000 == 0:
                logger.info(f"Created {i + 1} user profiles")

        batch_size = 10000
        for i in range(0, len(user_profiles), batch_size):
            logger.info(f"Appending user data {i} - {i + batch_size} to db . . . ")
            UserProfile.objects.bulk_create(user_profiles[i: i + batch_size])
            logger.info(f"Appended batch {i // batch_size + 1} of {len(user_profiles) // batch_size}")

        analyzer_data = []
        for i in range(2000):
            analyzer_data.append(Analyzer(analyzer_id=uuid.uuid4(), name=fake.word()))
            if (i + 1) % 100 == 0:  
                logger.info(f"Created {i + 1} analyzer data")

        # Bulk create analyzers
        Analyzer.objects.bulk_create(analyzer_data)
        logger.info(f"Appended all analyzer data: {len(analyzer_data)} records")
