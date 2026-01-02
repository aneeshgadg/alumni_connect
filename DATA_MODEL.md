# Data Model Specification

## Entity Relationship Overview

```
┌─────────────┐
│    User     │ (Abstract Base)
│  (IAM)      │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──┴──┐ ┌──┴───┐
│Student│ │Alumni│
└───┬──┘ └───┬──┘
    │        │
    │        │
    └───┬────┘
        │
┌───────┴────────┐
│Introduction    │
│   Request      │
└───────┬────────┘
        │
        │ (if approved)
        │
┌───────┴────────┐
│ Introduction   │
└───────┬────────┘
        │
        │ (one or more)
        │
┌───────┴────────┐
│    Outcome     │
└────────────────┘

┌─────────────┐
│   Shared    │ (Many-to-Many)
│   Context   │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──┴──┐ ┌──┴───┐
│Student│ │Alumni│
└───────┘ └──────┘
```

## Detailed Entity Specifications

### User (Base Entity)
**Purpose**: Common authentication and identity information

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| university_id | UUID | FK, NOT NULL | Multi-tenant isolation |
| email | String(255) | UNIQUE, NOT NULL | Authentication email |
| password_hash | String(255) | NOT NULL | Encrypted password |
| role | Enum | NOT NULL | 'student' or 'alumni' |
| status | Enum | NOT NULL | 'active', 'inactive', 'suspended' |
| created_at | Timestamp | NOT NULL | Account creation time |
| updated_at | Timestamp | NOT NULL | Last update time |
| last_login_at | Timestamp | NULL | Last authentication time |

**Indexes**:
- `idx_user_email` on `email`
- `idx_user_university_role` on `(university_id, role)`

---

### Student
**Purpose**: Student-specific profile and tracking data

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, FK → User.id | References User |
| graduation_year | Integer | NOT NULL | Expected graduation year |
| major | String(100) | NULL | Primary field of study |
| secondary_major | String(100) | NULL | Optional second major |
| career_interests | JSONB | NOT NULL | Array of interest objects |
| current_location | String(100) | NULL | Geographic location |
| preferred_locations | JSONB | NULL | Array of preferred locations |
| target_companies | JSONB | NULL | Companies of interest |
| target_roles | JSONB | NULL | Role types of interest |
| target_industries | JSONB | NULL | Industries of interest |
| bio | Text | NULL | Optional personal statement |
| hobbies | JSONB | NULL | Array of hobbies and personal interests |
| interests | JSONB | NULL | Array of general interests (beyond career) |
| interesting_facts | JSONB | NULL | Array of interesting facts about the student |
| linkedin_url | String(255) | NULL | Optional LinkedIn profile |
| resume_url | String(255) | NULL | Optional resume link |
| reputation_score | Decimal(5,2) | DEFAULT 0.0 | Internal quality metric |
| total_requests | Integer | DEFAULT 0 | Total requests made |
| successful_introductions | Integer | DEFAULT 0 | Successful outcomes |
| created_at | Timestamp | NOT NULL | Profile creation |
| updated_at | Timestamp | NOT NULL | Last profile update |

**career_interests JSONB Structure**:
```json
[
  {
    "type": "industry",
    "value": "Technology",
    "priority": 1
  },
  {
    "type": "role",
    "value": "Software Engineer",
    "priority": 1
  },
  {
    "type": "location",
    "value": "San Francisco, CA",
    "priority": 2
  }
]
```

**hobbies JSONB Structure**:
```json
[
  "Rock climbing",
  "Photography",
  "Cooking",
  "Playing guitar"
]
```

**interests JSONB Structure**:
```json
[
  "Sustainable technology",
  "Startup ecosystem",
  "Travel",
  "Reading science fiction"
]
```

**interesting_facts JSONB Structure**:
```json
[
  "Studied abroad in Japan for a semester",
  "Published a research paper on machine learning",
  "Volunteer at local food bank",
  "Speak three languages fluently"
]
```

**Indexes**:
- `idx_student_graduation_year` on `graduation_year`
- `idx_student_major` on `major`
- `idx_student_career_interests` on `career_interests` (GIN index)
- `idx_student_hobbies` on `hobbies` (GIN index, for matching)
- `idx_student_interests` on `interests` (GIN index, for matching)
- `idx_student_reputation` on `reputation_score`

---

