from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def to_dict(self):
        """Convert model instance to a dictionary, mostly just for debugging in the console and such """
        return {field.name: getattr(self, field.name) for field in self._meta.get_fields()}
