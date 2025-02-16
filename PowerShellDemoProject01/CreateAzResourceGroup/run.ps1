<#
  This Azure function will communicate with Azure Resource Manager via Az modules. 
  hence ENSURE REQUIRED RBAC FOR THE FUNCTION APP IDENTITY  
#>

# Input bindings are passed in via param block.
param($Timer)

# Get the current universal time in the default string format.
$currentUTCtime = (Get-Date).ToUniversalTime()

# The 'IsPastDue' property is 'true' when the current function invocation is later than scheduled.
if ($Timer.IsPastDue) {
    Write-Host "PowerShell timer is running late!"
}

# Perform Azure Operations
$rgs = Get-AzResourceGroup

Write-Output "Total number of resource groups found in the subscription $((Get-AzSubscription).name) is: $($rgs.count)"

foreach ($rg in $rgs) {
    Write-Output "Resourcegroup found: $($rg.ResourceGroupName) in Azure Region of $($rg.Location)"
}

# Write an information log with the current time.
Write-Output "PowerShell timer trigger function ran! TIME: $currentUTCtime"
