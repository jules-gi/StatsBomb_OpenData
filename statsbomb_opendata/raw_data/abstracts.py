from typing import Dict, List, Tuple, cast, Any
import uuid

from django.db import models


class AbstractStatsBombModel(models.Model):

    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=128)
    statsbomb_id: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(unique=True)
    
    class Meta:
        abstract = True
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} object [{self.id}]'
    
    def populate(self, data: Dict[str, Any], attr_key_mapping: List[Tuple[str, List[str]]]) -> None:

        for attr_name, key_list in attr_key_mapping:
            self._populate_attr(data, attr_name, key_list)

    def _populate_attr(self, data: Dict[str, Any], attr_name: str, key_list: List[str]) -> None:

        key = key_list.pop(0)
        if key not in data:
            raise KeyError("Key '{key}' was not found to populate '{obj_name}' object.".format(
                key=key,
                obj_name=self.__class__.__name__
            ))

        if key_list:
            self._populate_attr(
                data=cast(Dict, data.get(key)),
                attr_name=attr_name,
                key_list=key_list
            )
        
        elif not hasattr(self, attr_name):
            raise AttributeError("'{obj_name}' object has no attribute '{attr_name}'.".format(
                attr_name=attr_name,
                obj_name=self.__class__.__name__
            ))
        
        else:
            setattr(self, attr_name, data.get(key))