### Alumni
**Purpose**: Alumni-specific profile and availability data

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, FK → User.id | References User |
| graduation_year | Integer | NOT NULL | Year of graduation |
| degree | String(100) | NULL | Degree obtained |
| major | String(100) | NULL | Field of study |
| current_role | String(100) | NOT NULL | Job title |
| current_company | String(100) | NOT NULL | Employer |
| industry | String(100) | NOT NULL | Industry sector |
| location | String(100) | NULL | Geographic location |
| years_experience | Integer | NULL | Professional experience |
| previous_companies | JSONB | NULL | Career history |
| bio | Text | NULL | Optional professional summary |
| hobbies | JSONB | NULL | Array of hobbies and personal interests |
| interests | JSONB | NULL | Array of general interests (beyond career) |
| interesting_facts | JSONB | NULL | Array of interesting facts about the alumni |
| linkedin_url | String(255) | NULL | Optional LinkedIn profile |
| availability_status | Enum | NOT NULL | 'open', 'limited', 'closed' |
| request_preferences | JSONB | NULL | Types of requests accepted |
| max_requests_per_month | Integer | DEFAULT 5 | Rate limiting |
| current_month_requests | Integer | DEFAULT 0 | Current month counter |
| helpfulness_score | Decimal(5,2) | DEFAULT 0.0 | Internal quality metric |
| total_introductions | Integer | DEFAULT 0 | Total introductions made |
| response_rate | Decimal(5,2) | DEFAULT 0.0 | Approval rate |
| avg_response_time_hours | Decimal(8,2) | NULL | Average time to respond |
| created_at | Timestamp | NOT NULL | Profile creation |
| updated_at | Timestamp | NOT NULL | Last profile update |

**previous_companies JSONB Structure**:
```json
[
  {
    "company": "Company Name",
    "role": "Role Title",
    "start_date": "2020-01",
    "end_date": "2022-06"
  }
]
```

**request_preferences JSONB Structure**:
```json
{
  "informational_interview": true,
  "referral": true,
  "career_guidance": true,
  "mentorship": false
}
```

**hobbies JSONB Structure**:
```json
[
  "Rock climbing",
  "Photography",
  "Cooking",
  "Playing guitar"
]
```

**interests JSONB Structure**:
```json
[
  "Sustainable technology",
  "Startup ecosystem",
  "Travel",
  "Reading science fiction"
]
```

**interesting_facts JSONB Structure**:
```json
[
  "Studied abroad in Japan for a semester",
  "Published a research paper on machine learning",
  "Volunteer at local food bank",
  "Speak three languages fluently"
]
```

**Indexes**:
- `idx_alumni_industry` on `industry`
- `idx_alumni_company` on `current_company`
- `idx_alumni_location` on `location`
- `idx_alumni_availability` on `availability_status`
- `idx_alumni_helpfulness` on `helpfulness_score`
- `idx_alumni_career` on `(industry, current_role)` (composite)
- `idx_alumni_hobbies` on `hobbies` (GIN index, for matching)
- `idx_alumni_interests` on `interests` (GIN index, for matching)

---

### Introduction Request
**Purpose**: Structured requests from students to alumni

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| student_id | UUID | FK → Student.id, NOT NULL | Requestor |
| target_alumni_id | UUID | FK → Alumni.id, NOT NULL | Requested connection |
| request_type | Enum | NOT NULL | Type of request |
| context | JSONB | NOT NULL | Structured context data |
| message | Text | NOT NULL | Template-based message |
| status | Enum | NOT NULL | Current status |
| expires_at | Timestamp | NULL | Request expiration |
| approved_at | Timestamp | NULL | When approved |
| declined_at | Timestamp | NULL | When declined |
| decline_reason | Text | NULL | Optional decline reason |
| quality_score | Decimal(5,2) | NULL | Internal quality metric |
| created_at | Timestamp | NOT NULL | Request creation |
| updated_at | Timestamp | NOT NULL | Last update |

**request_type Enum Values**:
- `informational_interview`
- `referral`
- `career_guidance`
- `mentorship`
- `other`

**status Enum Values**:
- `draft` (student editing)
- `pending` (awaiting alumni response)
- `approved` (alumni approved)
- `declined` (alumni declined)
- `expired` (time limit reached)
- `cancelled` (student cancelled)

**context JSONB Structure**:
```json
{
  "shared_major": true,
  "shared_company_interest": true,
  "shared_location": false,
  "why_this_connection": "I'm interested in transitioning to product management...",
  "specific_ask": "I'd like to learn about your day-to-day responsibilities...",
  "timeline": "I'm applying in the next 2 months"
}
```

