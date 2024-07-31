from typing import Any

from django.db.models import Model, PositiveIntegerField
from django.core.exceptions import ObjectDoesNotExist

class OrderField(PositiveIntegerField):
    
    def __init__(self, for_fields: list = None, *args: Any, **kwargs: Any) -> None:
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance: Model, add: bool) -> Any:
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = getattr(last_item, self.attname) + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)