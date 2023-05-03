Overview
==

This repository contains code to run your own personal monthly spending tracking sheet. We will use a service called Plaid to securely connect to banks and credit card websites to download transactions.



Sub-system layout
=====

There are 3 main sub-systems in this repo.

1. Python Flask-based api server under the `/api` directoryy
2. React JS web app under the `connect-plaid-once` directory
3. streamlit web app user the `/scripts` directory

Instructions
==
You will connect your financial accounts only once. This will download all your transactions and store them in a local database. You will then use the data visualization app to view your spending.

1. Start the backend server using this command `flask run` from the `api` directory
2. Start the frontend web app using this command `npm start` from the `connect-plaid-once` directory
3. Click the 'Connect with Plaid' button and follow the instructions to connect your accounts.
4. Once you have connected your accounts, you can stop the backend server and the frontend web app. You will not need them again. You can now use the data visualization app to view your spending. Check the instance folder for the database file.
5. Start the data visualization app using this command `streamlit run scripts/app.py` from the top-level directory.

## Running the backend server in development/sandbox mode
### Prerequisites

Create an `.envrc` file at the top-level and add these two lines

```
export PLAID_CLIENT_ID=[XXX]
export PLAID_SECRET=[YYY]
```

Replace XXX and YYY with your Plaid API credentials which you can get [here](https://dashboard.plaid.com/team/keys)

These environment variables need to be loaded into your shell before you start the server. You can do this by running `source .envrc` from the top-level directory. Alternately, if you use direnv, you can run `direnv allow` from the top-level directory, which will automatically load the environment variables into your shell when you `cd` into the directory.

```
cd api
pip install -r requirements.txt
flask --debug run
```
