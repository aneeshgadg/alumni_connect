# Fixing Supabase Database Connection

## The Problem

The error `could not translate host name "db.puagnvhdsqvfwsqgtcrb.supabase.co"` means your computer can't resolve the Supabase hostname. This could be due to:

1. **Network/DNS issues**
2. **Supabase project paused** (free tier projects pause after inactivity)
3. **Wrong connection string format**
4. **Need to use connection pooler**

## Solutions

### Solution 1: Check if Supabase Project is Active

1. Go to [Supabase Dashboard](https://app.supabase.com/)
2. Check if your project shows as "Paused" or "Inactive"
3. If paused, click "Restore" to wake it up
4. Wait 1-2 minutes for it to fully start

### Solution 2: Use Connection Pooler (Recommended)

The connection pooler is more reliable and handles connections better:

1. **Go to Supabase Dashboard** → Your Project → **Project Settings** → **Database**
2. **Find "Connection Pooling"** section
3. **Copy the "Connection string"** (URI format)
4. It will look like:
   ```
   postgresql://postgres.xxxxx:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
5. **Update your `.env` file**:
   ```env
   DATABASE_URL="postgresql://postgres.xxxxx:your-password@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
   ```

### Solution 3: Verify Connection String Format

Make sure your `DATABASE_URL` in `.env` is exactly:

```env
DATABASE_URL="postgresql://postgres:your-password@db.puagnvhdsqvfwsqgtcrb.supabase.co:5432/postgres"
```

**Important:**
- Use double quotes around the entire URL
- Replace `your-password` with your actual password
- If password has special characters, URL-encode them OR use `%%` to escape `%`

### Solution 4: Test Connection Manually

Test if you can reach Supabase:

```bash
# Test DNS resolution
nslookup db.puagnvhdsqvfwsqgtcrb.supabase.co

# Test connection (if psql is installed)
psql "postgresql://postgres:your-password@db.puagnvhdsqvfwsqgtcrb.supabase.co:5432/postgres"
```

### Solution 5: Check Network/Firewall

- Make sure you're connected to the internet
- Check if any VPN/firewall is blocking the connection
- Try from a different network

## Quick Fix Steps

1. **Check Supabase Dashboard** - Make sure project is active
2. **Get Connection Pooler URL** - More reliable than direct connection
3. **Update `.env`** with pooler URL in quotes
4. **Try migration again**

## Recommended: Use Connection Pooler

The connection pooler is better because:
- More reliable connections
- Better for production
- Handles special characters better
- Less likely to have DNS issues

Get it from: **Supabase Dashboard** → **Project Settings** → **Database** → **Connection Pooling** → **Connection string**

