data "google_secret_manager_secret_version" "env_secret" {
  secret  = var.env_secret
  project = var.gcp_project[terraform.workspace]
  version = "latest"
}