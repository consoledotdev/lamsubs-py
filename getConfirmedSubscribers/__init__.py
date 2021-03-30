# Copyright 2021, Console Ltd https://console.dev
# SPDX-License-Identifier: AGPL-3.0-or-later

# System
import json
import logging

# Third party
import azure.functions as func
import mailchimp_marketing as MailchimpMarketing

from mailchimp_marketing.api_client import ApiClientError

# Config
import app_config


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            'api_key': app_config.MAILCHIMP_API_KEY,
            'server': 'us7'
        })

        # Get Confirmed segment info
        # https://mailchimp.com/developer/marketing/api/list-segments/get-segment-info/
        # https://us7.admin.mailchimp.com/lists/segments?id=518946
        segmentConfirmedStats = client.lists.get_segment(
            app_config.MAILCHIMP_LIST_ID, '3577267')
        confirmedSubscribers = str(segmentConfirmedStats['member_count'])

    except ApiClientError as error:
        logging.error(f'Mailchimp Error: {error.text}')
        jsonResponse = json.dumps({
            'frames': [{
                'icon': 'i619',
                'text': 'Mailchimp Error'
            }]
        })

        return func.HttpResponse(jsonResponse, mimetype='application/json')

    # The total number of subscribers in the list
    # Includes confirmed and unconfirmed
    jsonResponse = json.dumps({
        'frames': [{
            'icon': 'i29438',
            'text': confirmedSubscribers
        }]
    })

    return func.HttpResponse(jsonResponse, mimetype='application/json')
