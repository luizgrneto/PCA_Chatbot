variable "app_name" {
  type = map(string)
  description = "Name of the ADK Agent app"
}

variable "env_secret" {
  type = string
  description = "Name of the Google Secret Manager secret containing ADK Agent environment variables"
}

variable "app_description" {
  type = string
  default = "ADK Agent"
  description = "App description"
}

variable "app_plataform" {
  type = string
  default = "python"
}

variable "env" {
  type = map(string)
  default = {
    dev = "dev"
    prd = "prd"
  }
}

variable "app_pool" {
  type = map(string)
  default = {
    dev = "gcp-aiops-dev"
    prd = "gcp-aiops-prod"
  }
}

variable "app_plan_agent" {
type = map(string)
  default = {
    dev = "c0.5m1"
    prd = "c1m1"
  }
}

variable "tags" {
  type = list(string)
  default = ["product=aiops-isesc", "project=aiops-agent"]
}

variable "gcp_project" {
  type = map(string)
  default = {
    dev = "gglobo-aiops-hdg-dev"
    prd = "gglobo-aiops-hdg-prd"
  }
}

variable "region" {
  type = string
  default = "us-east1"
}

variable "team" {
  type = string
  default = "gg_gcom_aiops"
}

variable "iam_roles" {
  type        = set(string)
  description = "Roles used by ADK Agent"
  default = [
    "roles/bigquery.admin",
    "roles/secretmanager.admin",
    "roles/serviceusage.serviceUsageAdmin",
    "roles/aiplatform.user",
  ]
}

variable "tsuru_project" {
  type = map(string)
  default = {
    dev = "gglobo-tsuru-us2-hdg-dev"
    prd = "gglobo-tsuru-br1-hdg-prd"
  }
}
