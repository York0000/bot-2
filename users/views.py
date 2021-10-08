from rest_framework.generics import CreateAPIView

from users.serializers import TelegramRegistrationSerializer


class TelegramRegistrationView(CreateAPIView):
    serializer_class = TelegramRegistrationSerializer
