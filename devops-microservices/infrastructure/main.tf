# 1. Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "${var.project_name}-rg"
  location = var.location
}

# 2. Virtual Network (VNet)
resource "azurerm_virtual_network" "vnet" {
  name                = "${var.project_name}-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = var.vnet_address_space
}

# 3. Subnet for AKS Nodes
resource "azurerm_subnet" "aks_subnet" {
  name                 = "${var.project_name}-aks-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = [var.aks_subnet_address_prefix]
}

# 4. Azure Container Registry (ACR)
# Sku: Basic is chosen for cost-efficiency in a demo/assignment
resource "azurerm_container_registry" "acr" {
  name                = "${var.project_name}acr"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true # Enabled for simpler CI/CD access in a demo
}

# 5. Azure Key Vault
resource "azurerm_key_vault" "kv" {
  name                       = "${var.project_name}-kv"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard" # Standard for cost-efficiency
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get",
      "List",
      "Set",
    ]
  }
}

# Store a dummy secret to demonstrate Key Vault functionality
resource "azurerm_key_vault_secret" "example_secret" {
  name         = "Demo-Secret-Key"
  value        = "This-is-a-secure-value"
  key_vault_id = azurerm_key_vault.kv.id
}

# Retrieve the current client configuration (for Service Principal/User ID and Tenant ID)
data "azurerm_client_config" "current" {}

# 6. Azure Kubernetes Service (AKS) Cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "${var.project_name}-aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${var.project_name}-k8s"

  # Use System Assigned Managed Identity for connecting to ACR and other Azure services securely
  identity {
    type = "SystemAssigned"
  }

  default_node_pool {
    name                = "agentpool"
    vm_size             = "Standard_DS2_v2" # Right-sizing for cost-efficiency
    node_count          = 2                 # Minimal node count
    vnet_subnet_id      = azurerm_subnet.aks_subnet.id
    enable_auto_scaling = true # Demonstrate cost optimization / scalability
    min_count           = 2
    max_count           = 3
  }

  network_profile {
    network_plugin = "azure" # CNI for advanced networking
    dns_service_ip = "10.0.0.10"
    service_cidr   = "10.0.0.0/24"
  }
}

# Grant the AKS Managed Identity (MI) Pull access to ACR
resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.aks.identity[0].principal_id
}

# Grant the AKS System Assigned Managed Identity (MI) Read access to Key Vault
# This is required if you use Azure workload identity (or a similar method) to fetch secrets
resource "azurerm_key_vault_access_policy" "aks_kv_access" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_kubernetes_cluster.aks.identity[0].principal_id

  secret_permissions = [
    "Get",
  ]
}

resource "azurerm_application_insights" "app_insights" {
  name                = "${var.project_name}-appinsights"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  application_type    = "web"
}

output "app_insights_ikey" {
  value     = azurerm_application_insights.app_insights.instrumentation_key
  sensitive = true
}
