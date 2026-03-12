from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from apps.orders.models import Order
from apps.enrollments.models import Enrollment
from apps.notifications.services import create_notification

# Create your views here.
class PaymentViewSet(ModelViewSet):
    serializer_class=PaymentSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #start payment
    @action(detail=False,methods=["post"])
    def start_payment(self,request):
        order_id=request.data.get("order_id")

        if not order_id:
            return Response({"error":"order_id required"},status=400)
        
        order=Order.objects.filter(id=order_id,user=request.user).first()
        
        if not order:
            return Response({"error":"Order not found"},status=404)
        
        if order.status != "PENDING":
            return Response({"error":"Payment already processed"})
        
        payment=Payment.objects.create(
            user=request.user,
            order=order,
            amount=order.amount
        )
        return Response({
            "payment_id":payment.id,
            "amount":payment.amount,
            "status":payment.status
        })
    
    #confirm payment (simulate gateway sunccess)
    @action(detail=True,methods=["post"])
    def confirm_payment(self,request,pk=None):

        payment=self.get_object()

        if payment.status == "success":
            return Response({"message":"Payment already completed"})
        
        payment_id=request.data.get("payment_id")

        if not payment_id:
            return Response({"error":"payment_id required"}, status=400)
        
        payment.payment_id=payment_id
        payment.status="success"
        payment.save()

        order=payment.order
        order.status="PAID"
        order.payment_id=payment_id
        order.save()

        #enroll user to courses
        Enrollment.objects.get_or_create(user=request.user,course=order.course)

        create_notification(
            user=request.user,
            title="Payment Successful",
            message=f"Your payment for{order.course.title} was successful",
            ntype="PAYMENT"
        )

        return Response({"message":"Payment successful","order":order.id,"payment_id":payment_id})
    
    #failed payment
    @action(detail=True,methods=["post"])
    def fail_payment(self,request,pk=None):
        payment=self.get_object()
        payment.status="failed"
        payment.save()
        return Response({"message":"Payment failed"})

        
