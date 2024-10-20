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
    help = "Add  2 thousand analyzers"

    def handle(self, *args, **options):

        analyzer_data = []
        for i in range(2000):
            analyzer_data.append(
                UserAnalyzer(analyzer_id=uuid.uuid4(), name=fake.word())
            )
            if (i + 1) % 100 == 0:
                logger.info(f"Created {i + 1} analyzer data")

        # Bulk create analyzers
        UserAnalyzer.objects.bulk_create(analyzer_data)
        logger.info(f"Appended all analyzer data: {len(analyzer_data)} records")
