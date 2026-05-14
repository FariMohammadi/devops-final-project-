# Study Planner

A simple study task manager built with Python Flask, containerized with Docker, and deployed via a CI/CD pipeline using GitHub Actions. Infrastructure is managed with Terraform.

## Project Structure

devOps-project/
├── app/
│   ├── app.py              
│   ├── test_app.py         
│   └── requirements.txt    
├── terraform/
│   ├── main.tf             
│   ├── variables.tf        
│   └── outputs.tf          
├── .github/workflows/
│   └── ci-cd.yml           
├── Dockerfile
├── .gitignore
└── README.md

## How to Run

### Run locally
cd app
pip install -r requirements.txt
python app.py

Visit http://localhost:5000

### Run with Docker
docker build -t study-planner .
docker run -d -p 5000:5000 --name myapp study-planner

### Run Tests
cd app
pytest test_app.py -v

### Deploy with Terraform
cd terraform
terraform init
terraform apply

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Web UI |
| GET | /api/tasks | Get all tasks |
| POST | /api/tasks | Add a task |
| PUT | /api/tasks/<id> | Update a task |
| DELETE | /api/tasks/<id> | Delete a task |
| GET | /api/health | Health check |
| GET | /api/info | App info |

## Tools Used

- Python Flask
- Git / GitHub
- Docker
- GitHub Actions
- Terraform
- Pytest
