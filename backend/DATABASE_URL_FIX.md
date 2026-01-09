# Fixing DATABASE_URL Format

## The Problem

You're getting a `ValueError: invalid interpolation syntax` error. This happens when:
1. Your password contains special characters (like `@`)
2. The config parser tries to interpret URL-encoded characters

## Solution

### Option 1: Use Raw String in .env (Recommended)

In your `backend/.env` file, wrap the DATABASE_URL in quotes:

```env
DATABASE_URL="postgresql://postgres:dipti%40hoboken22@db.puagnvhdsqvfwsqgtcrb.supabase.co:5432/postgres"
```

The quotes tell the parser to treat it as a literal string.

### Option 2: Double the % Sign

If quotes don't work, try escaping the `%`:

```env
DATABASE_URL=postgresql://postgres:dipti%%40hoboken22@db.puagnvhdsqvfwsqgtcrb.supabase.co:5432/postgres
```

### Option 3: Use Connection Pooler (Best for Production)

Supabase provides a connection pooler that's more reliable:

1. Go to Supabase Dashboard → Project Settings → Database
2. Find the **Connection Pooling** section
3. Copy the **Connection string** (URI format)
4. It will look like:
   ```
   postgresql://postgres.xxxxx:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

The pooler URL often handles special characters better.

## Quick Fix Steps

1. **Open** `backend/.env`
2. **Find** the `DATABASE_URL` line
3. **Wrap it in double quotes**:
   ```env
   DATABASE_URL="postgresql://postgres:dipti%40hoboken22@db.puagnvhdsqvfwsqgtcrb.supabase.co:5432/postgres"
   ```
4. **Save** the file
5. **Try the migration again**:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

## Alternative: Change Your Database Password

If the above doesn't work, you can change your Supabase database password to one without special characters:

1. Go to Supabase Dashboard → Project Settings → Database
2. Click "Reset database password"
3. Choose a password without `@`, `#`, `$`, `%` characters
4. Update your `.env` with the new password (no URL encoding needed)

## Testing

After fixing, test the connection:
```bash
python -c "from app.core.config import settings; print('Database URL loaded:', settings.DATABASE_URL[:50] + '...')"
```

This should print the first 50 characters without errors.
