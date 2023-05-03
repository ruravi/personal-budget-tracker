import plaid
from plaid.api import plaid_api
import os

'''
This function returns a Plaid API client.
'''


def get_plaid_client():
    configuration = plaid.Configuration(
        # TODO: Figure out a way to inject a value based on the environment.
        host=plaid.Environment.Sandbox,
        api_key={
            'clientId': os.environ['PLAID_CLIENT_ID'],
            'secret': os.environ['PLAID_SECRET'],
        }
    )

    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)
