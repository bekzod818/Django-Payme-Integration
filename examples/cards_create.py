from pprint import pprint

from payme.cards.subscribe_cards import PaymeSubscribeCards


client = PaymeSubscribeCards(
    base_url="https://checkout.test.paycom.uz/api/",
    paycom_id="5e730e8e0b852a417aa49ceb"
)

resp = client._cards_create(
    number="8600495473316478",
    expire="0399",
    save=True,
)

pprint(resp)