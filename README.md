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
2. Installs Python dependencies
3. Runs the pytest test suite

A green tick indicates all tests passed. A red cross indicates a failure that should be investigated before merging.

---

## Known Limitations & Security Shortcomings

This project is a **local development and learning exercise only**. The following issues are known and will be addressed in Phase 2 (AWS Deployment) and Phase 3 (Security Hardening).

### 🔴 High Priority

**Hardcoded credentials in docker-compose.yml**
MongoDB credentials are currently defined as plain text in `docker-compose.yml`. In production these should be stored in a secrets management service such as AWS Secrets Manager and injected at runtime, never committed to source control.

**No production WSGI server**
The app currently runs on Flask's built-in development server, which is single-threaded, not performant, and not suitable for production traffic. This will be replaced with Gunicorn prior to AWS deployment.

**No .dockerignore optimisation**
A `.dockerignore` is in place but the Docker image has not been fully optimised. Multi-stage builds should be implemented to reduce final image size before production deployment.

### 🟡 Medium Priority

**MongoDB root user**
The application connects to MongoDB using a root-level admin user. In production a dedicated least-privilege user should be created with only `readWrite` access to the specific database the application requires.

**MongoDB publicly accessible**
Port 27017 is exposed on the host machine via docker-compose. In production MongoDB should sit in a private subnet with no public IP, accessible only by the application layer via internal networking.

**Insufficient test coverage**
The current test suite covers only a single happy-path route. Prior to production deployment tests should cover the database route, unhappy paths (e.g. database unavailable), and use mocking to remove dependency on a live MongoDB instance.

**No docker-compose healthcheck**
There is a potential race condition where Flask starts before MongoDB is fully ready. A healthcheck on the MongoDB service should be added to docker-compose to ensure correct startup ordering.

### 🟢 Lower Priority

**No logging strategy**
The application has no structured logging. Basic Python logging should be added to aid debugging in production environments where direct container access is not always available.

**No pip caching in GitHub Actions**
The CI pipeline reinstalls all dependencies from scratch on every run. Dependency caching should be added to the workflow to improve pipeline speed.

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

---

## Notes

This project was built as part of a structured DevOps learning plan in preparation for a Development Lead role at a SaaS bioinformatics startup. It is not intended for production use in its current state.
