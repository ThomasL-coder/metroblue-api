# MetroBlue API Integration

## Base URL
http://127.0.0.1:8000

---

## Lead Scores
GET /api/leads/scores

Example:
```javascript
fetch('/api/leads/scores')
  .then(res => res.json())
  .then(data => console.log(data));