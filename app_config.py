import logging
import os
import sys

if 'PRODUCTION' in os.environ:
    logging.info('config PROD')
else:
    logging.info('config TEST')

# Get configs from environment variables
if 'CAMPFIRE_ROOM' in os.environ:
    CAMPFIRE_ROOM = os.environ['CAMPFIRE_ROOM']
else:
    logging.error('envar CAMPFIRE_ROOM not set')
    sys.exit(1)

if 'MAILCHIMP_API_KEY' in os.environ:
    MAILCHIMP_API_KEY = os.environ['MAILCHIMP_API_KEY']
else:
    logging.error('envar MAILCHIMP_API_KEY not set')
    sys.exit(1)

if 'MAILCHIMP_LIST_ID' in os.environ:
    MAILCHIMP_LIST_ID = os.environ['MAILCHIMP_LIST_ID']
else:
    logging.error('envar MAILCHIMP_LIST_ID not set')
    sys.exit(1)
