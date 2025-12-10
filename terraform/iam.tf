resource "google_service_account" "service_account" {
  project      = var.gcp_project[terraform.workspace]
  account_id   = "${var.app_name[terraform.workspace]}"
  display_name = "Agent ${var.app_name[terraform.workspace]} ${var.env[terraform.workspace]}"
  description  = "Service account used by ADK Agent"
}

resource "google_project_iam_member" "iam_roles" {  
  for_each     = var.iam_roles
  project      = var.gcp_project[terraform.workspace]
  role         = each.key
  member       = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_service_account_key" "sa_key" {
  service_account_id = google_service_account.service_account.name
}
