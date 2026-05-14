output "container_id" {
  description = "ID of the running Docker container"
  value       = docker_container.app_container.id
}

output "container_name" {
  description = "Name of the running Docker container"
  value       = docker_container.app_container.name
}

output "app_url" {
  description = "URL to access the application"
  value       = "http://localhost:${var.host_port}"
}

output "image_id" {
  description = "Docker image ID used"
  value       = docker_image.app_image.image_id
}
