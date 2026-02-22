from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser,FormParser
from .models import User,InstructorProfile,InstructorRequest
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer
from .serializers import InstructorProfileSerializer,InstructorRequestSerializer
from django.utils import timezone

# Create your views here.

# user register

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
        
            return Response({
                "message":"User registered successfully",
                "username":user.username,
                "role":user.role
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


# login user

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# user profile

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # handle file upload

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self,request):
        serializer = UserSerializer(request.user,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Profile updated successfully","data":serializer.data})
        return Response(serializer.errors,status=400)

    
# user activation and deactivation section

class ToggleUserActiveView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self,request,user_id):
        user = get_object_or_404(User,id=user_id)

        user.is_active = not user.is_active
        user.save()

        status_text = "activated" if user.is_active else "deactivated"

        return Response({"message":f"User {status_text} successfully","is_active":user.is_active})
    

# instructor profile

class InstructorProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):  
        # check role     
        if not request.user.is_instructor:
            return Response({"error":"Only instructors allowed"},status=403)  
              
        #get profile
        try:
            profile = request.user.instructor_profile
        except InstructorProfile.DoesNotExist:
            return Response({"error":"Profile not found"}, status=404)
        
        serializer = InstructorProfileSerializer(profile)
        return Response(serializer.data)
    
    def patch(self,request):
        if not request.user.is_instructor:
            return Response({"error":"Only instructors allowed"},status=403)
        try:
            profile =request.user.instructor_profile
        except InstructorProfile.DoesNotExist:
            return Response({"error":"Profile not found"},status=404)  
         
        serializer = InstructorProfileSerializer(profile,data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Profile updated successfully", "data": serializer.data})    
        return Response(serializer.errors, status=400)



# instructor request section

class CreateInstructorRequestView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #check if already requested
        if InstructorRequest.objects.filter(user=request.user).exists():
            return Response({"error":"Request already submitted"},status=400)
        
        serializer = InstructorRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=201)
        
        return Response(serializer.errors, status=400)
    

class InstructorRequestListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        requests = InstructorRequest.objects.all()
        serializer = InstructorRequestSerializer(requests, many=True)
        return Response(serializer.data)


class ReviewInstructorRequestView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            req = InstructorRequest.objects.get(id=pk)
        except InstructorRequest.DoesNotExist:
            return Response({"error":"Not found"}, status=404)
        
        status_value = request.data.get("status")

        if status_value not in ["approved", "rejected"]:
            return Response({"error":"Invalid status"}, status=400)
        
        req.status = status_value
        req.reviewed_by = request.user
        req.reviewed_at = timezone.now()
        req.reason = request.data.get("reason", "")

        req.save()

        return Response({"message": f"Request {status_value}"},status=200)
    