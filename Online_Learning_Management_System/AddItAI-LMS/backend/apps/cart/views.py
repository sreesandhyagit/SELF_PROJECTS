from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer
from apps.courses.models import Course

# Create your views here.

class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related("course")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Add course to cart
    @action(detail=False, methods=["post"])
    def add_to_cart(self, request):
        course_id = request.data.get("course")
        if not course_id:
            return Response({"error": "course_id required"},status=400)
        course = Course.objects.filter(id=course_id).first()
        if not course:
            return Response({"error": "Course not found"},status=404)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            course=course
        )
        if not created:
            return Response({"message": "Course already in cart"})
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data,status=201)

    # Remove item
    @action(detail=True, methods=["delete"])
    def remove(self, request, pk=None):
        item = self.get_object()
        item.delete()
        return Response({"message": "Removed from cart"})

    # Clear cart
    @action(detail=False, methods=["delete"])
    def clear(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared"})

    # Cart summary
    @action(detail=False, methods=["get"])
    def summary(self, request):
        items = Cart.objects.filter(user=request.user).select_related("course")
        total_price = sum(item.course.price for item in items)
        return Response({"total_items": items.count(),"total_price": total_price})