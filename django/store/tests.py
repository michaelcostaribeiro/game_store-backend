from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from . import models
from datetime import date

#--------------------------------
# Game creation tests
#--------------------------------


class GamePlatformTests(APITestCase):

    def setUp(self):
        self.ps = models.Platform.objects.create(platform_name="PlayStation")

        self.game = models.Game.objects.create(
            title="Clair Obscur: Expedition 33",
            description='Conduza os membros da Expedição 33 em uma missão para destruir a Artífice para que ela nunca mais possa pintar a morte. Explore um mundo inspirado na Belle Époque da França e enfrente inimigos únicos neste RPG em turnos com mecânicas em tempo real.',
            price="199",
            release_date=date(2025, 10, 7),
            quantity_sold=0
        )
        self.game.platforms.add(self.ps)

    def test_games_by_platform_happy_path(self):
        url = '/api/games_by_platform/PlayStation/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()


        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('games', response_data)

        games_list = response_data['games']
        self.assertEqual(len(games_list), 1)
        self.assertEqual(games_list[0]['title'], "Clair Obscur: Expedition 33")

    def test_games_by_platform_not_found_edge_case(self):

        url = '/api/games_by_platform/Dreamcast/'

        response = self.client.get(url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        games_list = response_data['games']
        self.assertEqual(len(games_list), 0)
        self.assertEqual(games_list, [])

#--------------------------------
# Login/Auth tests
#--------------------------------


class AuthAndCartTests(APITestCase):

  def test_register_validation_failures(self):
    url = reverse('register')

    invalid_payload = {
        'username': '',
        'email': 'not-a-valid-email',
        'password': '',
    }

    response = self.client.post(url, invalid_payload, format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    response_data = response.json()
    self.assertIn('email', response_data)

  def test_register_token_issuance_success(self):
    url = reverse('register')

    valid_payload = {
        'username': 'gamer123',
        'email': 'gamer@example.com',
        'password': 'StrongPassword123!',
    }

    response = self.client.post(url, valid_payload, format='json')
    response_data = response.json()


    self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    self.assertIn('access', response_data)
    self.assertIn('refresh', response_data)

  def test_manage_cart_items_unauthenticated_returns_401(self):
    url = reverse('add_item_to_cart')


    response = self.client.post(
        url, {'game': 1, 'quantity': 1}, format='json'
    )

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_cart_unauthenticated_returns_400_or_401(self):
    url = reverse('getCart')

    response = self.client.get(url)

    self.assertIn(
        response.status_code,
        [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED],
    )


#--------------------------------
# Search Tests
#--------------------------------

class GameSearchTests(APITestCase):

    def setUp(self):
        self.game = models.Game.objects.create(
            title="The Legend of Zelda: Breath of the Wild",
            description="Step into a world of discovery, exploration, and adventure.",
            price="299.00",
            release_date=date(2017, 3, 3),
            quantity_sold=0  # Don't forget this!
        )

    def test_game_search_case_insensitive(self):
        url_upper = reverse('gameSearch', kwargs={'query': 'ZELDA'})
        response_upper = self.client.get(url_upper)

        self.assertEqual(response_upper.status_code, status.HTTP_200_OK)

        data_upper = response_upper.json()
        self.assertIn('games', data_upper)
        self.assertEqual(len(data_upper['games']), 1)
        self.assertEqual(data_upper['games'][0]['title'], "The Legend of Zelda: Breath of the Wild")

        url_lower = reverse('gameSearch', kwargs={'query': 'zelda'})
        response_lower = self.client.get(url_lower)

        self.assertEqual(response_lower.status_code, status.HTTP_200_OK)

        data_lower = response_lower.json()
        self.assertEqual(len(data_lower['games']), 1)
        self.assertEqual(data_lower['games'][0]['title'], "The Legend of Zelda: Breath of the Wild")

    def test_game_search_not_found_miss(self):
        url = reverse('gameSearch', kwargs={'query': 'Half-Life 3'})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



#--------------------------------
# Payment tests
#--------------------------------
class MercadoPagoTests(APITestCase):

    @patch('store.views.mercadopago.SDK')
    def test_create_preference_success(self, mock_sdk):
        mock_sdk_instance = mock_sdk.return_value
        mock_sdk_instance.preference.return_value.create.return_value = {
            'status': 201,
            'response': {
                'id': 'PREF_123456789_MOCK',
                'init_point': 'https://www.mercadopago.com/checkout/v1/redirect?pref_id=PREF_123456789_MOCK'
            }
        }

        url = reverse('criar_preferencia')
        payload = {
            'items': [
                {
                    'title': 'Clair Obscur: Expedition 33',
                    'quantity': 1,
                    'price': 199.00
                }
            ]
        }

        response = self.client.post(url, payload, format='json')

        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        response_data = response.json()
        self.assertTrue('id' in response_data or 'preference_id' in response_data)

    @patch('store.views.mercadopago.SDK')
    def test_create_preference_failure_returns_400(self, mock_sdk):
        mock_sdk_instance = mock_sdk.return_value
        mock_sdk_instance.preference.return_value.create.return_value = {
            'status': 400,
            'response': {'message': 'Invalid payload items'}
        }

        url = reverse('criar_preferencia')
        invalid_payload = {'items': []}

        response = self.client.post(url, invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('store.views.mercadopago.SDK')
    def test_webhook_payment_created_simulation(self, mock_sdk):
        mock_sdk_instance = mock_sdk.return_value
        mock_sdk_instance.payment.return_value.get.return_value = {
            'status': 200,
            'response': {'id': 123456789, 'status': 'approved'}
        }

        url = reverse('mp_webhook')

        fake_webhook_payload = {
            'action': 'payment.created',
            'type': 'payment',
            'data': {'id': '123456789'}
        }

        response = self.client.post(url, fake_webhook_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)