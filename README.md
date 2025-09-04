# ACEest Fitness and Gym – DevOps Assignment

## Overview

This project is a Flask-based fitness and gym management application built to demonstrate best practices in DevOps, including version control, automated testing, containerization, and CI/CD automation.

- Frontend/Backend: Python Flask
- Testing: Pytest framework
- Containerization: Docker
- CI/CD: GitHub Actions (automated testing, build, and Docker Hub deployment)

---

## Features

- Add and review workouts (name, duration, history)
- REST API endpoints for easy integration
- Responsive web interface (Bootstrap)
- Input validation & error handling
- Automated summary analytics

---

## Local Setup

1. Clone Repository
    ```
    git clone https://github.com/pguser12-beep/aceest-fitness.git
    cd aceest-fitness
    ```

2. Create Virtual Environment
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install Dependencies
    ```
    pip install -r requirements.txt
    ```

4. Run Application
    ```
    python app.py
    ```
    Visit [http://localhost:5000](http://localhost:5000)

---

## Run Tests Locally

pytest tests/ -v

text

---

## Run with Docker

docker build -t aceest-fitness .
docker run -p 5000:5000 aceest-fitness

text

---

## Project Structure

aceest-fitness/
├── app/
│ ├── init.py
│ ├── models.py
│ ├── routes.py
│ └── templates/
├── tests/
│ └── test_app.py
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md

text

---

## CI/CD Pipeline

- GitHub Actions runs on each commit/pull request
    - Installs dependencies
    - Runs Pytest tests
    - Builds and pushes Docker image to Docker Hub
    - Runs security scans (Trivy, CodeQL)
- Configured in `.github/workflows/ci-cd.yml`
- Secrets required: `DOCKER_USERNAME`, `DOCKER_TOKEN`

---

## Useful Links

- Project Repo: https://github.com/pguser12-beep/aceest-fitness.git
- Docker Image: https://hub.docker.com/repository/docker/imp98/aceest-fitness/
- Actions: https://github.com/pguser12-beep/aceest-fitness/actions

---

## Maintainer

- Name: Prachi Gupta
- Email: 2024tm93236@wilp.bits-pilani.ac.in

