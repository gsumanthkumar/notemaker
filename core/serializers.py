from rest_framework import serializers
from .models import Notes, NotesVersionHistory

class NoteSerializer(serializers.ModelSerializer):
   class Meta:
      model = Notes
      fields = '__all__'
      extra_kwargs = {
            'shared': {'read_only': True},
            'owner': {'read_only': True}
        }

   def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner_name'] = instance.owner.username

        return representation
   