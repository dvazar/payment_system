from rest_framework import serializers


class CustomPrimaryKey(serializers.PrimaryKeyRelatedField):
    """"""

    def use_pk_only_optimization(self):
        return False
