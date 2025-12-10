terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=6.46.0"
    }
    tsuru = {
      source  = "tsuru/tsuru"
      version = ">= 2.17.0"
    }
  }

  backend "gcs" {
  }
}
