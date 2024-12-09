from django.conf import settings
from django.db import models

from book_loan_system.contrib.utils.model_utils import ReprMixin


class BaseModel(ReprMixin, models.Model):
    class Meta:
        abstract = True

    def to_dict(self):
        """Convert model instance to a dictionary, mostly just for debugging in the console and such """
        return {field.name: getattr(self, field.name) for field in self._meta.get_fields()}
