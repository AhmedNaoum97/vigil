# Vuln Scanner as a Service — API Endpoints

## Auth

| Method | Path           | Description               |
| ------ | -------------- | ------------------------- |
| POST   | /auth/register | Create a new user         |
| POST   | /auth/login    | Authenticate, returns JWT |

## Scans

| Method | Path        | Description                                                            |
| ------ | ----------- | ---------------------------------------------------------------------- |
| POST   | /scans      | Submit a scan job (body: `target`). Returns `job_id`, status `pending` |
| GET    | /scans      | List current user's scan jobs                                          |
| GET    | /scans/{id} | Get job status (and results once completed)                            |
