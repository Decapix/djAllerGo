
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
    """
    Handles the sending of a verification riddle to the user's phone number.

    A random riddle is selected from the database and associated with a generated temporary token.
    The riddle question and token are sent to the user's phone number. The token and associated riddle 
    are then stored in the database for later verification.

    Example Request:
    POST /send-verification-code/
    {
        "phone_number": "+1234567890"
    }
    """
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
            
            # renvoyer le token et les 3 réponses
            return Response({"message": "Verification code sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    """
    Verifies the user's answer to the riddle sent to their phone number.

    This view checks if the submitted answer for the riddle is correct and if the provided token is valid.
    If the verification is successful, the view either logs in an existing user or creates a new one.
    It then generates and returns a JWT for the authenticated user.

    Example Request:
    POST /verify-code/
    {
        "phone_number": "+1234567890",
        "verification_word": "answer_to_riddle",
        "token": "temporary_token_received"
    }
    """
    def post(self, request, *args, **kwargs):
        # Deserialize and validate the incoming data
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data
            phone_number = serializer.validated_data['phone_number']
            submitted_answer = serializer.validated_data['verification_word']
            token = serializer.validated_data['token']

            try:
                return self._extracted_from_post_(token, submitted_answer, phone_number)
            except RiddleToken.DoesNotExist:
                # Handle the case where the token does not exist
                return Response({"message": "Invalid token."}, status=status.HTTP_404_NOT_FOUND)

        # Return errors if the data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO Rename this here and in `post`
    def _extracted_from_post_(self, token, submitted_answer, phone_number):
        # Retrieve the riddle token from the database
        riddle_token = RiddleToken.objects.get(token=token)

        # Check if the token is valid
        if not riddle_token.is_valid():
            return Response({"message": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the submitted answer is correct
        if riddle_token.riddle.correct_answer.lower() != submitted_answer.lower():
            return Response({"message": "Incorrect answer."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si l'utilisateur existe déjà
        user = User.objects.filter(phone_number=phone_number).first()
        if user:
            return self._extracted_from_post_26(
                user,
                riddle_token,
                "A user with this phone number already exists. You have been logged in.",
            )
        # Create a new user with the provided phone number
        user = User.objects.create_user(phone_number=phone_number)

        return self._extracted_from_post_26(
            user, riddle_token, "Phone number verified successfully."
        )

    # TODO Rename this here and in `post`
    def _extracted_from_post_26(self, user, riddle_token, arg2):
        # Générer un JWT pour l'utilisateur existant
        refresh = RefreshToken.for_user(user)
        jwt_token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        # Supprimez le token Riddle après la vérification
        riddle_token.delete()

                    # Renvoyer la réponse avec le JWT
        return Response({"message": arg2, "jwt": jwt_token}, status=status.HTTP_200_OK)

    
# login 

class LoginView(APIView):
    """
    Handles user login using phone number or email and password.

    Validates the user credentials and, upon successful authentication, generates
    a JWT (including access and refresh tokens) which is returned to the user.

    Example Request:
    POST /login/
    {
        "login": "user@example.com or +1234567890",
        "password": "user_password"
    }
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "jwt": {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                "message": "You have been logged in."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
# other

class AddAdditionalInformationView(APIView):
    """
    Allows authenticated users to add or update additional information to their profile.

    This view requires user authentication and accepts additional information like
    email and password. On successful update, a confirmation message is sent back.

    Example Request:
    POST /add-additional-information/
    Headers: Authorization: Bearer <access_token>
    {
        "email": "newemail@example.com",
        "password": "newpassword"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = AddAdditionalInformationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User information updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BulkContactUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        contacts_data = request.data.get('contacts', [])

        for contact_data in contacts_data:
            serializer = ContactSerializer(data=contact_data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            phone_number = serializer.validated_data['phone_number']

            # Vérifier si le contact existe déjà
            contact, created = Contact.objects.get_or_create(phone_number=phone_number, defaults=serializer.validated_data)

            # Relier le contact à l'utilisateur actuel
            user.contacts.add(contact)
        return Response({"message": "Contacts uploaded successfully."}, status=status.HTTP_201_CREATED)