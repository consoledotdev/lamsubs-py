import logging
import os
import sys

# Get configs from environment variables
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
