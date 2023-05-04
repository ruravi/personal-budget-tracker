from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)

from api.plaid_helper import retrieve_transactions
from api.get_plaid_client import get_plaid_client
from api.app import Transactions, UserToken, app, db



def write_transactions_to_db(transactions: list):
    with app.app_context():
        for transaction in transactions:
            row = Transactions(
                user_id='ruravi',
                amount=transaction['amount'],
                category=transaction['category'][0],
                date=transaction['date'],
                description=transaction['name'],
                transaction_id=transaction['transaction_id'],
                account_id=transaction['account_id']
            )
            db.session.add(row)
        db.session.commit()


def fetch_transaction():
    with app.app_context():
        first_user = UserToken.query.first()
        access_token = first_user.access_token

        plaid_client = get_plaid_client()
        transactions = retrieve_transactions(plaid_client, access_token)
        write_transactions_to_db(transactions)


if __name__ == "__main__":
    fetch_transaction()
