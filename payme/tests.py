from django.test import TestCase
from payme.cards.subscribe_cards import PaymeSubscribeCards
from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts
from django.conf import settings


class SubscribeTestCase(TestCase):
    def setUp(self):
        client = PaymeSubscribeCards(
            base_url="https://checkout.test.paycom.uz/api/", 
            paycom_id=settings.PAYCOM_ID
        )
        return client


    def test_create_card(self):
        client = self.setUp()
        resp = client._cards_create(
            number="8600495473316478",
            expire="0399",
            save=True,
        )
        self.assertEqual(resp['result']['card']['number'], '860049******6478')
        self.assertEqual(resp['result']['card']['expire'], '03/99')
        self.assertEqual(resp['result']['card']['recurrent'], True)
        self.assertEqual(resp['result']['card']['verify'], False)

    def test_cards_get_verify_code(self):
        client = self.setUp()
        resp = client._card_get_verify_code(
            token="641be73c890565aa4e37c066_5e5av6CVB0hyGrb9bJsSog3KqorcgrzAOwce5Fc5dPj8tncC0k4rDdY7fWdNAZ9YsdaKoJShUi3EGNxA86MbQ1Jvq5evWvqUfdtZ5U3EMz3dgEM1QKqkhgEVyegQNgJPE3FQGu9HdWj9oYeqJKuEe6SJHoRX6xw95yJ9HEGb7Vo207OESWMJJESZirWSOQ8Gs3GrQ7tFVQ24Y1YAcimdfy4p5qDIjxKJxc2ikBAR8HTiMhd8RTOXPPAcb0g0siaqHiQbbHCedqy2I6eup5HV0mNea80xPxp9Iwz6V5VANSSx0nJSFnQPIDGW7FDRN5OApIFgM8j0i4fKs4XGSskhJJXxwdZMKjcGDoxBs9hc190g6H9WgGR6RWeMJBWW6erwwXkFwv"
        )
        self.assertEqual(resp['result']['sent'], True)
        self.assertEqual(resp['result']['phone'], "99890*****91")

    def test_cards_verify(self):
        client = self.setUp()
        resp = client._cards_verify(
            verify_code="666666",
            token="641be73c890565aa4e37c066_5e5av6CVB0hyGrb9bJsSog3KqorcgrzAOwce5Fc5dPj8tncC0k4rDdY7fWdNAZ9YsdaKoJShUi3EGNxA86MbQ1Jvq5evWvqUfdtZ5U3EMz3dgEM1QKqkhgEVyegQNgJPE3FQGu9HdWj9oYeqJKuEe6SJHoRX6xw95yJ9HEGb7Vo207OESWMJJESZirWSOQ8Gs3GrQ7tFVQ24Y1YAcimdfy4p5qDIjxKJxc2ikBAR8HTiMhd8RTOXPPAcb0g0siaqHiQbbHCedqy2I6eup5HV0mNea80xPxp9Iwz6V5VANSSx0nJSFnQPIDGW7FDRN5OApIFgM8j0i4fKs4XGSskhJJXxwdZMKjcGDoxBs9hc190g6H9WgGR6RWeMJBWW6erwwXkFwv"
        )
        self.assertEqual(resp['result']['card']['number'], '860049******6478')
        self.assertEqual(resp['result']['card']['expire'], '03/99')
        self.assertEqual(resp['result']['card']['token'], '641be73c890565aa4e37c066_5e5av6CVB0hyGrb9bJsSog3KqorcgrzAOwce5Fc5dPj8tncC0k4rDdY7fWdNAZ9YsdaKoJShUi3EGNxA86MbQ1Jvq5evWvqUfdtZ5U3EMz3dgEM1QKqkhgEVyegQNgJPE3FQGu9HdWj9oYeqJKuEe6SJHoRX6xw95yJ9HEGb7Vo207OESWMJJESZirWSOQ8Gs3GrQ7tFVQ24Y1YAcimdfy4p5qDIjxKJxc2ikBAR8HTiMhd8RTOXPPAcb0g0siaqHiQbbHCedqy2I6eup5HV0mNea80xPxp9Iwz6V5VANSSx0nJSFnQPIDGW7FDRN5OApIFgM8j0i4fKs4XGSskhJJXxwdZMKjcGDoxBs9hc190g6H9WgGR6RWeMJBWW6erwwXkFwv')
        self.assertEqual(resp['result']['card']['recurrent'], True)
        self.assertEqual(resp['result']['card']['verify'], True)

    def test_card_check(self):
        client = self.setUp()
        resp = client._cards_check(
            token="641be73c890565aa4e37c066_5e5av6CVB0hyGrb9bJsSog3KqorcgrzAOwce5Fc5dPj8tncC0k4rDdY7fWdNAZ9YsdaKoJShUi3EGNxA86MbQ1Jvq5evWvqUfdtZ5U3EMz3dgEM1QKqkhgEVyegQNgJPE3FQGu9HdWj9oYeqJKuEe6SJHoRX6xw95yJ9HEGb7Vo207OESWMJJESZirWSOQ8Gs3GrQ7tFVQ24Y1YAcimdfy4p5qDIjxKJxc2ikBAR8HTiMhd8RTOXPPAcb0g0siaqHiQbbHCedqy2I6eup5HV0mNea80xPxp9Iwz6V5VANSSx0nJSFnQPIDGW7FDRN5OApIFgM8j0i4fKs4XGSskhJJXxwdZMKjcGDoxBs9hc190g6H9WgGR6RWeMJBWW6erwwXkFwv"
        )
        self.assertEqual(resp['result']['card']['number'], '860049******6478')
        self.assertEqual(resp['result']['card']['expire'], '03/99')
        self.assertEqual(resp['result']['card']['token'], '641be73c890565aa4e37c066_5e5av6CVB0hyGrb9bJsSog3KqorcgrzAOwce5Fc5dPj8tncC0k4rDdY7fWdNAZ9YsdaKoJShUi3EGNxA86MbQ1Jvq5evWvqUfdtZ5U3EMz3dgEM1QKqkhgEVyegQNgJPE3FQGu9HdWj9oYeqJKuEe6SJHoRX6xw95yJ9HEGb7Vo207OESWMJJESZirWSOQ8Gs3GrQ7tFVQ24Y1YAcimdfy4p5qDIjxKJxc2ikBAR8HTiMhd8RTOXPPAcb0g0siaqHiQbbHCedqy2I6eup5HV0mNea80xPxp9Iwz6V5VANSSx0nJSFnQPIDGW7FDRN5OApIFgM8j0i4fKs4XGSskhJJXxwdZMKjcGDoxBs9hc190g6H9WgGR6RWeMJBWW6erwwXkFwv')
        self.assertEqual(resp['result']['card']['recurrent'], True)
        self.assertEqual(resp['result']['card']['verify'], True)

    def test_card_remove(self):
        client = self.setUp()
        resp = client._cards_remove(
            token="641be73c890565aa4e37c066_5e5av6CVB0hyGrb9bJsSog3KqorcgrzAOwce5Fc5dPj8tncC0k4rDdY7fWdNAZ9YsdaKoJShUi3EGNxA86MbQ1Jvq5evWvqUfdtZ5U3EMz3dgEM1QKqkhgEVyegQNgJPE3FQGu9HdWj9oYeqJKuEe6SJHoRX6xw95yJ9HEGb7Vo207OESWMJJESZirWSOQ8Gs3GrQ7tFVQ24Y1YAcimdfy4p5qDIjxKJxc2ikBAR8HTiMhd8RTOXPPAcb0g0siaqHiQbbHCedqy2I6eup5HV0mNea80xPxp9Iwz6V5VANSSx0nJSFnQPIDGW7FDRN5OApIFgM8j0i4fKs4XGSskhJJXxwdZMKjcGDoxBs9hc190g6H9WgGR6RWeMJBWW6erwwXkFwv"
        )
        self.assertEqual(resp['result']['success'], True)


class SubscribeReceiptsTestCase(TestCase):
    def setUp(self):
        client = PaymeSubscribeReceipts(
            base_url="https://checkout.test.paycom.uz/api/", 
            paycom_id=settings.PAYCOM_ID,
            paycom_key=settings.PAYCOM_KEY
        )
        return client
    
    def test_receipts_create(self):
        client = self.setUp()
        resp = client._receipts_create(
            amount=1000000,
            order_id=1
        )
        print(resp)
