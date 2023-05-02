from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import os
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.account_filter import AccountFilter
from plaid.model.account_subtype import AccountSubtype
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
import json


class handler(BaseHTTPRequestHandler):

    # set up function.
    def __init__(self, *args, **kwargs):

        # Available environments are
        # 'Production'
        # 'Development'
        # 'Sandbox'
        configuration = plaid.Configuration(
            # TODO: Figure out a way to inject a value based on the environment.
            host=plaid.Environment.Sandbox,
            api_key={
                'clientId': os.environ['PLAID_CLIENT_ID'],
                'secret': os.environ['PLAID_SECRET'],
            }
        )

        api_client = plaid.ApiClient(configuration)
        self.plaid_client = plaid_api.PlaidApi(api_client)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # TODO: Extract user id from the JWT token.

        # Send a request to the Plaid API to create a link token.
        # https://plaid.com/docs/#create-link-token
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        plaid_response = self.plaid_client.link_token_create(
            LinkTokenCreateRequest(
                products=[Products('transactions')],
                client_name='Rukmani Budget App',
                country_codes=[CountryCode('US')],
                language='en',
                user=LinkTokenCreateRequestUser(
                    client_user_id='user_good',
                ),
                # account_filters=AccountFilter(
                #     credit=[AccountSubtype('LINE_OF_CREDIT')],
                # ),
            )
        )

        self.wfile.write(json.dumps({
            "link_token": plaid_response.link_token,
        }).encode())
        return


# Use this for local testing
# if __name__ == "__main__":
#     httpd = HTTPServer(('localhost', 8080), handler)
#     try:
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         print('Shutting down server')
