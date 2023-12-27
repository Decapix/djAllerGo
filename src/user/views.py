
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import random

from .models import *
from .serializers import *
from .extras import *



# registration

class SendVerificationCodeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendVerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            
            # Sélectionnez une devinette aléatoirement
            riddle = random.choice(Riddle.objects.all())
            token = generate_temporary_token()

            # Envoyez la devinette et le token à l'utilisateur
            send_riddle_to_user(phone_number, riddle.question, token)  # Implémentez cette fonction
            
            # Enregistrez le token et l'association avec la devinette
            RiddleToken.objects.create(token=token, riddle=riddle)

            return Response({"message": "Verification code sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request, *args, **kwargs):
        # Deserialize and validate the incoming data
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data
            phone_number = serializer.validated_data['phone_number']
            submitted_answer = serializer.validated_data['verification_word']
            token = serializer.validated_data['token']

            try:
                # Retrieve the riddle token from the database
                riddle_token = RiddleToken.objects.get(token=token)

                # Check if the token is valid
                if not riddle_token.is_valid():
                    return Response({"message": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

                # Check if the submitted answer is correct
                if riddle_token.riddle.correct_answer.lower() != submitted_answer.lower():
                    return Response({"message": "Incorrect answer."}, status=status.HTTP_400_BAD_REQUEST)

                # Check if a user with the same phone number already exists
                if User.objects.filter(phone_number=phone_number).exists():
                    return Response({"message": "A user with this phone number already exists."}, status=status.HTTP_404_NOT_FOUND)

                
                # Create a new user with the provided phone number
                user = User.objects.create_user(phone_number=phone_number)
                
                # Générez un JWT pour l'utilisateur
                refresh = RefreshToken.for_user(user)
                jwt_token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                # Delete the riddle token after successful verification
                riddle_token.delete()
                return Response({"message": "Phone number verified successfully.", "jwt": jwt_token}, status=status.HTTP_200_OK)

            except RiddleToken.DoesNotExist:
                # Handle the case where the token does not exist
                return Response({"message": "Invalid token."}, status=status.HTTP_404_NOT_FOUND)

        # Return errors if the data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    
# other

class AddAdditionalInformationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone_number=request.data.get('phone_number'))
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddAdditionalInformationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User information updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        user = authenticate(request, username=phone_number, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "User successfully logged in."}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    


class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "User successfully logged out."}, status=status.HTTP_200_OK)



class BulkContactUploadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        contacts_data = request.data.get('contacts', [])

        for contact_data in contacts_data:
            serializer = ContactSerializer(data=contact_data)
            if serializer.is_valid():
                # Ici, on lie le contact à l'utilisateur actuellement authentifié
                contact = serializer.save(owner=user)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Contacts uploaded successfully."}, status=status.HTTP_201_CREATED)