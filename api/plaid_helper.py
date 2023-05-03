import plaid
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.account_filter import AccountFilter
from plaid.model.account_subtype import AccountSubtype
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.api import plaid_api
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest


def create_link_token(
        plaid_client: plaid_api.PlaidApi,
        user_id: str = 'user_good') -> str:
    try:
        plaid_response = plaid_client.link_token_create(
            LinkTokenCreateRequest(
                products=[Products('transactions')],
                client_name='Rukmani Budget App',
                country_codes=[CountryCode('US')],
                language='en',
                user=LinkTokenCreateRequestUser(
                    client_user_id=user_id,
                ),
                # account_filters=AccountFilter(
                #     credit=[AccountSubtype('LINE_OF_CREDIT')],
                # ),
            )
        )
        return plaid_response.link_token
    except plaid.ApiException as e:
        raise e


def exchange_public_token(
        plaid_client: plaid_api.PlaidApi,
        public_token: str) -> str:
    try:
        exchange_response = plaid_client.item_public_token_exchange(
            ItemPublicTokenExchangeRequest(
                public_token=public_token,
            )
        )
        return exchange_response.access_token
    except plaid.ApiException as e:
        raise e


def retrieve_transactions(
        plaid_client: plaid_api.PlaidApi,
        access_token: str) -> list:
    request = TransactionsSyncRequest(
        access_token=access_token,
    )
    response = plaid_client.transactions_sync(request)
    transactions = response['added']

    # the transactions in the response are paginated, so make multiple calls while incrementing the cursor to
    # retrieve all transactions
    while (response['has_more']):
        request = TransactionsSyncRequest(
            access_token=access_token,
            cursor=response['next_cursor']
        )
        response = plaid_client.transactions_sync(request)
        transactions += response['added']

    return transactions
