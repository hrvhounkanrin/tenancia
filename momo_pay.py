import requests
import json
import uuid
import random

subscription_key_user_create = '83745e545dce48d6aec29bfa1e1ed716'
subscription_key_trans_create = '83745e545dce48d6aec29bfa1e1ed716'
unique_ref = str(uuid.uuid4())
base_url = "https://sandbox.momodeveloper.mtn.com"
url = f'{base_url}/v1_0/apiuser'
body = {"providerCallbackHost": "string"}
headers = {
    'Content-type': 'application/json',
    'X-Reference-Id': unique_ref,
    'Ocp-Apim-Subscription-Key': subscription_key_user_create
}
# create api user key
r = requests.post(url, data=json.dumps(body), headers=headers)

if r.status_code == 201:
    print("User API Created")
    url = f'{base_url}/v1_0/apiuser/{unique_ref}/apikey'
    body = {"providerCallbackHost": "string"}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key_user_create}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    # print(r.content)
    user_key_tojson = r.json()
    # print(user_key_tojson)
    apikey = user_key_tojson["apiKey"]
    print(f"apikey created: {apikey}")

    print('ask for transaction token start')
    url = f'{base_url}/collection/token'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key_trans_create}
    r = requests.post(url, data=json.dumps(body), auth=(unique_ref, apikey))
    print('r.status_code: ', r.status_code)
    if r.status_code == 200:
        json_content = r.json()
        access_token = json_content['access_token']
        token_type = json_content['token_type']
        expires_in = json_content['expires_in']
        print('access_token: ', access_token)
        print('token_type: ', token_type)
        print('expires_in:', expires_in)

        montant = 500
        devise = 'XOF'
        id = '12345678'
        payer_phone = '22996120534'
        payer_message = "Paiement facture loyer n° 8787868545"
        payee_message = "Reglement facture loyer n°89797998"
        body = {
            "amount": montant,
            "currency": devise,
            "externalId": id,
            "payer": {"partyIdType": "MSISDN", "partyId": payer_message},
            "payerMessage": payer_message,
            "payeeNote": payee_message
        }
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'X-Reference-Id': unique_ref,
            'X-Target-Environment': 'sandbox',
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': subscription_key_trans_create
        }

        url = f'{base_url}/collection/v1_0/requesttopay'
        r = requests.post(url, data=json.dumps(body).encode('ascii'), headers=headers)
        print(r)
        print('end of transaction')
