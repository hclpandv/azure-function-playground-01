export RANDOM_ID="$(openssl rand -hex 3)"
export RESOURCE_GROUP_NAME="rg-module-test-01"
export REGION="westeurope"
export AZURE_FUNCTION_NAME="functionappdemo$RANDOM_ID"
export AZURE_FUNCTION_RBAC_ROLE="Reader"
export STORAGE_NAME="functionappdemo$RANDOM_ID"

# Get the subscription ID
export SUBSCRIPTION_ID=$(az account show --query "id" -o tsv)

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
    --runtime powershell \
    --runtime-version 7.4 \
    --functions-version 4 \
    --name $AZURE_FUNCTION_NAME \
    --os-type windows \
    --storage-account $STORAGE_NAME \
    --assign-identity '[system]'

# Get the Function App's Managed Identity Principal ID
PRINCIPAL_ID=$(az functionapp identity show \
    --name $AZURE_FUNCTION_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --query "principalId" -o tsv)

# Get the current user's Object ID
USER_ID=$(az ad signed-in-user show --query "id" -o tsv)

# Check if the user has Owner or User Access Administrator role before assigning Contributor role
USER_ROLE=$(az role assignment list --assignee $USER_ID --scope /subscriptions/$SUBSCRIPTION_ID --query "[].roleDefinitionName" -o tsv)

if [[ ! "$USER_ROLE" =~ "Owner" ]] && [[ ! "$USER_ROLE" =~ "User Access Administrator" ]]; then
    echo "❌ ERROR: You do not have permission to assign roles."
    echo "➡️  Please ask an Azure admin to assign the 'Owner' or 'User Access Administrator' role to your account."
    echo "➡️  Alternatively, they can manually assign the Contributor role using the following command:"
    echo ""
    echo "    az role assignment create --assignee $PRINCIPAL_ID --role 'Contributor' --scope /subscriptions/$SUBSCRIPTION_ID"
    echo ""
    exit 1
fi

# Assign Contributor Role at the Subscription Level
az role assignment create \
    --assignee $PRINCIPAL_ID \
    --role $AZURE_FUNCTION_RBAC_ROLE \
    --scope /subscriptions/$SUBSCRIPTION_ID

echo "✅ Role assignment successful! The Function App now has $AZURE_FUNCTION_RBAC_ROLE permissions."
