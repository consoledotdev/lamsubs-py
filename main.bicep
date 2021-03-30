//
// Bicep template to create the Azure resources
//
// Build for Bicep 0.2
//
// Based on: https://github.com/Azure/bicep/tree/2d1f43e57ccfbc117e0d6a9709e0b71377e9a83b/docs/examples/101/function-app-create

param campfireRoom string
param mailchimpApiKey string
param mailchimpListId string

param location string = resourceGroup().location

var appName = 'bc-totorobot-py'
param functionRuntime string = 'python'

// remove dashes for storage account name
var storageAccountName = format('{0}', replace(appName, '-', ''))

var appTags = {
  AppName: appName
}

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2019-06-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
    tier: 'Standard'
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    encryption: {
      services: {
        file: {
          keyType: 'Account'
          enabled: true
        }
        blob: {
          keyType: 'Account'
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    accessTier: 'Hot'
  }
  tags: appTags
}

// Blob Services for Storage Account
resource blobServices 'Microsoft.Storage/storageAccounts/blobServices@2019-06-01' = {
  name: '${storageAccount.name}/default'
  properties: {
    cors: {
      corsRules: []
    }
    deleteRetentionPolicy: {
      enabled: true
      days: 7
    }
  }
}

// Workspace & associated App Insights resource
resource workspace 'Microsoft.OperationalInsights/workspaces@2020-08-01' = {
  name: appName
  location: location
  properties: {
    retentionInDays: 7
    sku: {
      name: 'Free'
    }
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02-preview' = {
  name: appName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: workspace.id
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
  tags: appTags
}

// App Service
resource appService 'Microsoft.Web/serverFarms@2020-06-01' = {
  name: appName
  location: location
  kind: 'functionapp'
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
    size: 'Y1'
    family: 'Y'
    capacity: 0
  }
  properties: {
    reserved: true
  }
  tags: appTags
}

// Function App
resource functionApp 'Microsoft.Web/sites@2020-06-01' = {
  name: appName
  location: location
  kind: 'functionapp,linux'
  properties: {
    enabled: true
    hostNameSslStates: [
      {
        name: '${appName}.azurewebsites.net'
        sslState: 'Disabled'
        hostType: 'Standard'
      }
      {
        name: '${appName}.scm.azurewebsites.net'
        sslState: 'Disabled'
        hostType: 'Standard'
      }
    ]
    serverFarmId: appService.id
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${listKeys(storageAccount.id, storageAccount.apiVersion).keys[0].value}'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: 'InstrumentationKey=${appInsights.properties.InstrumentationKey}'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: functionRuntime
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~3'
        }
        {
          name: 'PRODUCTION'
          value: 'true'
        }
        {
          name: 'CAMPFIRE_ROOM'
          value: campfireRoom
        }
        {
          name: 'MAILCHIMP_API_KEY'
          value: mailchimpApiKey
        }
        {
          name: 'MAILCHIMP_LIST_ID'
          value: mailchimpListId
        }
      ]
      linuxFxVersion: 'python|3.8'
    }
    scmSiteAlsoStopped: false
    clientAffinityEnabled: false
    clientCertEnabled: false
    hostNamesDisabled: false
    dailyMemoryTimeQuota: 0
    httpsOnly: true
    redundancyMode: 'None'
  }
  tags: appTags
}

// Function App Binding
resource functionAppBinding 'Microsoft.Web/sites/hostNameBindings@2020-06-01' = {
  name: '${functionApp.name}/${functionApp.name}.azurewebsites.net'
  properties: {
    siteName: functionApp.name
    hostNameType: 'Verified'
  }
}
