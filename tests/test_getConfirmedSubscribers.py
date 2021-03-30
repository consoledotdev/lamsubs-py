# Copyright 2021, Console Ltd https://console.dev
# SPDX-License-Identifier: AGPL-3.0-or-later

# System
import json
import unittest
import unittest.mock

# Third party
import azure.functions as func

# Project
from getConfirmedSubscribers import main

# Config
import app_config


class TestGetStats(unittest.TestCase):

    # Tests production call
    # Should call Mailchimp API, construct the Basecamp message, then post it
    @unittest.mock.patch(
        'mailchimp_marketing.api.lists_api.ListsApi.get_segment')
    def testProduction(
            self,
            mock_mailchimp_get_segment):

        # Set test values
        confirmedSubscribers = 500

        # Set up Mailchimp responses
        mock_mailchimp_get_segment.return_value = {
            'member_count': confirmedSubscribers
        }

        # Construct a mock HTTP request
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/getConfirmedSubscribers')

        # Call the function
        resp = main(req)

        jsonResponse = json.dumps({
            'frames': [{
                'icon': 'i29438',
                'text': str(confirmedSubscribers)
            }]
        })

        # Check the output
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.get_body(),
            jsonResponse.encode('ascii'),
        )
        # Check basic calls to Mailchimp
        mock_mailchimp_get_segment.assert_called_once_with(
            app_config.MAILCHIMP_LIST_ID, '3577267')
