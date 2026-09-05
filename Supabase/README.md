# CropGuard AI: Supabase Integration & Security Guide

**Target Project URL:** `https://tspdpkyhszrebrclsefz.supabase.co`

---

## 1. Architectural Role of Supabase

Supabase delivers the production-grade PostgreSQL database and Authentication infrastructure for CropGuard AI:
1. **Supabase Auth:** Handles JWT-based user signup, login, session persistence, and secure token issuance.
2. **PostgreSQL Relational Storage:** Preserves structured prediction logs, historical telemetry, chat logs, and reference crop biology.
3. **Row Level Security (RLS):** Guarantees zero cross-farmer data leakage. Each query checks `auth.uid() = user_id`.

---

## 2. Database Schema Execution

To configure your hosted Supabase instance:
1. Open the [Supabase Dashboard](https://supabase.com/dashboard/project/tspdpkyhszrebrclsefz).
2. Navigate to the **SQL Editor** on the left menu.
3. Click **New query**, paste the contents of `Supabase/schema.sql`, and click **Run**.
4. Create a second query, paste the contents of `Supabase/policies.sql`, and click **Run**.

---

## 3. Row Level Security (RLS) Verification

| Table | RLS Active | Access Policy |
| :--- | :--- | :--- |
| `profiles` | **YES** | User can only `SELECT` and `UPDATE` their matching `id = auth.uid()` |
| `prediction_history`| **YES** | User can only query and append records where `user_id = auth.uid()` |
| `chat_history` | **YES** | Farmer can only view their own conversational exchanges |
| `crop_knowledge` | **YES** | Read-only to public/authenticated clients; `service_role` required for writes |

---

## 4. Environment Variables Required

In your `.env` (backend) or Flutter configuration:
```env
SUPABASE_URL=https://tspdpkyhszrebrclsefz.supabase.co
SUPABASE_ANON_KEY=<your-public-anon-key-from-api-settings>
```
> [!CAUTION]
> Never expose `SUPABASE_SERVICE_ROLE_KEY` inside Flutter or client-side bundles. The client requires only the public `anon` key, with user identities safely resolved by Supabase JWTs.
