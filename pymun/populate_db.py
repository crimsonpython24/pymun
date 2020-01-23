import os
import django

from . import models
from faker import Faker


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymun.settings')
django.setup()
obj = Faker()


def call(N=10):
    for i in range(N):
        full_name = obj.name()
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]
        full_name_clean = first_name + last_name
        user_obj = models.User.objects.get_or_create(
            username=full_name_clean,
            email=full_name_clean + '@gmail.com',
            first_name=first_name,
            last_name=last_name,
            password='1234567890.'
        )[0]


if __name__ == '__main__':
    print("Filling random data")
    call(10)
    print("Filling done ")
