from flask import Flask, jsonify, Response, jsonify, request
from os import environ
from bunq.sdk.client import Pagination
from bunq.sdk.context import ApiContext
from bunq.sdk.context import ApiEnvironmentType
from bunq.sdk.context import BunqContext
from bunq.sdk.model.generated import endpoint
from json import dumps

if "SECRET" not in environ:
    print("SECRET not specified. Exiting.")
    exit(0)

app = Flask(__name__)

CONTEXT_FILE = "bunq-production.conf"

api_context = ApiContext.restore(CONTEXT_FILE)
api_context.ensure_session_active()
api_context.save(CONTEXT_FILE)
BunqContext.load_api_context(api_context)

def get_all_monetary_account_active():
    pagination = Pagination()
    pagination.count = 25

    all_monetary_account_bank = endpoint.MonetaryAccountBank.list(pagination.url_params_count_only).value
    all_monetary_account_bank_active = []

    for monetary_account_bank in all_monetary_account_bank:
        if monetary_account_bank.status == "ACTIVE":
            all_monetary_account_bank_active.append(monetary_account_bank)

    return all_monetary_account_bank_active

def check_cookie():
    app.logger.warning("SECRET = " + environ["SECRET"])
    app.logger.warning("secret = " + request.cookies.get("secret"))
    return request.cookies.get("secret") == environ["SECRET"]

@app.route("/get_balances", methods=["GET"])
def get_balances():
    if not check_cookie():
        return Response("go away", mimetype="text/plain")

    data = {}
    for account in get_all_monetary_account_active():
        data[account.description] = account.balance.value

    return Response(dumps(data), mimetype="application/json")

if __name__ == "__main__":
    app.run(debug=("DEBUG" in environ), port=(int(environ["PORT"]) if "PORT" in environ else 5000), host=(environ["IP"] if "IP" in environ else "127.0.0.1"))