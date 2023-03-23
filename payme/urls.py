from django.urls import path

from payme.views import MerchantAPIView, CreateCardView


urlpatterns = [
    path('', CreateCardView.as_view(), name="create_card"),
    path("merchant/", MerchantAPIView.as_view())
]