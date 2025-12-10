resource "tsuru_app" "app" {
  name           = var.app_name[terraform.workspace]
  plan           = var.app_plan_agent[terraform.workspace]
  platform       = var.app_plataform
  team_owner     = var.team
  description    = var.app_description
  pool           = var.app_pool[terraform.workspace]
  tags           = var.tags
  metadata {
    labels = {
      "gatekeeper.tsuru.io/allow-spot"  = "true",
      "logging.tsuru.io/sample"         = "0.01"
    }
    annotations = {
      "app.tsuru.io/service-account-annotations" = jsonencode(
        {
          "iam.gke.io/gcp-service-account" : google_service_account.service_account.email
        }
      )
      "prometheus.io/scrape" = "false"
    }
  }
}

resource "tsuru_app_env" "env" {
  app               = tsuru_app.app.name
  restart_on_update = true

  environment_variables = jsondecode(data.google_secret_manager_secret_version.env_secret.secret_data)

  private_environment_variables = {
    "SERVICE_ACCOUNT_KEY" = base64decode(google_service_account_key.sa_key.private_key)
  }
}

resource "google_service_account_iam_binding" "tsuru_sa_binding" {
  service_account_id = google_service_account.service_account.name
  role               = "roles/iam.workloadIdentityUser"
  members            = ["serviceAccount:${var.tsuru_project[terraform.workspace]}.svc.id.goog[tsuru-${tsuru_app.app.pool}/app-${tsuru_app.app.name}]"]
}
