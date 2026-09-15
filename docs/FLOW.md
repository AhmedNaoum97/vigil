# Vuln Scanner as a Service — Request Flow

1. Client → POST /scans {target} → API
2. API creates scan_jobs row (status: pending) → returns job_id to client
3. API pushes job onto queue (Celery/Redis)
4. Worker picks up job → runs nmap scan against target
5. Worker parses results → writes scan_results rows
6. Worker cross-references service versions against CVE/NVD → writes findings rows
7. Worker updates scan_jobs status → completed (or failed)
8. Client polls GET /scans/{id} → sees status + results once completed
