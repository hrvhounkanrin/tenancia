import logging

from rest_framework import serializers

from customuser.models import User
from customuser.models import UserProfile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('title', 'address', 'country', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ Create function based on  the validated_data args """
        profile_data = validated_data.pop('profile')
        logging.debug(f'**Profile  data information', f'{profile_data}')
        password = validated_data.pop('password')
        user = User(**validated_data)
        logging.debug(f'User is', f'{user}')
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('dob', profile.dob)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()

        return instance
