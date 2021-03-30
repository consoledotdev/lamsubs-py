# Copyright 2021, Console Ltd https://console.dev
# SPDX-License-Identifier: AGPL-3.0-or-later

# System
import logging
import os

# Third party
import azure.functions as func
import mailchimp_marketing as MailchimpMarketing
import requests

from mailchimp_marketing.api_client import ApiClientError

# Config
import app_config


def main(getMailchimpStats: func.TimerRequest) -> None:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            'api_key': app_config.MAILCHIMP_API_KEY,
            'server': 'us7'
        })

        # Get list info
        # https://mailchimp.com/developer/api/marketing/lists/get-list-info/
        listStats = client.lists.get_list(app_config.MAILCHIMP_LIST_ID)
        totalSubscribers = int(listStats['stats']['member_count'])

        # Get Confirmed segment info
        # https://mailchimp.com/developer/marketing/api/list-segments/get-segment-info/
        # https://us7.admin.mailchimp.com/lists/segments?id=518946
        segmentConfirmedStats = client.lists.get_segment(
            app_config.MAILCHIMP_LIST_ID, '3577267')
        confirmedSubscribers = int(segmentConfirmedStats['member_count'])

        segmentUnconfirmedStats = client.lists.get_segment(
            app_config.MAILCHIMP_LIST_ID, '3577271')
        unconfirmedSubscribers = int(segmentUnconfirmedStats['member_count'])

    except ApiClientError as error:
        logging.error(f'Mailchimp Error: {error.text}')
        return

    # Construct message to send to Basecamp
    content = '<strong>Mailchimp Stats (py)</strong><ul>'

    # The total number of subscribers in the list
    # Includes confirmed and unconfirmed
    content += '<li><strong>Confirmed subscribers:</strong> '
    content += f'{confirmedSubscribers:,}</li>'

    content += '<li><strong>Unconfirmed members:</strong> '
    content += f'{unconfirmedSubscribers:,}</li>'

    content += '<li><strong>Total list members:</strong> '
    content += f'{totalSubscribers:,}</li>'

    content += '</ul>'

    if 'PRODUCTION' in os.environ:
        # Post to Campfire
        r = requests.post(app_config.CAMPFIRE_ROOM, json={'content': content})

        if r.status_code != 200 or r.status_code != 201:
            logging.error(f'Basecamp error: {r.status_code} {r.text}')
    else:
        logging.info('Not in production mode, would have posted:')
        logging.info(content)
