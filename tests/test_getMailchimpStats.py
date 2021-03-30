# Copyright 2021, Console Ltd https://console.dev
# SPDX-License-Identifier: AGPL-3.0-or-later

# System
import os
import unittest
import unittest.mock

# Project
from getMailchimpStats import main

# Config
import app_config


class TestGetStats(unittest.TestCase):

    # Tests production call
    # Should call Mailchimp API, construct the Basecamp message, then post it
    @unittest.mock.patch('requests.post')
    @unittest.mock.patch(
        'mailchimp_marketing.api.lists_api.ListsApi.get_segment')
    @unittest.mock.patch('mailchimp_marketing.api.lists_api.ListsApi.get_list')
    def testProduction(
            self,
            mock_mailchimp_get_list,
            mock_mailchimp_get_segment,
            requests_post):
        # Force into production mode
        # We're mocking requests so it won't actually post to Basecamp
        os.environ['PRODUCTION'] = 'true'

        # Set test values
        totalSubscribers = 1000
        confirmedSubscribers = 500
        unconfirmedSubscribers = 500

        # Set up Mailchimp responses
        mock_mailchimp_get_list.return_value = {
            'stats': {
                'member_count': totalSubscribers
            }
        }

        mock_mailchimp_get_segment.return_value = {
            'member_count': confirmedSubscribers
        }

        # Call the function
        # Passing false sets past_due to false
        # https://github.com/Azure/azure-functions-python-worker/issues/737
        main(False)

        # Check basic calls to Mailchimp
        mock_mailchimp_get_list.assert_called_once()
        mock_mailchimp_get_segment.assert_any_call(
            app_config.MAILCHIMP_LIST_ID, '3577267')
        mock_mailchimp_get_segment.assert_any_call(
            app_config.MAILCHIMP_LIST_ID, '3577271')

        # Construct message we expect will be sent to Basecamp
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

        requests_post.assert_called_once_with(
            app_config.CAMPFIRE_ROOM,
            json={'content': content}
        )

    # Test non production called
    # Should do the same as above, but not post to Basecamp
    @unittest.mock.patch('requests.post')
    @unittest.mock.patch(
        'mailchimp_marketing.api.lists_api.ListsApi.get_segment')
    @unittest.mock.patch('mailchimp_marketing.api.lists_api.ListsApi.get_list')
    def testNotProduction(
            self,
            mock_mailchimp_get_list,
            mock_mailchimp_get_segment,
            requests_post):

        # Set test values
        totalSubscribers = 1000
        confirmedSubscribers = 500

        # Set up Mailchimp responses
        mock_mailchimp_get_list.return_value = {
            'stats': {
                'member_count': totalSubscribers
            }
        }

        mock_mailchimp_get_segment.return_value = {
            'member_count': confirmedSubscribers
        }

        # Call the function
        # Passing false sets past_due to false
        # https://github.com/Azure/azure-functions-python-worker/issues/737
        main(False)

        # Check basic calls to Mailchimp
        mock_mailchimp_get_list.assert_called_once()
        mock_mailchimp_get_segment.assert_any_call(
            app_config.MAILCHIMP_LIST_ID, '3577267')
        mock_mailchimp_get_segment.assert_any_call(
            app_config.MAILCHIMP_LIST_ID, '3577271')

        requests_post.assert_not_called()
