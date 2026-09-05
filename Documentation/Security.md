# CropGuard AI: Security Architecture & Data Governance

CropGuard AI implements a defense-in-depth security model protecting farmer data, model pipelines, and cloud database infrastructure.

---

## 1. 20 Security Principles Implemented

1. **Strict Environment Variable Isolation:** Credentials reside exclusively in runtime environment variables (`.env`).
2. **Zero Secrets in Git:** `.gitignore` blocks `.env`, `*.pem`, `*.key`, and secret configurations from ever entering Git history.
3. **Template Provided:** `.env.example` documents all required parameters without containing live secrets.
4. **Supabase Row Level Security (RLS):** All database tables have RLS enabled with granular isolation policies.
5. **Farmer Data Isolation:** Queries enforce `auth.uid() = user_id`. No farmer can view, modify, or delete another producer's records.
6. **No Service-Role Key in Frontend:** The Flutter client bundle is strictly provisioned with the public anonymous key (`SUPABASE_ANON_KEY`); administrative service-role keys are never embedded in client binaries.
7. **Pydantic Data Validation:** Every incoming API request payload is strictly type-checked and sanitized via Pydantic models.
8. **SQL Injection Prevention:** Supabase queries use parameterized PostgreSQL bindings, preventing SQL injection vulnerabilities.
9. **Safe Error Masking:** Production exceptions return standardized, safe JSON responses without dumping Python stack traces or internal paths to users.
10. **Zero Password/Token Logging:** Sensitive authentication tokens and passwords are excluded from application log files.
11. **Configured CORS:** FastAPI middleware restricts origins to verified frontend clients.
12. **Local AI Privacy:** The local farmer chatbot processes questions 100% on-premise; no conversational data is sent to external LLM servers (OpenAI, Gemini, DeepSeek, etc.).
13. **Bounded Numerical Inputs:** Predictor checks enforce valid biological boundaries (e.g., pH 0-14, humidity 0-100%).
14. **HTTPS Enforcement in Deployment:** Docker and Render deployment configurations mandate TLS/HTTPS encrypted transport.
15. **JWT Token Authentication:** API endpoints verify Bearer tokens issued cryptographically by Supabase Auth.
16. **Session Expiry & Revocation:** Supabase manages refresh token lifecycles and revocation.
17. **Pluggable Weather Fallback:** Weather queries include timeout boundaries (8s) and safe offline agricultural fallbacks to prevent Denial of Service on upstream network timeouts.
18. **Read-Only Agricultural Knowledge:** Reference tables (`crop_knowledge`) are locked against modification by non-administrative users.
19. **Minimal Docker Attack Surface:** Container images build on `python:3.11-slim`, purging temporary build tools and package caches.
20. **Client-Side Secret Absence:** The Flutter mobile application contains zero private database passwords or third-party secret credentials.
