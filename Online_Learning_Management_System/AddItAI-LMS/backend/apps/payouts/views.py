from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from apps.payouts.models import Payout
from django.shortcuts import get_object_or_404
from apps.notifications.services import create_notification

# Create your views here.

class RequestPayoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user

        if user.role!="INSTRUCTOR":
            return Response({"error":"Only instructors allowed"},status=403)
        
        amount=request.data.get("amount")
        if not amount or float(amount) <= 0:
            return Response({"error":"Invalid amount"},status=400)
        
        payout=Payout.objects.create(instructor=user,amount=amount)

        return Response({
            "message":"Withdrawal request submitted",
            "payout_id":payout.id
        })


class InstructorPayoutHistoryView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        payouts=Payout.objects.filter(
            instructor=request.user
        ).order_by("-created_at")
        
        if request.user.role != "INSTRUCTOR":
            return Response({"error":"Only instructor allowed"},status=403)

        data=payouts.values("id","amount","status","created_at")
        return Response(data)
    

class PendingPayoutsView(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        payouts=Payout.objects.filter(status="PENDING")
        data=payouts.values("id","instructor__email","amount","created_at")
        return Response(data)
    
class ApprovePayoutView(APIView):
    permission_classes=[IsAdminUser]

    def post(self,request,id):
        payout=get_object_or_404(Payout,id=id)
        payout.status="APPROVED"
        payout.save()
        create_notification(
            user=payout.instructor,
            title="Payout Approved",
            message=f"{payout.amount} approved",
            ntype="PAYOUT"
        )
        return Response({"message":"Payment approved"})
    
class MarkPayoutPaidView(APIView):
    permission_classes=[IsAdminUser]
    def post(self,request,id):
        payout=get_object_or_404(Payout,id=id)
        payout.status="PAID"
        payout.save()
        return Response({"message":"Payout completed"})
    
    
