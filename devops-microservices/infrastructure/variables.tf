variable "location" {
  description = "The Azure region to deploy resources in"
  type        = string
  default     = "East US"
}

variable "project_name" {
  description = "A unique prefix for all resources"
  type        = string
  default     = "devopsassign" # Change this to a unique identifier
}

variable "vnet_address_space" {
  description = "The CIDR block for the VNet"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "aks_subnet_address_prefix" {
  description = "The CIDR prefix for the AKS subnet"
  type        = string
  default     = "10.0.1.0/24"
}