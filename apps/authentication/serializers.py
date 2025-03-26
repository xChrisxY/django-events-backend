from rest_framework import serializers
from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'email']

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password]
    )

    password2 = serializers.CharField(
        write_only = True,
        required = True
    )

    class Meta:
        
        model = User 
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'first_name' : {'required': False},
            'last_name' : {'required': False},
            'email' : {'required': True}
        }

    def validate(self, attrs):
        # personalizamos la validación

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden"
            })

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                "email": "Un usuario con este correo electrónico ya existe."
            })
            
        return attrs

    def create(self, validated_data):
        # método personalizado para crear un usuario
        
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        if 'first_name' in validated_data:
            user.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            user.last_name = validated_data['last_name']

        user.save()
        return user

        
class ChangePasswordSerializer(serializers.ModelSerializer):
    
    old_password = serializers.CharField(
        write_only = True,
        required = True
    )

    new_password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password]
    )

    confirm_new_password = serializers.CharField(
        write_only = True,
        required = True
    )

    def validate(self, attrs):
        # validaciones personalizadas para el cambio de contraseña

        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({
                "new_password": "Las nuevas contraseñas no coinciden."
            })

        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({
                "old_password" : "La contraseña actual es incorrecta."
            })

        return attrs

    def update(self, instance, validated_data):
        # Método para actualizar la nueva contraseña
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance

        
class UserPasswordResetSerializer(serializers.Serializer):
    # serializador para solicitar restablecimiento de contraseña

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "No existe ningún usuario con ese correo electrónico."    
            )

        return value