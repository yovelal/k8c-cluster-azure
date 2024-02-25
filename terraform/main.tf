
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_kubernetes_cluster" "aks" {
  depends_on          = [azurerm_resource_group.rg]
  name                = var.cluster_name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = "aks-${var.cluster_name}"

  default_node_pool {
    name       = "default"
    node_count = var.system_node_count
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  role_based_access_control_enabled = true
  http_application_routing_enabled = true

  network_profile {
    network_plugin = "azure"
    network_policy = "calico"
  }
  kubernetes_version = var.kubernetes_version

}

