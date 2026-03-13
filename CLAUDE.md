# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

GigFlow API — a Django 6 REST API using Python 3.13. Authentication is handled by the `authease` package (JWT, email OTP, OAuth).

## Commands

```bash
# Use the venv python directly (activate doesn't work in this shell)
"venv/Scripts/python.exe" manage.py runserver          # Start dev server
"venv/Scripts/python.exe" manage.py migrate             # Run migrations
"venv/Scripts/python.exe" manage.py makemigrations      # Create migrations
"venv/Scripts/python.exe" manage.py createsuperuser     # Create admin user
"venv/Scripts/python.exe" manage.py check               # Validate config
"venv/Scripts/python.exe" -m pip install <pkg>           # Install packages
```

## Architecture

- **Framework**: Django 6.0 + Django REST Framework
- **Auth**: `authease` package — provides JWT auth (SimpleJWT), email OTP verification, password reset, and Google/GitHub OAuth
- **User model**: `AUTH_USER_MODEL = 'auth_core.User'` (from authease) with email as the login field
- **Database**: SQLite (dev), configure via `DATABASES` in settings for production
- **Config**: Environment variables for secrets (see `.env.example`)

## Key Files

- `gigflow/settings.py` — all Django + authease + JWT + DRF config
- `gigflow/urls.py` — routes: `api/auth/` (authease core), `api/oauth/` (social login)

## API Endpoints (from authease)

- `POST api/auth/register/` — register
- `POST api/auth/login/` — login (returns JWT)
- `POST api/auth/verify_email/` — verify email with OTP
- `POST api/auth/resend_otp/` — resend OTP
- `POST api/auth/password_reset/` — request password reset
- `PATCH api/auth/set_new_password/` — set new password
- `POST api/auth/change_password/` — change password (authenticated)
- `POST api/auth/logout/` — logout (blacklist refresh token)
- `POST api/auth/token/refresh/` — refresh access token
- `POST api/oauth/google/` — Google sign-in
- `POST api/oauth/github/` — GitHub sign-in
