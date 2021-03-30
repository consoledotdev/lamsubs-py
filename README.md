# Basecamp Totorobot (Python)

Azure functions to send various stats into Basecamp Campfire as
[Totorobot](https://3.basecamp.com/4477159/buckets/19633762/chats/3207405868/integrations/33437320/edit).

## Methods

* **[`getMailchimpStats`](getMailchimpStats/)**: posts the latest stats from
  Mailchimp.
  * Type: [Timer trigger
    function](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python).

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
az ad sp create-for-rbac --name "bc-totorobot-py - GitHub" --sdk-auth --role contributor \
    --scopes /subscriptions/244fa449-6833-417a-9b8e-be5a66bdf344/resourceGroups/bc-totorobot-py
```

`AZURE_FUNCTIONAPP_PUBLISH_PROFILE` set up [according to the docs](https://github.com/marketplace/actions/azure-functions-action#using-publish-profile-as-deployment-credential-recommended).

### Manual

[Install Bicep](https://github.com/Azure/bicep/blob/main/docs/installing.md)
which is used to compile the ARM template that manages the Azure resources.

```zsh
# Assumes bc-totorobot-py resource group exists
bicep build ./main.bicep # generates main.json
az login
az deployment group create -f ./main.json -g bc-totorobot-py
func azure functionapp publish bc-totorobot-py
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

Azurite ([VS Code
extension](https://marketplace.visualstudio.com/items?itemName=Azurite.azurite)
or [NPM](https://www.npmjs.com/package/azurite)) is required for running the
Azure Functions server locally.

```zsh
# Set these values appropriately
export CAMPFIRE_ROOM=""
export MAILCHIMP_API_KEY=""
export MAILCHIMP_LIST_ID="" 
func host start
```

### Trigger timer function

```zsh
curl -i -X POST -H "Content-Type:application/json" -d "{}" http://localhost:7071/admin/functions/getMailchimpStats
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
* `CAMPFIRE_ROOM` from the [Campfire Bot Settings](https://3.basecamp.com/4477159/buckets/20714437/chats/3442253085/integrations).
* `MAILCHIMP_API_KEY` from [Mailchimp
  settings](https://us7.admin.mailchimp.com/account/api/) to be able to connect
  to the API.
  `MAILCHIMP_LIST_ID` from [Audience settings](https://us7.admin.mailchimp.com/lists/settings/defaults?id=518946).
* `PRODUCTION` should be set to any value.
