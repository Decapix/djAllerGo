from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Contact
from django.core.exceptions import ValidationError

User = get_user_model()


# registration

class SendVerificationCodeSerializer(serializers.Serializer):
    """we receive the phone number
    
    receive :
    - phone number
    """
    phone_number = serializers.CharField(validators=[User.phone_regex])

    def validate_phone_number(self, value):
        # Vous pouvez ajouter des validations supplémentaires ici si nécessaire
        return value


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_word = serializers.CharField()  # La réponse à la devinette
    token = serializers.CharField()  # Ajoutez ce champ pour le token
    


# other

class AddAdditionalInformationSerializer(serializers.ModelSerializer):
    """add info :
    - mail
    - password
    """
    class Meta:
        model = User
        fields = ['email', 'password', 'other_field']  # Ajoutez les champs nécessaires, comme Google ou Apple IDs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_password(self, value):
        return make_password(value)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        # Mettez à jour les autres champs ici
        instance.save()
        return instance
    
    
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'phone_number', 'email', 'owner')

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)
