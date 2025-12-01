# Define Terraform settings
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Configure the Azure Provider
# Terraform will use the credentials configured in your environment (e.g., 'az login' or Service Principal)
provider "azurerm" {
  features {}
  skip_provider_registration = true
}