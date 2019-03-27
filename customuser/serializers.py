from rest_framework import  serializers
from  .models import User
from django.contrib.auth.validators import UnicodeUsernameValidator

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name','username',
                  'date_joined', 'password')
    extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
    }
