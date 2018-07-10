from os.path import isfile
import argparse

from bunq.sdk.context import ApiContext
from bunq.sdk.context import ApiEnvironmentType

parser = argparse.ArgumentParser("Generate a Bunq API context.")
parser.add_argument("api_key", metavar="KEY", help="An API key as acquired from the Bunq app.")
parser.add_argument("device_name", metavar="NAME", help="A device name.")
parser.add_argument("output_filename", metavar="FILE", help="A destination for the context.")

args = parser.parse_args()

ApiContext(ApiEnvironmentType.PRODUCTION, args.api_key, args.device_name).save(args.output_filename)

api_context = ApiContext.restore(args.output_filename)
api_context.ensure_session_active()
api_context.save()
