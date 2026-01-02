# Sequence Diagrams - Key System Flows

## Flow 1: Student Creates Introduction Request

```
Student          Student API      Request Service    Matching Service    Notification Service    Alumni
  |                    |                 |                  |                      |              |
  |--POST /requests--->|                 |                  |                      |              |
  |                    |--validate------>|                  |                      |              |
  |                    |                 |--check eligibility|                      |              |
  |                    |                 |--get context----->|                      |              |
  |                    |                 |<--shared context--|                      |              |
  |                    |                 |--create request---|                      |              |
  |                    |                 |--notify---------->|                      |              |
  |                    |                 |                   |                      |--email------>|
  |                    |<--201 Created---|                   |                      |              |
  |<--request created--|                 |                   |                      |              |
```

## Flow 2: Alumni Approves Request & Creates Introduction

```
Alumni          Alumni API       Request Service    Introduction Service    Template Service    Notification Service    Student
  |                  |                 |                      |                    |                      |              |
  |--GET /requests--->|                 |                      |                    |                      |              |
  |<--pending list----|                 |                      |                    |                      |              |
  |                  |                 |                      |                    |                      |              |
  |--POST /approve--->|                 |                      |                    |                      |              |
  |                  |--approve-------->|                      |                    |                      |              |
  |                  |                 |--create intro-------->|                    |                      |              |
  |                  |                 |                      |--generate template->|                    |              |
  |                  |                 |                      |<--template----------|                    |              |
  |                  |                 |<--introduction--------|                    |                      |              |
  |                  |                 |--notify------------->|                    |                      |              |
  |                  |                 |                      |                    |--email-------------->|
  |<--introduction----|                 |                      |                    |                      |              |
  |   with template   |                 |                      |                    |                      |              |
```

## Flow 3: Alumni Delivers Introduction

```
Alumni          Alumni API       Introduction Service    Notification Service    Student    Email Service
  |                  |                      |                      |              |              |
  |--POST /deliver--->|                      |                      |              |              |
  |   (review/edit)   |                      |                      |              |              |
  |                  |--deliver------------->|                      |              |              |
  |                  |                      |--send email---------->|              |              |
  |                  |                      |                      |              |--email------->|
  |                  |                      |--mark active---------|              |              |
  |                  |                      |--notify student------|              |              |
  |                  |                      |                      |--email------->|              |
  |<--delivered-------|                      |                      |              |              |
```

## Flow 4: Outcome Tracking

```
Student         Student API      Outcome Service    Analytics Service    Introduction Service
  |                  |                  |                   |                      |
  |--POST /outcomes-->|                  |                   |                      |              |
  |                  |--record--------->|                   |                      |              |
  |                  |                  |--validate-------->|                      |              |
  |                  |                  |--log event--------|                      |              |
  |                  |                  |                   |--update metrics------|              |
  |                  |                  |--update intro------|                      |              |
  |                  |                  |                   |                      |--mark completed
  |<--outcome saved--|                  |                   |                      |              |
```

## Flow 5: Student Discovery (Finding Relevant Alumni)

```
Student         Student API      Matching Service    Profile Service    Context Discovery    Alumni Repository
  |                  |                  |                   |                      |                      |
  |--GET /discover--->|                  |                   |                      |                      |
  |                  |--get profile----->|                   |                      |                      |
  |                  |                  |<--student profile--|                      |                      |
  |                  |                  |--find alumni------>|                      |                      |
  |                  |                  |                   |                      |--query-------------->|
  |                  |                  |                   |                      |<--alumni list--------|
  |                  |                  |--discover context->|                      |                      |
  |                  |                  |                   |<--shared context------|                      |
  |                  |                  |--rank & filter----|                      |                      |
  |                  |<--alumni list----|                   |                      |                      |
  |<--discovery-------|                  |                   |                      |                      |
```

## Flow 6: Request Quality Validation (Future ML Integration Point)

