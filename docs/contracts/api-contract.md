# API Contract
## Bilingual AI Customer Support & Resolution System

**Base URL:** `http://localhost:8000`

### 1. Health Check

**Endpoint:** `GET /health`

**Purpose:** Check whether the backend is running.

**Expected response:**
```json
{
  "status": "ok"
}
```

### 2. Get Complaints

**Endpoint:** `GET /complaints`

**Purpose:** Retrieve complaints to display on the dashboard and complaints page.

**Expected response:** An array of complaint objects.

```json
[
  {
    "id": 1,
    "text": "My order has not arrived.",
    "category": "Shipping & Delivery",
    "priority": "High",
    "status": "Open",
    "aiConfidence": 0.93,
    "reply": "",
    "sources": []
  }
]
```

**Fields:**
- `id`: Unique complaint identifier.
- `text`: Complaint text.
- `category`: Predicted complaint category.
- `priority`: Complaint priority.
- `status`: Current complaint status.
- `aiConfidence`: AI classification confidence, from `0` to `1`.
- `reply`: Suggested or saved reply.
- `sources`: List of supporting information sources.

### 3. Create a Complaint

**Endpoint:** `POST /complaints`

**Purpose:** Submit a new complaint.

**Request body:**
```json
{
  "text": "My account is locked."
}
```

**Expected response:** The created complaint object, including its assigned ID and current processing status.

**Status:** Planned; backend implementation is required.

### 4. Save a Reply

**Endpoint:** `POST /complaints/{complaint_id}/reply`

**Purpose:** Save an agent's reply to a complaint.

**Request body:**
```json
{
  "reply": "We are reviewing your complaint."
}
```

**Expected response:** Confirmation that the reply was saved.

**Status:** Planned; backend implementation is required.

### 5. Update Complaint Status

**Endpoint:** `PATCH /complaints/{complaint_id}/status`

**Purpose:** Update the status of a complaint.

**Request body:**
```json
{
  "status": "Resolved"
}
```

**Expected response:** The updated complaint status.

**Status:** Planned; backend implementation is required.

### Error Handling

The API should return appropriate HTTP status codes:
- `200 OK`: Request completed successfully.
- `201 Created`: A new complaint was created.
- `400 Bad Request`: Invalid request data.
- `404 Not Found`: Complaint does not exist.
- `422 Unprocessable Entity`: Request validation failed.
- `500 Internal Server Error`: Unexpected server error.

### Frontend Integration

The frontend currently uses `GET /complaints` to retrieve complaint data from the backend.

The frontend and backend must use consistent field names and data types. The reply and status endpoints must be implemented before the corresponding frontend actions can persist changes.