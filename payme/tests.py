from django.test import TestCase
from payme.cards.subscribe_cards import PaymeSubscribeCards
from django.conf import settings


class SubscribeTestCase(TestCase):
    def setUp(self):
        client = PaymeSubscribeCards(
            base_url="https://checkout.test.paycom.uz/api/", 
            paycom_id="5e730e8e0b852a417aa49ceb"
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
