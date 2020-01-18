from PIL import Image
import os

from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now as timezone_now
from django.contrib.postgres.fields import ArrayField

from utils import models as util_models

# from utils import fields as util_fields


THUMBNAIL_SIZE = getattr(settings, "QUOTES_THUMBNAIL_SIZE", 50)
THUMBNAIL_EXT = getattr(settings, "QUOTES_THUMBNAIL_EXT", None)


def upload_to(instance, filename):
    now = timezone_now()
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    return f"{instance.slug}{now:%Y/%m/%Y%m%d%H%M%S}{ext}"


def get_square_crop_points(image):
    width, height = image.size
    target = width if width > height else height
    upper, lower = get_centering_points(height, target)
    left, right = get_centering_points(width, target)
    return left, upper, right, lower


def get_centering_points(size, target):
    delta = size - target
    start = int(delta) / 2
    end = start + target
    return start, end


# Still to be added: (1) many-to-many field, see book for details
class User(util_models.CreationModificationDateMixin, util_models.UrlMixin, AbstractUser):

    slug = models.SlugField(unique=True)
    avatar = models.ImageField('Avatar', upload_to=upload_to, blank=True, null=True)

    email = models.EmailField(_('email address'), blank=True)
    recovery_email = ArrayField(models.EmailField(_('Recovery Email')), blank=True, null=True)
    contact_email = ArrayField(models.EmailField(_('Contact Email')), blank=True, null=True)

    birthday = models.DateField(_('Birthday'), blank=True, null=True)
    genders = (('male', 'Male'), ('female', 'Female'), ('others', 'Non-Binary'), ('none', 'Undeclarable'))
    gender = models.CharField(_('Gender'), blank=True, choices=genders, max_length=10)

    workplace = models.CharField(_('Workplace'), blank=True, max_length=100)
    college = models.CharField(_('College'), blank=True, max_length=100)

    high_school = models.CharField(_('High School'), blank=True, max_length=100)
    current_city = models.CharField(_('Current City'), blank=True, max_length=100)
    hometown = models.CharField(_('Hometown'), blank=True, max_length=100)

    nickname = models.CharField(_('Nickname'), blank=True, max_length=50)
    biography = models.CharField(_('Biography'), blank=True, max_length=500)
    favorite_quote = models.CharField(_('Favorite Quote'), blank=True, max_length=500)
    # biography = util_fields.MultilingualCharField(_('Biography'), blank=True, max_length=500)
    # favorite_quote = util_fields.MultilingualCharField(_('Favorite Quote'), blank=True, max_length=500)

    def __str__(self):
        assert isinstance(self.username, object)
        return self.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username, allow_unicode=True)
        super().save(*args, **kwargs)
        self.create_thumbnail()
        
    @property
    def get_url_path(self):
        return reverse("profile", kwargs={"slug": self.object.slug})

    def create_thumbnail(self):
        if not self.avatar:
            return False
        picture_path, thumbnail_path = self.get_picture_paths()
        if thumbnail_path and not storage.exists(thumbnail_path):
            try:
                picture_file = storage.open(picture_path, "r")
                image = Image.open(picture_file)
                image = image.crop(get_square_crop_points(image))
                image = image.resize((THUMBNAIL_SIZE, THUMBNAIL_SIZE), Image.ANTIALIAS)
                image.save(thumbnail_path)
            except (IOError, KeyError, UnicodeDecodeError):
                return False
        return True

    def get_thumbnail_picture_url(self):
        url = ""
        self.create_thumbnail()
        picture_path, thumbnail_path = self.get_picture_paths()

        if thumbnail_path:
            url = (storage.url(thumbnail_path)
                   if storage.exists(thumbnail_path) else self.avatar.url)

        return '/static/' + url

    def get_picture_paths(self):
        picture_path = None
        thumb_path = None
    
        if self.avatar:
            picture_path = self.avatar.name
            filename_base, filename_ext = os.path.splitext(picture_path)
            if THUMBNAIL_EXT:
                filename_ext = THUMBNAIL_EXT
            thumb_path = f"{filename_base}_thumbnail{filename_ext}"
    
        return picture_path, thumb_path

    @classmethod
    def itemprop_fields(cls) -> object:
        return ["title", "content"] + super().itemprop_fields()

