from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from apps.courses.models import Course
from apps.enrollments.models import Enrollment

# Create your views here.

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    #user can only see their orders
    def get_queryset(self):
        if self.request.user.is_staff:#admin see all orders
            return Order.objects.all().order_by("-created_at")
        return Order.objects.filter(user=self.request.user).order_by("-created_at")
    

    # create order
    def create(self, request):
        course_id = request.data.get("course")

        if not course_id:
            return Response({"error":"course field required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Course.objects.get(id=course_id)
            
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
        #check already enrolled
        already_enrolled=Enrollment.objects.filter(user=request.user,course=course).exists()
        
        if already_enrolled:
            return Response({"error":"You are already enrolled in this course"},status=status.HTTP_400_BAD_REQUEST)
        
        # free course - enroll directly
        if course.is_free:
            Enrollment.objects.get_or_create(user=request.user, course=course)
            return Response({"message": "Enrolled in free course"})
        
        #check existing pending order
        pending_order=Order.objects.filter(user=request.user,course=course,status="PENDING").first()

        if pending_order:
            serializer=self.get_serializer(pending_order)
            return Response(serializer.data)
        
        #create new order
        order = Order.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            status="PENDING"
        )
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    '''
    # simulate payment success
    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        order = self.get_object()

        if order.status == "PAID":
            return Response({"message": "Already paid"})

        payment_id = request.data.get("payment_id")

        if not payment_id:
            return Response({"error":"payment_id required"},status=status.HTTP_400_BAD_REQUEST)
        
        order.payment_id = payment_id
        order.status = "PAID"
        order.save()

        # create enrollment
        Enrollment.objects.get_or_create(
            user=order.user,
            course=order.course
        )
        return Response({"message": "Payment successful & enrolled"})
    
    '''

    #order history
    @action(detail=False,methods=["get"])
    def history(self,request):
        orders=Order.objects.filter(user=request.user,status="PAID").order_by("-created_at")
        serializer=self.get_serializer(orders,many=True)
        return Response(serializer.data)
    
    #cancel order
    @action(detail=True,methods=["post"])
    def cancel(self,request,pk=None):
        order=self.get_object()
        if order.status != "PENDING":
            return Response({"error":"Only pending orders can be cancelled"})
        order.status="CANCELLED"
        order.save()
        return Response({"message":"Order Cancelled"})
    