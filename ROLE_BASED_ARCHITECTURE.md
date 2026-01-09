# Role-Based Architecture: How Student/Alumni Mapping Works

## Overview

The platform uses **role-based domain separation** where the role selected during registration determines:
1. Which profile type is created (Student or Alumni)
2. Which API endpoints the user can access
3. Which UI/dashboard they see
4. What actions they can perform

## Registration Flow

### Step 1: User Selects Role
**Frontend (`/register`):**
```typescript
// User selects "I am a Student" or "I am an Alumni"
role: "student" | "alumni"
```

### Step 2: Backend Creates User + Profile
**Backend (`POST /api/v1/auth/register`):**

```python
# 1. Create User record
user = User(
    role=user_data.role,  # "student" or "alumni"
    email=user_data.email,
    password_hash=hash(password),
    ...
)

# 2. Create corresponding profile based on role
if role == "student":
    Student(id=user.id, ...)  # Creates Student profile
elif role == "alumni":
    Alumni(id=user.id, ...)   # Creates Alumni profile
```

**Key Point:** The role selected in the registration form determines which profile type is created.

## API Domain Separation

### Separate Endpoints by Role

**Student Domain:**
- `GET /api/v1/students/me` - Get student profile
- `PUT /api/v1/students/me` - Update student profile
- `GET /api/v1/students/discover` - Find alumni
- `POST /api/v1/students/requests` - Create introduction request

**Alumni Domain:**
- `GET /api/v1/alumni/me` - Get alumni profile
- `PUT /api/v1/alumni/me` - Update alumni profile
- `GET /api/v1/alumni/me/requests` - View pending requests
- `POST /api/v1/alumni/requests/{id}/approve` - Approve request

### How Frontend Routes API Calls

**After Login:**
```typescript
// 1. Get user from auth context
const { user } = useAuth()
// user = { id: "...", email: "...", role: "student" }

// 2. Route API calls based on role
if (user.role === 'student') {
  // Call student endpoints
  const profile = await apiClient.get('/students/me')
  const alumni = await apiClient.get('/students/discover')
} else if (user.role === 'alumni') {
  // Call alumni endpoints
  const profile = await apiClient.get('/alumni/me')
  const requests = await apiClient.get('/alumni/me/requests')
}
```

**Key Point:** Frontend checks `user.role` from JWT token and calls the appropriate domain endpoints.

## Backend Authorization

### Role-Based Access Control

**Student Endpoints:**
```python
@router.get("/students/me")
async def get_student_profile(
    current_user: User = Depends(get_current_user)
):
    # Verify user is a student
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(403, "Access denied")
    
    # Return student profile
    student = db.query(Student).filter(Student.id == current_user.id).first()
    return student
```

**Alumni Endpoints:**
```python
@router.get("/alumni/me")
async def get_alumni_profile(
    current_user: User = Depends(get_current_user)
):
    # Verify user is an alumni
    if current_user.role != UserRole.ALUMNI:
        raise HTTPException(403, "Access denied")
    
    # Return alumni profile
    alumni = db.query(Alumni).filter(Alumni.id == current_user.id).first()
    return alumni
```

**Key Point:** Backend validates that the user's role matches the endpoint domain before allowing access.

## Complete Flow Example

### Registration → Login → Dashboard

```
1. REGISTRATION
   Frontend: User selects "Student" → POST /auth/register { role: "student" }
   Backend: Creates User + Student profile
   Response: { user: { role: "student" } }

2. LOGIN
   Frontend: POST /auth/login { email, password }
   Backend: Returns JWT with role in payload
   Response: { access_token, user: { role: "student" } }

3. DASHBOARD ROUTING
   Frontend: Checks user.role
   - If "student" → Route to /students/dashboard
   - If "alumni" → Route to /alumni/dashboard

4. PROFILE ACCESS
   Frontend: GET /api/v1/students/me (if student)
   Backend: 
     - Extract user from JWT
     - Verify role == "student"
     - Return Student profile
```

## Data Model Relationship

```
User Table:
├── id: uuid
├── email: string
├── role: "student" | "alumni"  ← Single source of truth
└── university_id: uuid

Student Table:
└── id: uuid (FK → User.id)  ← One-to-one with User

Alumni Table:
└── id: uuid (FK → User.id)  ← One-to-one with User
```

**Important:** 
- Each User has EITHER a Student profile OR an Alumni profile (never both)
- The `role` field in User table determines which profile exists
- Profile `id` matches User `id` (one-to-one relationship)

## Summary

**How mapping works:**

1. **Registration:** Role selection → Creates User + corresponding profile (Student or Alumni)
2. **Login:** Returns JWT with role → Frontend knows which domain to use
3. **API Calls:** Frontend checks role → Calls appropriate domain endpoints (`/students/*` or `/alumni/*`)
4. **Authorization:** Backend validates role → Ensures user can only access their domain endpoints

**The role selected at registration determines everything** - it's not just a UI choice, it's a fundamental architectural decision that affects:
- Database structure (which profile table)
- API routing (which endpoints)
- UI flow (which dashboard)
- Permissions (what actions allowed)
