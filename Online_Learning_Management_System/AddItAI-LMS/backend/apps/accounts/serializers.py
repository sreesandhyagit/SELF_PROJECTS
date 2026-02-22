from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,InstructorRequest,InstructorProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True) # not a db field
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    # def validate_email(self, value):
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("Email already exists")
    #     return value

    def validate(self,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password do not match")
        return data

    def create(self,validated_data):
        validated_data.pop('confirm_password') # remove it before saving

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError("Username and password are required")
        
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("Account is deactivated")
        
        # generate JWT tokens

        refresh = RefreshToken.for_user(user)

        return{
            "id": user.id,
            "username":user.username,
            "email":user.email,
            "role":user.role,
            "is_instructor_approved":user.is_instructor_approved,
            "access":str(refresh.access_token),
            "refresh":str(refresh)
        }


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ['id','username','email','bio','profile_image']
        read_only_fields = ['id']
        

class InstructorProfileSerializer(serializers.ModelSerializer):
    level = serializers.ReadOnlyField()
    class Meta:
        model = InstructorProfile
        fields = "__all__"
        read_only_fields = ["user","rating","total_students","total_course","is_verified"]

class InstructorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorRequest
        fields = '__all__'
        read_only_fields = ['user','status','submitted_at', 'reviewed_at', 'reviewed_by']



        
        