from rest_framework import serializers

from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'birth_date', 'bsn']


class MatchSerializer(serializers.Serializer):
    person_1 = PersonSerializer(required=True)
    person_2 = PersonSerializer(required=True)
    match = serializers.SerializerMethodField('_match')

    def _match(self, validated_data):
        person_1 = Person.objects.model(**validated_data['person_1'])
        person_2 = Person.objects.model(**validated_data['person_2'])
        return person_1.match(person_2)
