terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}


provider "docker" {}

#docker image
resource "docker_image" "app_image" {
  name = "devops-task-manager:terraform"

  build {
    context    = "${path.module}/.."
    dockerfile = "Dockerfile"
  }

  triggers = {
    dockerfile = filemd5("${path.module}/../Dockerfile")
    app_code   = filemd5("${path.module}/../app/app.py")
  }
}


# Docker Container

resource "docker_container" "app_container" {
  name  = var.container_name
  image = docker_image.app_image.image_id

  ports {
    internal = 5000
    external = var.host_port
  }

  restart = "unless-stopped"

  healthcheck {
    test         = ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')"]
    interval     = "30s"
    timeout      = "5s"
    start_period = "10s"
    retries      = 3
  }

  labels {
    label = "managed_by"
    value = "terraform"
  }

  labels {
    label = "environment"
    value = var.environment
  }
}
