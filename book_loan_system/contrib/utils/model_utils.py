class ReprMixin:
    @property
    def repr_attributes(self):
        return ('id',)  # Default attributes for __repr__

    @property
    def str_attributes(self):
        return self.repr_attributes

    def __repr__(self):
        cls_name = self.__class__.__name__
        attributes = self._format_attributes(self.repr_attributes)
        return f"{cls_name}({attributes})"

    def __str__(self):
        attributes = self._format_attributes(self.str_attributes)
        return f"{attributes}"

    def _format_attributes(self, attributes):
        return ", ".join(
            f"{attr}={repr(getattr(self, attr, None))}" for attr in attributes
        )
