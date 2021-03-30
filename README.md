# Mailchimp App for LaMetric (Python)

An HTTP endpoint for polling Mailchimp subscriber numbers for an [LaMetric
Time](https://lametric.com/en-US/time/overview) device. Designed to run on
Azure Functions as an HTTP endpoint.

## Methods

* **[`getConfirmedSubscribers`](getConfirmedSubscribers/)**: returns the confirmed
  subscribers from Mailchimp.
  * Type: [HTTP trigger
    function](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger?tabs=python).

## Deployment

Uses [`main.bicep`](main.bicep) to define the Azure resources.

### Automatic

Uses [Azure
ARM](https://github.com/marketplace/actions/deploy-azure-resource-manager-arm-template)
and [Login](https://github.com/marketplace/actions/azure-login) GitHub actions
to deploy.

`AZURE_CREDENTIALS` created as per [the service principal
instructions](https://github.com/marketplace/actions/azure-login#configure-deployment-credentials):

```zsh
az ad sp create-for-rbac --name "lamsubs-py - GitHub" --sdk-auth --role contributor \
    --scopes /subscriptions/244fa449-6833-417a-9b8e-be5a66bdf344/resourceGroups/lamsubs-py
```

`AZURE_FUNCTIONAPP_PUBLISH_PROFILE` set up [according to the docs](https://github.com/marketplace/actions/azure-functions-action#using-publish-profile-as-deployment-credential-recommended).

### Manual

[Install Bicep](https://github.com/Azure/bicep/blob/main/docs/installing.md)
which is used to compile the ARM template that manages the Azure resources.

```zsh
# Assumes bc-totorobot-py resource group exists
bicep build ./main.bicep # generates main.json
az login
az deployment group create -f ./main.json -g lamsubs-py
func azure functionapp publish lamsubs-py
```

## Local development

### Setup

Install the [Azure Functions
SDK](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
and [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli),
then:

1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip3 install -r requirements.txt`

### Local dev server

```zsh
# Set these values appropriately
export MAILCHIMP_API_KEY=""
export MAILCHIMP_LIST_ID=""
func host start
```

### Trigger timer function

```zsh
curl -i -X POST -H "Content-Type:application/json" -d "{}" http://localhost:7071/admin/functions/getConfirmedSubscribers
```

### Tests

```zsh
python3 -m pytest
```

Coverage reports:

```zsh
python3 -m coverage run -m pytest
python3 -m coverage report --omit '.venv/*'
```

## Environment variables

These are substituted in as part of the deploy process and set in the GitHub
repo secrets:

* `AZURE_CREDENTIALS` discussed above.
* `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` discussed above.
* `MAILCHIMP_API_KEY` from [Mailchimp
  settings](https://us7.admin.mailchimp.com/account/api/) to be able to connect
  to the API.
  `MAILCHIMP_LIST_ID` from [Audience settings](https://us7.admin.mailchimp.com/lists/settings/defaults?id=518946).
