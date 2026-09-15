# Vuln Scanner as a Service — DB Schema

## users

| Column        | Type           | Notes |
| ------------- | -------------- | ----- |
| id            | PK             |       |
| email         | string, unique |       |
| password_hash | string         |       |
| created_at    | timestamp      |       |

## scan_jobs

| Column       | Type       | Notes                                  |
| ------------ | ---------- | -------------------------------------- |
| id           | PK         |                                        |
| user_id      | FK → users |                                        |
| target       | string     | IP, hostname, or CIDR                  |
| status       | enum       | pending / running / completed / failed |
| created_at   | timestamp  |                                        |
| started_at   | timestamp  | nullable                               |
| completed_at | timestamp  | nullable                               |

## scan_results

| Column          | Type           | Notes                          |
| --------------- | -------------- | ------------------------------ |
| id              | PK             |                                |
| scan_job_id     | FK → scan_jobs |                                |
| host            | string         | relevant if target was a range |
| port            | integer        |                                |
| protocol        | enum           | tcp / udp                      |
| service_name    | string         |                                |
| service_version | string         |                                |

## findings

| Column         | Type              | Notes                          |
| -------------- | ----------------- | ------------------------------ |
| id             | PK                |                                |
| scan_result_id | FK → scan_results |                                |
| cve_id         | string            |                                |
| severity       | enum              | low / medium / high / critical |
| description    | text              |                                |
| source         | string            | e.g. "NVD"                     |

## Scoping decision (v1)

v1 supports a single target (host/IP) per scan job, not CIDR ranges. Range support is a planned v2 extension. `target` on `scan_jobs` is a single string; `host` on `scan_results` is kept for forward compatibility with v2.
