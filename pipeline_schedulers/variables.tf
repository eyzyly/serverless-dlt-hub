variable "project_id" {
  description = "The ID of the Google Cloud project where resources will be created."
  type        = string

}

variable "region" {
  description = "The region where resources will be created."
  type        = string
}

variable "cloud_run_job_name" {
  description = "The name of the Cloud Run job."
  type        = string
}

variable "service_account_email" {
  description = "The email of the service account to use for authentication."
  type        = string
}

variable "gcs_bucket_name" {
  description = "The name of the Google Cloud Storage bucket."
  type        = string
}