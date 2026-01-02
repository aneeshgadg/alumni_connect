# API Specification

## API Design Principles

1. **Domain Separation**: Separate endpoints for Student and Alumni domains
2. **RESTful Conventions**: Standard HTTP methods, clear resource naming
3. **Versioning**: All endpoints prefixed with `/api/v1/`
4. **Authentication**: JWT tokens in Authorization header
5. **Pagination**: All list endpoints support cursor-based pagination
6. **Error Handling**: Consistent error response format
7. **Rate Limiting**: Per-user rate limits to prevent abuse

## Base URL Structure

```
/api/v1/
├── /auth/              # Authentication endpoints
├── /students/          # Student domain endpoints
├── /alumni/            # Alumni domain endpoints
├── /requests/          # Introduction request endpoints
├── /introductions/     # Introduction endpoints
├── /outcomes/          # Outcome tracking endpoints
└── /admin/             # Admin endpoints (future)
```

## Authentication

### POST /api/v1/auth/login
Authenticate user and receive JWT token.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response** (200):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "refresh_token_string",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "role": "student" | "alumni"
  },
  "expires_in": 3600
}
```

### POST /api/v1/auth/refresh
Refresh access token.

**Request**:
```json
{
  "refresh_token": "refresh_token_string"
}
```

**Response**: Same as login response.

---

## Student Domain APIs

### GET /api/v1/students/me
Get current student's profile.

**Response** (200):
```json
{
  "id": "uuid",
  "email": "student@university.edu",
  "graduation_year": 2025,
  "major": "Computer Science",
  "career_interests": [
    {
      "type": "industry",
      "value": "Technology",
      "priority": 1
    }
  ],
  "current_location": "San Francisco, CA",
  "bio": "I'm passionate about building products that make a difference...",
  "hobbies": ["Rock climbing", "Photography", "Cooking"],
  "interests": ["Sustainable technology", "Startup ecosystem", "Travel"],
  "interesting_facts": ["Studied abroad in Japan", "Published research on ML"],
  "reputation_score": 4.2,
  "total_requests": 5,
  "successful_introductions": 3
}
```

### PUT /api/v1/students/me
Update student profile.

**Request**:
```json
{
  "graduation_year": 2025,
  "major": "Computer Science",
  "career_interests": [...],
  "bio": "Updated bio text",
  "hobbies": ["Rock climbing", "Photography", "Cooking"],
  "interests": ["Sustainable technology", "Startup ecosystem"],
  "interesting_facts": ["Studied abroad in Japan", "Published research on ML"]
}
```

### GET /api/v1/students/me/requests
Get student's introduction requests.

**Query Parameters**:
- `status`: Filter by status (pending, approved, declined, etc.)
- `limit`: Number of results (default: 20)
- `cursor`: Pagination cursor

**Response** (200):
```json
{
  "data": [
    {
      "id": "uuid",
      "target_alumni": {
        "id": "uuid",
        "name": "John Doe",
        "current_role": "Senior Engineer",
        "current_company": "Tech Corp"
      },
      "request_type": "informational_interview",
      "status": "approved",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "pagination": {
    "next_cursor": "cursor_string",
    "has_more": true
  }
}
```

### GET /api/v1/students/discover
Discover relevant alumni for introductions.

**Query Parameters**:
- `industry`: Filter by industry
- `role`: Filter by role type
- `location`: Filter by location
- `limit`: Number of results (default: 20)
- `cursor`: Pagination cursor

**Response** (200):
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "Jane Smith",
      "current_role": "Product Manager",
      "current_company": "Tech Corp",
      "industry": "Technology",
      "location": "San Francisco, CA",
      "shared_context": [
        {
          "type": "same_major",
          "value": "Computer Science"
        },
        {
          "type": "same_company_interest",
          "value": "Tech Corp"
        },
        {
          "type": "shared_interest",
          "value": "Rock climbing"
        }
      ],
      "helpfulness_score": 4.5,
      "response_rate": 0.85
    }
  ],
  "pagination": {
    "next_cursor": "cursor_string",
    "has_more": true
  }
}
```

### POST /api/v1/students/requests
Create a new introduction request.

**Request**:
```json
{
  "target_alumni_id": "uuid",
  "request_type": "informational_interview",
  "context": {
    "shared_major": true,
    "why_this_connection": "I'm interested in product management...",
    "specific_ask": "I'd like to learn about your day-to-day..."
  },
  "message": "Template-based message text"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "status": "pending",
  "created_at": "2024-01-15T10:00:00Z",
  "expires_at": "2024-01-22T10:00:00Z"
}
```

---

## Alumni Domain APIs

### GET /api/v1/alumni/me
Get current alumni's profile.

**Response** (200):
```json
{
  "id": "uuid",
  "email": "alumni@example.com",
  "graduation_year": 2015,
  "current_role": "Senior Engineer",
  "current_company": "Tech Corp",
  "industry": "Technology",
  "location": "San Francisco, CA",
  "bio": "I've been building products for over 10 years...",
  "hobbies": ["Rock climbing", "Photography", "Playing guitar"],
  "interests": ["Sustainable technology", "Travel", "Reading sci-fi"],
  "interesting_facts": ["Speak three languages", "Volunteer at food bank"],
  "availability_status": "open",
  "max_requests_per_month": 5,
  "current_month_requests": 2,
  "helpfulness_score": 4.5,
  "total_introductions": 12
}
```

### PUT /api/v1/alumni/me
Update alumni profile.

**Request**:
```json
{
  "current_role": "Principal Engineer",
  "current_company": "New Corp",
  "bio": "Updated professional summary...",
  "hobbies": ["Rock climbing", "Photography", "Playing guitar"],
  "interests": ["Sustainable technology", "Travel"],
  "interesting_facts": ["Speak three languages", "Volunteer at food bank"],
  "availability_status": "limited",
  "request_preferences": {
    "informational_interview": true,
    "referral": false
  }
}
```

### GET /api/v1/alumni/me/requests
Get pending introduction requests for alumni.

**Query Parameters**:
- `status`: Filter by status (default: pending)
- `limit`: Number of results (default: 20)
- `cursor`: Pagination cursor

**Response** (200):
```json
{
  "data": [
    {
      "id": "uuid",
      "student": {
        "id": "uuid",
        "name": "Student Name",
        "graduation_year": 2025,
        "major": "Computer Science"
      },
      "request_type": "informational_interview",
      "context": {
        "shared_major": true,
        "why_this_connection": "...",
        "specific_ask": "..."
      },
      "message": "Request message text",
      "quality_score": 4.2,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "pagination": {
    "next_cursor": "cursor_string",
    "has_more": false
  }
}
```

### POST /api/v1/alumni/requests/{request_id}/approve
Approve an introduction request.

**Request** (optional):
```json
{
  "introduction_method": "platform_email",
  "custom_message": "Optional custom introduction text"
}
```

**Response** (200):
```json
{
  "introduction_id": "uuid",
  "status": "pending",
  "introduction_template": "Pre-filled introduction text..."
}
```

### POST /api/v1/alumni/requests/{request_id}/decline
Decline an introduction request.

**Request** (optional):
```json
{
  "reason": "Too busy this month"
}
```

**Response** (200):
```json
{
  "status": "declined",
  "declined_at": "2024-01-15T10:00:00Z"
}
```

### GET /api/v1/alumni/me/introductions
Get alumni's introductions.

**Query Parameters**:
- `status`: Filter by status
- `limit`: Number of results
- `cursor`: Pagination cursor

**Response** (200):
```json
{
  "data": [
    {
      "id": "uuid",
      "student": {
        "id": "uuid",
        "name": "Student Name"
      },
      "status": "active",
      "introduced_at": "2024-01-15T10:00:00Z",
      "request_type": "informational_interview
    }
  ],
  "pagination": {...}
}
```

---

## Introduction Request APIs (Shared)

### GET /api/v1/requests/{request_id}
Get details of a specific request.

**Response** (200):
```json
{
  "id": "uuid",
  "student": {...},
  "target_alumni": {...},
  "request_type": "informational_interview",
  "context": {...},
  "message": "...",
  "status": "approved",
  "created_at": "2024-01-15T10:00:00Z",
  "approved_at": "2024-01-16T10:00:00Z"
}
```

### DELETE /api/v1/requests/{request_id}
Cancel a request (student only, if pending).

**Response** (200):
```json
{
  "status": "cancelled"
}
```

---

## Introduction APIs (Shared)

### GET /api/v1/introductions/{introduction_id}
Get details of a specific introduction.

**Response** (200):
```json
{
  "id": "uuid",
  "request_id": "uuid",
  "student": {...},
  "alumni": {...},
  "introduction_method": "platform_email",
  "introduction_text": "Introduction message...",
  "status": "active",
  "introduced_at": "2024-01-16T10:00:00Z"
}
```

### POST /api/v1/introductions/{introduction_id}/deliver
Deliver introduction (alumni action).

**Request**:
```json
{
  "introduction_text": "Final introduction message",
  "delivery_method": "email"
}
```

**Response** (200):
```json
{
  "status": "active",
  "introduced_at": "2024-01-16T10:00:00Z"
}
```

---

## Outcome Tracking APIs (Shared)

### POST /api/v1/outcomes
Record an outcome for an introduction.

**Request**:
```json
{
  "introduction_id": "uuid",
  "outcome_type": "conversation_occurred",
  "notes": "Had a great 30-minute conversation...",
  "occurred_at": "2024-01-20T10:00:00Z",
  "satisfaction": 5
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "introduction_id": "uuid",
  "outcome_type": "conversation_occurred",
  "recorded_at": "2024-01-20T11:00:00Z"
}
```

### GET /api/v1/introductions/{introduction_id}/outcomes
Get outcomes for an introduction.

**Response** (200):
```json
{
  "data": [
    {
      "id": "uuid",
      "outcome_type": "conversation_occurred",
      "recorded_by": "student",
      "notes": "...",
      "satisfaction": 5,
      "occurred_at": "2024-01-20T10:00:00Z"
    }
  ]
}
```

---

## Error Responses

All errors follow this format:

**Response** (4xx/5xx):
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional error details"
    }
  }
}
```

### Common Error Codes

- `AUTHENTICATION_REQUIRED`: Missing or invalid token
- `AUTHORIZATION_DENIED`: User doesn't have permission
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `VALIDATION_ERROR`: Request validation failed
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `BUSINESS_RULE_VIOLATION`: Violates business logic
- `INTERNAL_ERROR`: Server error

### Example Error Response

**Response** (400):
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "target_alumni_id": "Alumni not found or not available",
      "request_type": "Invalid request type"
    }
  }
}
```

---

## Rate Limiting

Rate limits are applied per user:
- **Authentication**: 5 requests per minute
- **Read endpoints**: 100 requests per minute
- **Write endpoints**: 20 requests per minute
- **Discovery/Search**: 30 requests per minute

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

---

## API Versioning Strategy

- Current version: `v1`
- Version specified in URL path: `/api/v1/...`
- Breaking changes require new version
- Non-breaking changes (new fields, new endpoints) can be added to current version
- Deprecation: Announce 6 months before removal, maintain for 12 months

---

## Webhooks (Future)

For future integrations, webhook support:

### POST /api/v1/webhooks
Register webhook endpoint.

**Request**:
```json
{
  "url": "https://example.com/webhook",
  "events": ["request.approved", "introduction.created", "outcome.recorded"]
}
```

### Webhook Payload Format
```json
{
  "event": "request.approved",
  "timestamp": "2024-01-15T10:00:00Z",
  "data": {
    "request_id": "uuid",
    "student_id": "uuid",
    "alumni_id": "uuid"
  }
}
```

---

## OpenAPI/Swagger Specification

A complete OpenAPI 3.0 specification should be generated from this design and maintained alongside the codebase for:
- API documentation
- Client SDK generation
- Testing and validation

