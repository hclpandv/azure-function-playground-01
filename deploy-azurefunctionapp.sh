export RANDOM_ID="$(openssl rand -hex 3)"
export RESOURCE_GROUP_NAME="rg-module-test-01"
export REGION="westeurope"
export AZURE_FUNCTION_NAME="functionappdemo$RANDOM_ID"
export STORAGE_NAME="functionappdemo$RANDOM_ID"

# rg
az group create --name $RESOURCE_GROUP_NAME --location $REGION

# storage account
az storage account create \
    --name $STORAGE_NAME \
    --location $REGION \
    --resource-group $RESOURCE_GROUP_NAME \
    --sku Standard_LRS

# azure function
az functionapp create \
    --resource-group $RESOURCE_GROUP_NAME \
    --consumption-plan-location $REGION \
    --runtime python \
    --runtime-version 3.12 \
    --functions-version 4 \
    --name $AZURE_FUNCTION_NAME \
    --os-type linux \
    --storage-account $STORAGE_NAME