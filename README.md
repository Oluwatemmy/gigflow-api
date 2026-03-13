# GigFlow API

A freelancing platform REST API (Upwork-style) built with Django 6 and Django REST Framework. Features user profiles, job postings, proposals, messaging, and reviews. Built as a real-world integration testbed for the [authease](https://pypi.org/project/authease/) authentication package (JWT, email OTP, Google/GitHub OAuth).

## Tech Stack

- **Python** 3.13
- **Django** 6.0
- **Django REST Framework** 3.16
- **authease** — JWT auth, email OTP verification, password reset, Google/GitHub OAuth
- **SimpleJWT** — token management with blacklisting
- **drf-yasg** — Swagger/OpenAPI documentation
- **SQLite** (dev) — swap to PostgreSQL/MySQL for production

## Setup

```bash
# Clone
git clone https://github.com/Oluwatemmy/gigflow-api.git
cd gigflow-api

# Virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Edit .env with your secrets

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

## API Documentation

- **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## API Endpoints

### Authentication (authease)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/verify_email/` | Verify email with OTP |
| POST | `/api/auth/resend_otp/` | Resend OTP |
| POST | `/api/auth/login/` | Login (returns JWT) |
| POST | `/api/auth/logout/` | Logout (blacklist token) |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| POST | `/api/auth/password_reset/` | Request password reset |
| PATCH | `/api/auth/set_new_password/` | Set new password |
| POST | `/api/auth/change_password/` | Change password (authenticated) |
| POST | `/api/oauth/google/` | Google sign-in |
| POST | `/api/oauth/github/` | GitHub sign-in |

### Profiles

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/profiles/` | Create profile (choose role) |
| GET | `/api/profiles/me/` | Get my profile |
| PATCH | `/api/profiles/me/` | Update my profile |
| GET | `/api/profiles/{id}/` | View a profile |
| GET | `/api/profiles/freelancers/` | List freelancers |
| POST | `/api/profiles/me/portfolio/` | Add portfolio item |
| DELETE | `/api/profiles/me/portfolio/{id}/` | Remove portfolio item |

### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs/` | List jobs (filterable) |
| POST | `/api/jobs/create/` | Post a job (client) |
| GET | `/api/jobs/{id}/` | Job detail |
| PATCH | `/api/jobs/{id}/` | Update job (owner) |
| POST | `/api/jobs/{id}/close/` | Close job (owner) |
| POST | `/api/jobs/{id}/complete/` | Mark complete (owner) |
| GET | `/api/jobs/my/` | My jobs |
| GET | `/api/categories/` | List categories |
| POST | `/api/categories/` | Create category (client) |

### Proposals

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/proposals/{job_id}/` | List proposals (job owner) |
| POST | `/api/proposals/{job_id}/create/` | Submit proposal (freelancer) |
| GET | `/api/proposals/{job_id}/{id}/` | Proposal detail |
| PATCH | `/api/proposals/{job_id}/{id}/` | Edit proposal (author, while pending) |
| DELETE | `/api/proposals/{job_id}/{id}/` | Withdraw proposal (author) |
| POST | `/api/proposals/{job_id}/{id}/accept/` | Accept proposal (job owner) |
| POST | `/api/proposals/{job_id}/{id}/reject/` | Reject proposal (job owner) |
| GET | `/api/proposals/my/` | My proposals (freelancer) |

### Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/reviews/job/{job_id}/create/` | Leave review (completed jobs) |
| GET | `/api/reviews/job/{job_id}/` | Reviews for a job |
| GET | `/api/reviews/profile/{profile_id}/` | Reviews for a user |

### Messaging

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/messages/jobs/{job_id}/` | Job messages |
| POST | `/api/messages/jobs/{job_id}/` | Send message |
| GET | `/api/messages/conversations/` | My conversations |

## Job Workflow

```
OPEN --> IN_PROGRESS (proposal accepted) --> COMPLETED (client marks done)
OPEN --> CLOSED (client cancels)
```

When a proposal is accepted:
- Other pending proposals are auto-rejected
- A conversation is created for the job
- Job status moves to `in_progress`

## Project Structure

```
gigflow-api/
├── core/            # Shared permissions & validators
├── profiles/        # User profiles (freelancer + client)
├── jobs/            # Job listings & categories
├── proposals/       # Proposals/applications
├── reviews/         # Ratings and reviews
├── messaging/       # Per-job conversations
└── gigflow/         # Django project config
```

## Environment Variables

```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@gigflow.com
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

## License

MIT
