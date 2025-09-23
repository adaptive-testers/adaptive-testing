# Authentication Backend Setup

## What's Ready
- ✅ Custom User model with email-based auth
- ✅ User roles (student/instructor/admin)
- ✅ JWT token endpoints
- ✅ Admin interface
- ✅ OAuth fields ready for implementation

## TODO for Team
1. **Traditional Auth** - Implement registration, login, profile views
2. **Serializers** - Create user serializers
3. **OAuth** - Implement Google/Microsoft OAuth (separate task)

## Endpoints to Implement
- POST /api/auth/register/
- POST /api/auth/login/
- POST /api/auth/logout/
- GET/PUT /api/auth/profile/
- POST /api/auth/password/change/
- POST /api/auth/password/reset/
- POST /api/auth/verify-email/

## Testing
- Run: `poetry run pytest`
- Admin: http://127.0.0.1:8000/admin/