#!/bin/bash

# Set Variables
export SUBSCRIPTION_ID=$(az account show --query "id" -o tsv)
RESOURCE_GROUP="rg-module-test-01"
LOCATION="westeurope"
EVENT_SUBSCRIPTION_NAME="event-subscription-01"
EVENT_TOPIC_NAME="event-topic-01"
FUNCTION_APP_NAME="functionappdemoc85c59"

az eventgrid system-topic create \
  -g $RESOURCE_GROUP \
  --name $EVENT_TOPIC_NAME \
  --location global \
  --topic-type Microsoft.Resources.Subscriptions \
  --source /subscriptions/$SUBSCRIPTION_ID

az eventgrid system-topic event-subscription create \
  --name $EVENT_SUBSCRIPTION_NAME \
  --system-topic-name $EVENT_TOPIC_NAME \
  --resource-group $RESOURCE_GROUP \
  --endpoint "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$FUNCTION_APP_NAME/functions/AutoUpdateAzureTags" \
  --endpoint-type azurefunction \
  --included-event-types "Microsoft.Resources.ResourceWriteSuccess" \
  --advanced-filter data.authorization.action StringContains "Microsoft.Resources/subscriptions/resourceGroups/write" \
  --event-delivery-schema EventGridSchema \
  --max-delivery-attempts 30 \
  --event-ttl 1440 \
  --max-events-per-batch 1 \
  --preferred-batch-size-in-kilobytes 64

