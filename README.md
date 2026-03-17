# FlaskAppTest

A containerised Flask + MongoDB application built as a Phase 1 learning exercise for cloud migration preparation. This project demonstrates core DevOps fundamentals including Docker, docker-compose, and automated CI/CD via GitHub Actions.

---

## Project Overview

This project serves as a foundational sandbox for learning the tooling required to migrate a production Flask/MongoDB SaaS platform to cloud infrastructure (AWS). It covers containerisation, multi-service orchestration, environment management, and automated testing pipelines.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Flask |
| WSGI Server | Gunicorn |
| Database | MongoDB 6 |
| Containerisation | Docker, docker-compose |
| CI/CD | GitHub Actions |
| Testing | pytest |

---

## Project Structure

```
FlaskAppTest/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
├── .dockerignore            # Files excluded from Docker build context
├── .env                     # Local environment variables (not committed)
├── .env.example             # Environment variable documentation (committed)
├── .gitignore               # Files excluded from git
├── app.py                   # Flask application
├── docker-compose.yml       # Multi-container orchestration
├── Dockerfile               # Flask app container definition
├── requirements.txt         # Python dependencies
└── test_app.py              # pytest test suite
```

---

## Getting Started

### Prerequisites

- Docker Desktop
- Python 3.11+
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/olivercarter98-sys/flask-mongo-test.git
cd flask-mongo-test
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and populate with your values:
```bash
cp .env.example .env
```

4. Build and run with docker-compose:
```bash
docker-compose up --build
```

5. Visit the application:
- `http://localhost:5000` — Hello world route
- `http://localhost:5000/test-db` — MongoDB connection test

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `MONGO_URI` | MongoDB connection string | `mongodb://admin:password@mongo:27017/flasktest?authSource=admin` |

---

## CI/CD Pipeline

Every push or pull request to `main` triggers the GitHub Actions workflow which:

1. Spins up a MongoDB service container
2. Restores cached pip dependencies if requirements.txt is unchanged
3. Installs Python dependencies
4. Runs the pytest test suite with verbose output

A green tick indicates all tests passed. A red cross indicates a failure that should be investigated before merging.

> **Note:** A Node.js deprecation warning may appear in the Actions log relating to GitHub's internal MongoDB service container action. This is outside our control and does not affect the pipeline. GitHub have indicated this will be resolved before June 2nd, 2026.

---

## Security

### Current Measures
- MongoDB requires authentication via username and password
- Credentials are managed via environment variables, never hardcoded in application code
- `.env` is gitignored and never committed to source control
- `.env.example` documents required variables without exposing values
- Docker build context is minimised via `.dockerignore`
- Flask development server replaced with Gunicorn for production readiness

### Known Limitations

This project is a **local development and learning exercise only**. The following issues are known and will be addressed in Phase 2 (AWS Deployment) and Phase 3 (Security Hardening).

**🔴 High Priority**

**Hardcoded credentials in docker-compose.yml**
MongoDB credentials are currently defined as plain text in `docker-compose.yml`. In production these should be stored in AWS Secrets Manager and injected at runtime, never committed to source control.

**No multi-stage Docker builds**
The Docker image has not been fully optimised. Multi-stage builds should be implemented to reduce final image size before production deployment.

**🟡 Medium Priority**

**MongoDB root user**
The application connects to MongoDB using a root-level admin user. In production a dedicated least-privilege user should be created with only `readWrite` access to the specific database the application requires.

**MongoDB publicly accessible**
Port 27017 is exposed on the host machine via docker-compose. In production MongoDB should sit in a private subnet with no public IP, accessible only by the application layer via internal networking.

**🟢 Lower Priority**

**No logging strategy**
The application has no structured logging. Basic Python logging should be added to aid debugging in production environments where direct container access is not always available.

**No credential rotation**
Credentials are static. In production AWS Secrets Manager should be configured to rotate MongoDB credentials automatically on a regular schedule.

---

## Roadmap

### Phase 2 — AWS Deployment
- Push Docker image to AWS ECR
- Deploy to AWS ECS or Elastic Beanstalk
- Set up staging and production environments
- Configure AWS Secrets Manager for credential management
- Move MongoDB to a private subnet

### Phase 3 — Security Hardening
- IAM roles and least privilege access
- HTTPS via SSL certificate
- Monitoring and alerting via AWS CloudWatch
- Automated credential rotation
- Penetration testing and security audit


