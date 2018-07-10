from os.path import isfile
import argparse

from bunq.sdk.context import ApiContext
from bunq.sdk.context import ApiEnvironmentType

parser = argparse.ArgumentParser("Generate a Bunq API context.")
parser.add_argument("api key", metavar="KEY", nargs=1, help="An API key as acquired from the Bunq app.")
parser.add_argument("device name", metavar="NAME", nargs=1, help="A device name.")
parser.add_argument("output filename", metavar="FILE", nargs=1, help="A destination for the context.")

args = parser.parse_args()

ApiContext(ApiEnvironmentType.PRODUCTION, args["api_key"], args["device_name"]).save(args["save_where"])

api_context = ApiContext.restore(args["save_where"])
api_context.ensure_session_active()
api_context.save()