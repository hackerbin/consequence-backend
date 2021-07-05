import json

import requests
from config.settings import TRUELAYER_AUTH_BASE, TRUELAYER_API_BASE, TRUELAYER_RESPONSE_TYPE, TRUELAYER_CLIENT_ID, \
    TRUELAYER_CLIENT_SECRET, \
    TRUELAYER_SCOPE, \
    TRUELAYER_REDIRECT_URI, TRUELAYER_PROVIDERS


class TrueLayer:
    access_token = None

    def get_access_token(self, code):
        url = f"{TRUELAYER_AUTH_BASE}/connect/token"

        payload = f'grant_type=authorization_code&client_id={TRUELAYER_CLIENT_ID}&client_secret={TRUELAYER_CLIENT_SECRET}&redirect_uri={TRUELAYER_REDIRECT_URI}&code={code}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # return response.text
        if response.status_code == 200:
            self.access_token = json.loads(response.text).get('access_token')
            return json.loads(response.text).get('access_token')
        return {}

    def connect(self, code):
        url = f"{TRUELAYER_AUTH_BASE}/connect/token"

        payload = f'grant_type=authorization_code&client_id={TRUELAYER_CLIENT_ID}&client_secret={TRUELAYER_CLIENT_SECRET}&redirect_uri={TRUELAYER_REDIRECT_URI}&code={code}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # return response.text
        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def get_refresh_token(self, refresh_token):
        url = f"{TRUELAYER_AUTH_BASE}/connect/token"

        payload = f'grant_type=refresh_token&client_id={TRUELAYER_CLIENT_ID}&client_secret={TRUELAYER_CLIENT_SECRET}&refresh_token={refresh_token}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def set_access_token(self, access_token):
        self.access_token = access_token
        return

    def retrieve_access_token_metadata(self):
        url = f"{TRUELAYER_API_BASE}/data/v1/me"

        payload = {}
        files = {}
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload, files=files)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def retrieve_identity_information(self):

        url = f"{TRUELAYER_API_BASE}/data/v1/info"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def list_all_bank_accounts(self):
        url = f"{TRUELAYER_API_BASE}/data/v1/accounts"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def retrieve_bank_account(self, account_id):
        url = f"{TRUELAYER_API_BASE}/data/v1/accounts/{account_id}"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def retrieve_bank_account_transactions(self, account_id):
        url = f"{TRUELAYER_API_BASE}/data/v1/accounts/{account_id}/transactions"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def retrieve_bank_account_pending_transactions(self, account_id):
        url = f"{TRUELAYER_API_BASE}/data/v1/accounts/{account_id}/transactions/pending"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def list_all_cards(self):
        url = f"{TRUELAYER_API_BASE}/data/v1/cards"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def retrieve_card(self, account_id):
        url = f"{TRUELAYER_API_BASE}/data/v1/cards/{account_id}"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def retrieve_card_transactions(self, account_id):
        url = f"{TRUELAYER_API_BASE}/data/v1/cards/{account_id}/transactions"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def retrieve_card_pending_transactions(self, account_id):
        url = f"{TRUELAYER_API_BASE}/data/v1/cards/{account_id}/transactions/pending"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        return {}
