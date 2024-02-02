from rest_framework import serializers

from core.choices import TaskStatuses


class TaskChoiceField(serializers.ChoiceField):
    """
    Кастомное поле ChoiceField.

    Возвращает label наименования из TaskStatuses при получении объекта.
    Принимает label наименование и преобразовывает
    в value для сохранения в базу.
    """

    def to_representation(self, value: str):
        return TaskStatuses(value).label

    def to_internal_value(self, data: str):
        for value, label in TaskStatuses.choices:
            if data == label:
                return value
        return TaskStatuses.DRAFT
