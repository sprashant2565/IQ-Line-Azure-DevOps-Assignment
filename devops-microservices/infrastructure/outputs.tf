output "resource_group_name" {
  value       = azurerm_resource_group.rg.name
  description = "The name of the Resource Group."
}

output "aks_cluster_name" {
  value       = azurerm_kubernetes_cluster.aks.name
  description = "The name of the AKS cluster."
}

output "acr_login_server" {
  value       = azurerm_container_registry.acr.login_server
  description = "The login server for the Azure Container Registry."
}

output "key_vault_uri" {
  value       = azurerm_key_vault.kv.vault_uri
  description = "The URI of the Azure Key Vault."
}