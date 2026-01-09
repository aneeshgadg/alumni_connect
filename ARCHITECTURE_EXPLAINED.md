# Architecture Explanation: Student vs Alumni Mapping

## Current Architecture Overview

### Data Model Structure

```
User (Base Entity)
├── id (UUID)
├── email
├── password_hash
├── role (student | alumni)  ← This determines the domain
└── university_id

Student Profile (extends User)
└── id (references User.id)
└── graduation_year, major, career_interests, etc.

Alumni Profile (extends User)
└── id (references User.id)
└── current_role, current_company, industry, etc.
```

### How Role-Based Routing Works

#### 1. **Registration Flow** (Current Implementation)

**Frontend:**
- User selects "I am a Student" or "I am an Alumni" in registration form
- Sends `role: "student"` or `role: "alumni"` to backend

**Backend:**
- `/api/v1/auth/register` endpoint receives the role
- Creates `User` record with `role` field set
- **Currently Missing**: Should also create `Student` or `Alumni` profile

#### 2. **API Domain Separation**

The architecture uses **separate API endpoints** for Student and Alumni domains:

**Student Endpoints:**
- `GET /api/v1/students/me` - Get student profile
- `PUT /api/v1/students/me` - Update student profile
- `GET /api/v1/students/discover` - Find alumni
- `POST /api/v1/students/requests` - Create introduction request

**Alumni Endpoints:**
- `GET /api/v1/alumni/me` - Get alumni profile
- `PUT /api/v1/alumni/me` - Update alumni profile
- `GET /api/v1/alumni/me/requests` - View pending requests
- `POST /api/v1/alumni/requests/{id}/approve` - Approve request

#### 3. **How Frontend Routes Based on Role**

**After Login:**
1. Frontend receives JWT token with `role` in payload
2. Checks `user.role` from auth context
3. Routes to appropriate dashboard:
   - If `role === "student"` → `/students/dashboard`
   - If `role === "alumni"` → `/alumni/dashboard`

**API Calls:**
- Frontend checks `user.role` from auth context
- Makes API calls to appropriate domain:
   ```typescript
   if (user.role === 'student') {
     // Call /api/v1/students/* endpoints
   } else if (user.role === 'alumni') {
     // Call /api/v1/alumni/* endpoints
   }
   ```

#### 4. **Backend Authorization**

**Middleware/Depends:**
- `get_current_user()` extracts user from JWT token
- Checks `user.role` to authorize access
- Student endpoints verify `current_user.role == "student"`
- Alumni endpoints verify `current_user.role == "alumni"`

## Current Gap: Profile Creation

**Problem:** Registration only creates `User`, not `Student` or `Alumni` profile.

**Solution Needed:**
After creating `User`, we should:
1. Check `user.role`
2. If `role == "student"`: Create `Student` profile
3. If `role == "alumni"`: Create `Alumni` profile

## Flow Diagram

```
Registration:
┌─────────────┐
│   Frontend   │
│  (Register)  │
└──────┬───────┘
       │ POST /api/v1/auth/register
       │ { role: "student", email, password, ... }
       ▼
┌─────────────────────┐
│   Auth Endpoint     │
│  /auth/register     │
└──────┬──────────────┘
       │
       ├─→ Create User (role = "student")
       │
       ├─→ Create Student Profile (id = user.id)
       │
       └─→ Return UserResponse

Login:
┌─────────────┐
│   Frontend   │
│   (Login)    │
└──────┬───────┘
       │ POST /api/v1/auth/login
       │ { email, password }
       ▼
┌─────────────────────┐
│   Auth Endpoint     │
│   /auth/login       │
└──────┬──────────────┘
       │
       ├─→ Verify credentials
       ├─→ Create JWT (includes role)
       └─→ Return { access_token, user: { role: "student" } }

After Login - Profile Access:
┌─────────────┐
│   Frontend   │
│ (Dashboard) │
└──────┬───────┘
       │
       ├─→ Check user.role
       │
       ├─→ If "student":
       │   GET /api/v1/students/me
       │   └─→ Backend checks role, returns Student profile
       │
       └─→ If "alumni":
           GET /api/v1/alumni/me
           └─→ Backend checks role, returns Alumni profile
```

## Key Points

1. **Role is set at registration** - User selects student/alumni
2. **Role is stored in User table** - Single source of truth
3. **Role determines API domain** - Different endpoints for each role
4. **JWT token includes role** - Frontend knows which endpoints to call
5. **Backend validates role** - Endpoints check role matches before allowing access

## Next Steps

We need to:
1. ✅ Update registration to create Student/Alumni profile
2. ✅ Create separate Student and Alumni API endpoints
3. ✅ Add role-based authorization middleware
4. ✅ Update frontend to route based on role
