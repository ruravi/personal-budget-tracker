Prerequisites
==============

1. Create an `.envrc` file at the top-level and these two lines

```
export PLAID_CLIENT_ID=[XXX]
export PLAID_SECRET=[YYY]
```

Replace XXX and YYY with your Plaid credentials.

Running the app
=================
```
cd api
flask run
```

This will start the backend server. You will also need the frontend web app to connect Plaid with your accounts.