from haystack import indexes

from accounts.models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_text(self, user):
        return "\n".join([user.username, user.email, user.first_name, user.last_name])
