from django.urls import path as p
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    p('send_verification_code/', SendVerificationCodeView.as_view(), name='send_verification_code'),
    p('verify_code/', VerifyCodeView.as_view(), name='verify_code'),
    p('add_additional_information/', AddAdditionalInformationView.as_view(), name='add_additional_information'),
    p('login/', LoginView.as_view(), name='user-login'),
    p('upload-contacts/', BulkContactUploadView.as_view(), name='upload-contacts'),
    p('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    p('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

