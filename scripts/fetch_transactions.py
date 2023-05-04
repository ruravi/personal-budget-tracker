from os.path import dirname, abspath, join
import sys
import argparse
import datetime

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)

from api.app import Transactions, UserToken, app, db
from api.get_plaid_client import get_plaid_client
from api.plaid_helper import retrieve_transactions


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


def fetch_transaction(from_date: datetime.date):
    with app.app_context():
        first_user = UserToken.query.first()
        access_token = first_user.access_token

        plaid_client = get_plaid_client()
        transactions = retrieve_transactions(
            plaid_client, access_token, start_date=from_date)
        write_transactions_to_db(transactions)


if __name__ == "__main__":
    # Extract command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_date',
                        type=str,
                        default=datetime.date.today().strftime('%Y-%m-%d'),
                        help='From date in YYYY-MM-DD format')

    args = parser.parse_args()
    from_date = datetime.date.fromisoformat(args.start_date)
    fetch_transaction(from_date)
