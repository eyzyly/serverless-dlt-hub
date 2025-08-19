locals {
  # List all config files in the configs directory
  config_files = fileset("${path.module}/configs", "*")
}

resource "google_cloud_scheduler_job" "serverless_dlt_hub_triggers" {
  # Create a Cloud Scheduler job for each config file
  for_each = { for file in local.config_files : file => yamldecode(file("${path.module}/configs/${file}")) }

  project = var.project_id
  region  = var.region

  name             = "${each.value.pipeline_name}_pipeline_trigger"
  description      = each.value.description
  schedule         = each.value.schedule
  time_zone        = "Europe/London"
  attempt_deadline = "60s"

  retry_config {
    retry_count = 0
  }

  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${var.cloud_run_job_name}:run"
    body = base64encode(jsonencode({
      "overrides" : {
        "containerOverrides" : [
          {
            "env" : [
              { "name" : "CONFIG_FILE", "value" : each.key }
            ]
          }
        ]
      }
    }))
    headers = {
      "Content-Type" = "application/json"
    }
    oauth_token {
      service_account_email = var.service_account_email
    }
  }
}

resource "google_storage_bucket" "pipeline_configs" {
  # Storage bucket to store pipeline configuration files
  name     = var.gcs_bucket_name
  location = var.region
  project  = var.project_id

  uniform_bucket_level_access = true
}