variable "container_name" {
  description = "Name of the Docker container"
  type        = string
  default     = "devops-task-manager"
}

variable "host_port" {
  description = "Host port to expose the application on"
  type        = number
  default     = 5000
}

variable "environment" {
  description = "Deployment environment (development, staging, production)"
  type        = string
  default     = "development"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be one of: development, staging, production."
  }
}
