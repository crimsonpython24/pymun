# You have no friends.

from models import User
from faker import Faker

fake = Faker(['en_US', 'es_ES', 'fr_FR', 'zh_TW'])

x = int(input('How many user objects to generate?'))
for i in range(x):
    first_name = fake.first_name()
    last_name = fake.last_name()
    name = (first_name + last_name).lower()

    user = User.objects.create_user(username=name,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=name+'@gmail.com',
                                    password='12345678900.'
                                    )
