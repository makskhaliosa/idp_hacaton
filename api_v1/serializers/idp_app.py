from rest_framework import serializers
from idp_app.models import Department, Task


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'dep_id',
            'dep_name',
            'company_id'
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'task_id',
            'task_name',
            'task_description',
            'task_status',
            'task_start_date',
            'task_end_date_plan',
            'task_end_date_fact',
            'task_note_employee',
            'task_note_cheif',
            'task_note_cheif',
            'task_note_mentor',
            'task_mentor_id'
        )