import os
import uuid
from faker import Faker
from .models import UserProfile, Analyzer
from django.utils import timezone

fake = Faker("fa_IR")



user_profiles = [
    UserProfile(
        phonenumber=fake.phone_number(),
        natoinal_id=fake.ssn(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        birthday=fake.date_of_birth(),
        address=fake.address()
    )
    for _ in range(10000000)
]

batch_size = 10000  # اندازه دسته
for i in range(0, len(user_profiles), batch_size):
    UserProfile.objects.bulk_create(user_profiles[i:i + batch_size])


for _ in range(2000):
    Analyzer.objects.create(analyzer_id=uuid.uuid4(), name=fake.word())
