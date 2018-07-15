#from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate, user_logged_in
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler

class RegistrationSerializer(serializers.Serializer):
    """Serializers registration requests and creates a new user."""

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(required=True,max_length=128,min_length=8,write_only=True)
    confirm_password = serializers.CharField(required=True,max_length=128,min_length=8,write_only=True)
    num_telephone = serializers.CharField(required=True)
    sexe = serializers.CharField(required=False)
    date_naissance = serializers.CharField(required=False)
    adresse_residence = serializers.CharField(required=False)
    ville = serializers.CharField(required=False)
    code_postal = serializers.CharField(required=False)
    pays = serializers.CharField(required=False)

    # The client should not be able to send a token along with a registration
    # request. Making 'token' read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)
    """
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token', 'first_name', 'last_name', 
        'num_telephone', 'sexe', 'date_naissance', 'adresse_residence', 'code_postal', 'ville', 'pays']
    """

    def create(self, validated_data):
        # Use the 'create_user' method we wrote in usermanager to create a new user.
        return User.objects.create_user(**validated_data)

    def validate_email(self, email):
        existing = User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("Someone with that email "
                "address has already registered. Was it you?")

        return email

    def validate_num_telephone(self, num_telephone):
        existing = User.objects.filter(num_telephone=num_telephone).first()
        if existing:
            raise serializers.ValidationError("Someone with that phone "
                "number has already registered. Was it you?")

        return num_telephone

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                "confirm it.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data 



class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The 'validate' method is where we make sure that the current
        # instance of 'LoginSerializer' has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

   
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # 'authenticate' will return 'None'. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

    
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields=('email', 'username', 'password', 'token', 'first_name', 'last_name', 
        'num_telephone', 'sexe', 'date_naissance', 'adresse_residence', 'code_postal', 'ville', 'pays',)

        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(request=self.context['request'], **credentials)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)
                #msg = 'User find but connexion refused by admin.'+jwt_encode_handler(payload)
                #raise serializers.ValidationError(msg)
                #return {
                #    'token': jwt_encode_handler(payload),
                #    'user': user
                #}
                return {
                    'email': user.email,
                    'username': user.username,
                    'token': user.token
                }
            else:
                msg = 'Unable to log in with provided credentials. Connexion refusé.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)