**Indexes**:
- `idx_request_student` on `student_id`
- `idx_request_alumni` on `target_alumni_id`
- `idx_request_status` on `status`
- `idx_request_type` on `request_type`
- `idx_request_created` on `created_at`
- `idx_request_expires` on `expires_at` (for cleanup jobs)

**Constraints**:
- `CHECK (status = 'approved' OR approved_at IS NULL)`
- `CHECK (status = 'declined' OR declined_at IS NULL)`
- `CHECK (expires_at IS NULL OR expires_at > created_at)`

---

### Introduction
**Purpose**: Actual connection between student and alumni

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| request_id | UUID | FK → IntroductionRequest.id, UNIQUE | Source request |
| student_id | UUID | FK → Student.id, NOT NULL | Student participant |
| alumni_id | UUID | FK → Alumni.id, NOT NULL | Alumni participant |
| introduction_method | Enum | NOT NULL | How connection was made |
| introduction_text | Text | NULL | Actual introduction message |
| introduced_at | Timestamp | NULL | When introduction occurred |
| status | Enum | NOT NULL | Current status |
| created_at | Timestamp | NOT NULL | Introduction creation |
| updated_at | Timestamp | NOT NULL | Last update |

**introduction_method Enum Values**:
- `platform_email` (system sent email)
- `platform_message` (in-platform message)
- `alumni_direct` (alumni sent directly)
- `other`

**status Enum Values**:
- `pending` (created, not yet delivered)
- `active` (delivered, awaiting outcome)
- `completed` (outcome recorded)
- `archived` (old, no longer active)

**Indexes**:
- `idx_intro_request` on `request_id`
- `idx_intro_student` on `student_id`
- `idx_intro_alumni` on `alumni_id`
- `idx_intro_status` on `status`
- `idx_intro_created` on `created_at`

---

### Outcome
**Purpose**: Track real-world results from introductions

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| introduction_id | UUID | FK → Introduction.id, NOT NULL | Related introduction |
| outcome_type | Enum | NOT NULL | Type of outcome |
| recorded_by | Enum | NOT NULL | Who recorded this |
| notes | Text | NULL | Optional context |
| occurred_at | Timestamp | NULL | When outcome happened |
| recorded_at | Timestamp | NOT NULL | When logged in system |
| student_satisfaction | Integer | NULL | 1-5 rating (if student recorded) |
| alumni_satisfaction | Integer | NULL | 1-5 rating (if alumni recorded) |

