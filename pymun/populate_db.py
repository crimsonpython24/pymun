import os
import django
import random

from accounts.models import User
from faker import Faker


obj = Faker()


def call(N, first):
    for i in range(N):
        if first is None:
            full_name = obj.name()
            first_name = full_name.split()[0]
            last_name = full_name.split()[1]
            full_name_clean = (first_name + last_name).lower()
        else:
            first_name = first
            last_name = obj.name().split()[1]
            full_name_clean = (first_name + last_name).lower()

        user_obj = User.objects.get_or_create(
            username=full_name_clean.lower() + str(random.randrange(0, 10000)),
            email=full_name_clean + '@gmail.com',
            first_name=first_name,
            last_name=last_name,
            password='1234567890.'
        )[0]


if __name__ == '__main__':
    "Starting club population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymun.settings')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'pymun.settings'

    django.setup()

    print("Filling random data")
    call(int(input("Input a number: ")), input("first name if any: "))
    print("Filling done ")
