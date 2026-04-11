# MetroBlue API Integration Guide

## Base URL
`http://127.0.0.1:8000`

## Auth
Most endpoints require `X-API-KEY` header (user-provided at runtime in dashboard).

```js
const headers = { "X-API-KEY": "<your-api-key>" };
```

---

## `GET /api/health`
Health check.

**Response shape**
```json
{ "success": true, "data": { "status": "ok" }, "message": "Success", "timestamp": "..." }
```

**fetch example**
```js
fetch("/api/health").then(r => r.json()).then(console.log);
```

## `GET /api/config`
Frontend-safe configuration.

**Response shape**
```json
{ "success": true, "data": { "api_url": "...", "api_key_header": "X-API-KEY", "requires_api_key": true } }
```

**fetch example**
```js
fetch("/api/config").then(r => r.json()).then(console.log);
```

## `GET /api/stats`
Returns basic counts.

**Response shape**
```json
{ "success": true, "data": { "leads": 0, "clients": 0, "last_updated": "..." } }
```

**fetch example**
```js
fetch("/api/stats", { headers }).then(r => r.json()).then(console.log);
```

## `POST /api/leads/score`
Scores a single lead.

**Request shape**
```json
{
  "name": "Jane",
  "source": "Google",
  "course_service": "IELTS",
  "gender": "Female",
  "location": "Darwin",
  "phone": "0400000000",
  "stage": "qualified"
}
```

**Response shape**
```json
{ "success": true, "data": { "score": 0.82, "label": "Hot", "top_factors": [] } }
```

**fetch example**
```js
fetch("/api/leads/score", {
  method: "POST",
  headers: { ...headers, "Content-Type": "application/json" },
  body: JSON.stringify({ source: "Google", course_service: "IELTS" })
}).then(r => r.json()).then(console.log);
```

## `GET /api/leads/scores?limit=200`
Batch scores leads from DB.

**Response shape**
```json
{ "success": true, "data": { "results": [{ "lead_id": 1, "name": "Jane", "stage": "qualified", "score": 0.82, "label": "Hot" }] } }
```

**fetch example**
```js
fetch("/api/leads/scores?limit=100", { headers }).then(r => r.json()).then(console.log);
```

## `GET /api/revenue/forecast?months=6&history_months=6`
Returns history + forecast + interval bands.

**Response shape**
```json
{
  "success": true,
  "data": {
    "history": [{ "month": "2026-01", "revenue": 52000 }],
    "forecast": [{ "month": "F+1", "predicted_revenue": 53560, "lower_bound": 48204, "upper_bound": 58916 }]
  }
}
```

**fetch example**
```js
fetch("/api/revenue/forecast?months=6&history_months=6", { headers }).then(r => r.json()).then(console.log);
```

## `GET /api/revenue/overdue`
Lists overdue receivables.

**Response shape**
```json
{ "success": true, "data": [{ "client": "ABC Corp", "amount_due": 12000, "days_overdue": 15 }] }
```

**fetch example**
```js
fetch("/api/revenue/overdue", { headers }).then(r => r.json()).then(console.log);
```

## `GET /api/clients/risk`
Lists client risk level.

**Response shape**
```json
{ "success": true, "data": [{ "client": "ABC Corp", "risk_level": "Medium", "reason": "Payment overdue by 20+ days" }] }
```

**fetch example**
```js
fetch("/api/clients/risk", { headers }).then(r => r.json()).then(console.log);
```

## `POST /api/models/retrain`
Triggers model retraining in background.

**Request shape**
No body.

**Response shape**
```json
{ "success": true, "message": "Retrain process started in background" }
```

**fetch example**
```js
fetch("/api/models/retrain", { method: "POST", headers }).then(r => r.json()).then(console.log);
```
