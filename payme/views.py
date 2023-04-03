import base64
import binascii

from django.shortcuts import render
from django.conf import settings
from django.views import View
from .forms import CreateCardForm, VerifyCodeForm
from .cards.subscribe_cards import PaymeSubscribeCards

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from payme.utils.logger import logged

from payme.errors.exceptions import MethodNotFound
from payme.errors.exceptions import PermissionDenied
from payme.errors.exceptions import PerformTransactionDoesNotExist

from payme.methods.check_transaction import CheckTransaction
from payme.methods.cancel_transaction import CancelTransaction
from payme.methods.create_transaction import CreateTransaction
from payme.methods.perform_transaction import PerformTransaction
from payme.methods.check_perform_transaction import CheckPerformTransaction


class MerchantAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        password = request.META.get('HTTP_AUTHORIZATION')
        if self.authorize(password):
            incoming_data: dict = request.data
            incoming_method: str = incoming_data.get("method")
            logged_message: str = "Incoming {data}"

            logged(
                logged_message=logged_message.format(
                    method=incoming_method,
                    data=incoming_data
                ),
                logged_type="info"
            )
            try:
                paycom_method = self.get_paycom_method_by_name(
                    incoming_method=incoming_method
                )
            except ValidationError:
                raise MethodNotFound()
            except PerformTransactionDoesNotExist:
                raise PerformTransactionDoesNotExist()

            paycom_method = paycom_method(incoming_data.get("params"))

        return Response(data=paycom_method)

    @staticmethod
    def get_paycom_method_by_name(incoming_method: str) -> object:
        """
        Use this static method to get the paycom method by name.
        :param incoming_method: string -> incoming method name
        """
        available_methods: dict = {
            "CheckTransaction": CheckTransaction,
            "CreateTransaction": CreateTransaction,
            "CancelTransaction": CancelTransaction,
            "PerformTransaction": PerformTransaction,
            "CheckPerformTransaction": CheckPerformTransaction
        }

        try:
            MerchantMethod = available_methods[incoming_method]
        except Exception:
            error_message = "Unavailable method: %s" % incoming_method
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise MethodNotFound(error_message=error_message)

        merchant_method = MerchantMethod()

        return merchant_method

    @staticmethod
    def authorize(password: str) -> None:
        """
        Authorize the Merchant.
        :param password: string -> Merchant authorization password
        """
        is_payme: bool = False
        error_message: str = ""

        if not isinstance(password, str):
            error_message = "Request from an unauthorized source!"
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise PermissionDenied(error_message=error_message)

        password = password.split()[-1]

        try:
            password = base64.b64decode(password).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            error_message = "Error when authorize request to merchant!"
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise PermissionDenied(error_message=error_message)

        merchant_key = password.split(':')[-1]

        if merchant_key == settings.PAYME.get('PAYME_KEY'):
            is_payme = True

        if merchant_key != settings.PAYME.get('PAYME_KEY'):
            logged(
                logged_message="Invalid key in request!",
                logged_type="error"
            )

        if is_payme is False:
            raise PermissionDenied(
                error_message="Unavailable data for unauthorized users!"
            )

        return is_payme
    

class CreateCardView(View):
    def get(self, request):
        form = CreateCardForm()
        return render(request, "payme/create_card.html", {"form": form})
    
    def post(self, request):
        form = CreateCardForm(request.POST)
        if form.is_valid():
            client = PaymeSubscribeCards(
                base_url="https://checkout.test.paycom.uz/api/",
                paycom_id=settings.PAYCOM_ID
            )
            resp = client._cards_create(
                number=form.cleaned_data.get("card_number"),
                expire=f"{form.cleaned_data.get('expires_month')}{form.cleaned_data.get('expires_year')}",
                save=True
            )
            if resp.get("result"):
                token = resp.get("result").get("card").get("token")
                send_code_resp = client._card_get_verify_code(token=token)
                if send_code_resp.get("result"):
                    send_status = send_code_resp.get("result").get("sent")
                    if send_status:
                        form = VerifyCodeForm(request.POST)
                        if form.is_valid():
                            resp = client._cards_verify(
                                verify_code=form.cleaned_data.get("verify_code"),
                                token=token
                            )
                            print(resp)
        return render(request, "payme/create_card.html", {"form": form})