```
Request Service    Request Validator    Quality Scorer (Future ML)    Template Service    Profile Service
       |                   |                         |                        |                  |
       |--validate--------->|                         |                        |                  |
       |                   |--check completeness----->|                        |                  |
       |                   |                          |--get student profile-->|                  |
       |                   |                          |<--profile data--------|                  |
       |                   |                          |--score quality-------->|                  |
       |                   |                          |<--quality score-------|                  |
       |                   |<--validation result-----|                        |                  |
       |<--validated-------|                          |                        |                  |
```

## Flow 7: Multi-University Isolation (Tenant Separation)

```
Student          Student API      IAM Service        University Service    Database (with tenant filter)
  |                   |                 |                     |                          |
  |--GET /me---------->|                 |                     |                          |
  |                   |--get user-------->|                     |                          |
  |                   |                  |--get university_id-->|                          |
  |                   |                  |<--university_id------|                          |
  |                   |--query profile-->|                     |                          |
  |                   |                  |                     |--filter by tenant-------->|
  |                   |                  |                     |<--tenant-scoped data-----|
  |<--profile data----|                  |                     |                          |
```

## Flow 8: Feedback Loop - Outcome to Matching Improvement (Future)

```
Outcome Service    Analytics Service    Feature Store    ML Matching Service    Matching Service
       |                   |                  |                    |                    |
       |--log outcome------>|                  |                    |                    |
       |                   |--aggregate-------->|                    |                    |
       |                   |                    |--compute features-->|                    |                    |
       |                   |                    |<--features----------|                    |                    |
       |                   |                    |--update model------>|                    |                    |
       |                   |                    |                    |--update weights----->|                    |
       |                   |                    |                    |<--new weights--------|                    |
       |                   |                    |                    |                      |--apply new matching
```

## Flow 9: Alumni Availability Management

```
Alumni          Alumni API       Profile Service    Matching Service    Request Router
  |                  |                   |                  |                  |
  |--PUT /me--------->|                   |                  |                  |
  |  (availability)   |                   |                  |                  |
  |                  |--update profile---->|                  |                  |
  |                  |                    |--update discovery->|                  |                  |
  |                  |                    |                   |--re-rank-------->|                  |
  |                  |                    |                   |                  |--filter requests
  |<--updated--------|                    |                   |                  |
```

## Flow 10: Request Expiration & Cleanup

```
Scheduler      Request Service    Notification Service    Student
    |                 |                      |              |
    |--check expired->|                      |              |
    |                 |--find expired--------|              |
    |                 |--mark expired--------|              |
    |                 |--notify------------->|              |
    |                 |                      |--email------->|
    |                 |                      |              |
```

## Key Interaction Patterns

### Synchronous Operations
- Request creation
- Request approval/decline
- Introduction delivery
- Outcome recording
- Profile updates

### Asynchronous Operations (Future)
- Email notifications (can be queued)
- Event logging (can be queued)
- Analytics aggregation (can be batched)
- ML model updates (can be scheduled)

### Event-Driven Operations (Future)
- Outcome recorded → Update reputation scores
- Request approved → Create introduction
- Introduction delivered → Start outcome tracking timer
- Profile updated → Update matching indexes

---

## Error Handling Flows

### Flow: Request Validation Failure

```
Student         Student API      Request Service    Validation Service
  |                  |                 |                    |
  |--POST /request--->|                 |                    |
  |                  |--validate------->|                    |
  |                  |                  |--check rules------>|
  |                  |                  |<--validation error--|
  |                  |<--400 Bad Request|                    |
  |<--error details--|                 |                    |
```

### Flow: Alumni Unavailable

```
Student         Student API      Request Service    Alumni Repository
  |                  |                 |                    |
  |--POST /request--->|                 |                    |
  |                  |--validate------->|                    |
  |                  |                  |--check availability->|
  |                  |                  |<--unavailable---------|
  |                  |<--403 Forbidden |                    |
  |<--error: unavailable|              |                    |
```

---

## Notes on Implementation

1. **Service Boundaries**: Each service should be independently deployable
2. **Database Transactions**: Use transactions for multi-step operations (e.g., approve request + create introduction)
3. **Idempotency**: All write operations should be idempotent (use unique constraints, check-and-set patterns)
4. **Caching**: Discovery and matching results can be cached (with appropriate invalidation)
5. **Retry Logic**: External services (email, notifications) should have retry logic with exponential backoff