**outcome_type Enum Values**:
- `conversation_occurred` (meaningful discussion happened)
- `referral_made` (alumni provided referral)
- `follow_up_scheduled` (ongoing relationship)
- `no_response` (introduction didn't lead to connection)
- `declined` (alumni declined after introduction)
- `other`

**recorded_by Enum Values**:
- `student`
- `alumni`
- `system` (future: automated detection)

**Indexes**:
- `idx_outcome_introduction` on `introduction_id`
- `idx_outcome_type` on `outcome_type`
- `idx_outcome_recorded` on `recorded_at`
- `idx_outcome_occurred` on `occurred_at`

**Constraints**:
- `CHECK (student_satisfaction IS NULL OR (student_satisfaction >= 1 AND student_satisfaction <= 5))`
- `CHECK (alumni_satisfaction IS NULL OR (alumni_satisfaction >= 1 AND alumni_satisfaction <= 5))`

---

### Shared Context
**Purpose**: Discovered connections between students and alumni

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| student_id | UUID | FK → Student.id, NOT NULL | Student |
| alumni_id | UUID | FK → Alumni.id, NOT NULL | Alumni |
| context_type | Enum | NOT NULL | Type of shared context |
| context_value | String(255) | NULL | Specific value (e.g., company name) |
| strength | Decimal(5,2) | DEFAULT 1.0 | Relevance score (future ML) |
| discovered_at | Timestamp | NOT NULL | When context was identified |
| last_verified_at | Timestamp | NULL | When context was last verified |

**context_type Enum Values**:
- `same_major`
- `same_company_interest` (student interested in alumni's company)
- `same_location`
- `same_industry`
- `same_role_interest` (student interested in alumni's role)
- `graduation_proximity` (close graduation years)
- `shared_interest` (shared general interests)
- `shared_hobby` (shared hobbies or activities)
- `shared_personal_interest` (shared personal interests beyond career)

**Indexes**:
- `idx_context_student` on `student_id`
- `idx_context_alumni` on `alumni_id`
- `idx_context_type` on `context_type`
- `idx_context_strength` on `strength`
- `UNIQUE (student_id, alumni_id, context_type, context_value)`

---

### Event Log (Future Intelligence)
**Purpose**: Capture all system events for analytics and ML

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| event_type | String(50) | NOT NULL | Type of event |
| entity_type | String(50) | NOT NULL | Entity involved |
| entity_id | UUID | NOT NULL | Entity identifier |
| user_id | UUID | FK → User.id, NULL | User who triggered event |
| event_data | JSONB | NOT NULL | Event-specific data |
| timestamp | Timestamp | NOT NULL | When event occurred |

**event_type Examples**:
- `request_created`
- `request_approved`
- `request_declined`
- `introduction_created`
- `introduction_delivered`
- `outcome_recorded`
- `profile_updated`
- `search_performed`

**Indexes**:
- `idx_event_type` on `event_type`
- `idx_event_entity` on `(entity_type, entity_id)`
- `idx_event_user` on `user_id`
- `idx_event_timestamp` on `timestamp` (for time-series queries)

**Partitioning Strategy** (Future):
- Partition by month or quarter for scale
- Archive old partitions to cold storage

---

## Data Relationships Summary

### One-to-Many Relationships
- `User` → `Student` (1:1, inheritance)
- `User` → `Alumni` (1:1, inheritance)
- `Student` → `IntroductionRequest` (1:many)
- `Alumni` → `IntroductionRequest` (1:many, as target)
- `IntroductionRequest` → `Introduction` (1:1, if approved)
- `Introduction` → `Outcome` (1:many, multiple outcomes possible)

### Many-to-Many Relationships
- `Student` ↔ `Alumni` via `SharedContext` (many:many)
- `Student` ↔ `Alumni` via `Introduction` (many:many, through requests)

### Temporal Relationships
- All entities track `created_at` and `updated_at`
- Requests and introductions have expiration/status tracking
- Outcomes track both `occurred_at` and `recorded_at`

---

## Data Integrity Rules

1. **Cascade Deletes**: 
   - Deleting a User should cascade to Student/Alumni
   - Deleting an IntroductionRequest should delete related Introduction
   - Deleting an Introduction should NOT delete Outcomes (preserve history)

2. **Referential Integrity**:
   - All foreign keys must reference existing records
   - Soft deletes preferred over hard deletes (status fields)

3. **Business Rules**:
   - A student cannot create duplicate requests to the same alumni (within time window)
   - An introduction can only be created from an approved request
   - Outcomes can only be recorded for active or completed introductions

4. **Data Quality**:
   - Required fields must be non-null
   - Enums must use valid values
   - JSONB fields must conform to schema (application-level validation)

---

## Query Patterns & Optimization

### High-Frequency Queries

1. **Student Discovery** (Find relevant alumni):
   ```sql
   SELECT * FROM alumni 
   WHERE availability_status = 'open'
   AND industry IN (student_interests)
   AND id NOT IN (recent_requests)
   ORDER BY helpfulness_score DESC, shared_context_strength DESC
   LIMIT 20;
   ```

2. **Alumni Request Queue** (Pending requests):
   ```sql
   SELECT * FROM introduction_request
   WHERE target_alumni_id = ?
   AND status = 'pending'
   ORDER BY quality_score DESC, created_at ASC;
   ```

3. **Outcome Analytics** (Success metrics):
   ```sql
   SELECT outcome_type, COUNT(*), AVG(satisfaction)
   FROM outcome
   WHERE recorded_at >= ?
   GROUP BY outcome_type;
   ```

### Indexing Strategy
- Index all foreign keys
- Index frequently filtered columns (status, type, dates)
- Use GIN indexes for JSONB fields used in queries
- Composite indexes for common query patterns
- Partial indexes for filtered queries (e.g., active requests only)

---

## Data Migration Considerations

### Future Schema Changes
- Use migration framework (e.g., Alembic, Flyway)
- Version all schema changes
- Support rollback strategies
- Add new fields as nullable initially, backfill, then make required

### Multi-University Support
- `university_id` on User enables row-level security
- Consider separate schemas per university for strict isolation
- Or use `university_id` in all queries for logical separation

---

## Privacy & Compliance

### PII Handling
- Email addresses: Encrypted at rest
- Personal information: Minimal collection, explicit consent
- Profile data: User-controlled visibility

### Data Retention
- Active users: Full data retention
- Inactive users: Archive after X months
- Event logs: Retain for analytics, archive old data

### GDPR Considerations
- Right to access: Export user data
- Right to deletion: Soft delete with data anonymization
- Right to portability: JSON export of user data

