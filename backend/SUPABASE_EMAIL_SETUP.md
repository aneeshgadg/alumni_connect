# Supabase Email Setup Guide

This guide walks you through setting up email sending using Supabase's SMTP configuration.

## Step 1: Access Supabase Dashboard

1. Go to [Supabase Dashboard](https://app.supabase.com/)
2. Select your project

## Step 2: Configure SMTP Settings

Supabase provides SMTP settings for sending emails. You have two options:

### Option A: Use Supabase's Default Email Service (Development/Testing)

Supabase has a built-in email service, but it's primarily for their Auth system. For custom emails, you'll need to configure custom SMTP.

### Option B: Configure Custom SMTP (Recommended)

1. **Navigate to Authentication Settings:**
   - In your Supabase Dashboard, go to **Authentication** → **Settings**
   - Scroll down to **Email** section

2. **Enable Custom SMTP:**
   - Toggle on **Custom SMTP**
   - You'll need to provide SMTP credentials

3. **Get SMTP Credentials:**
   
   **Option 1: Use Supabase's SMTP (if available)**
   - Check if Supabase provides SMTP credentials in your project settings
   - Look for SMTP configuration in **Project Settings** → **API** or **Settings**
   
   **Option 2: Use a Third-Party SMTP Service**
   - **Resend** (Recommended - works great with Supabase)
     - Sign up at [resend.com](https://resend.com)
     - Free tier: 3,000 emails/month
     - Get API key from dashboard
   - **SendGrid** (Alternative)
     - Sign up at [sendgrid.com](https://sendgrid.com)
     - Free tier: 100 emails/day
     - Get API key from dashboard

## Step 3: Add SMTP Credentials to .env

Add these to your `backend/.env` file:

### If using Resend (Recommended):
```env
SMTP_HOST=smtp.resend.com
SMTP_PORT=587
SMTP_USER=resend
SMTP_PASSWORD=your-resend-api-key-here
EMAIL_FROM=noreply@yourdomain.com
```

### If using SendGrid:
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key-here
EMAIL_FROM=noreply@yourdomain.com
```

### If using Supabase's SMTP (if available):
```env
SMTP_HOST=[from-supabase-dashboard]
SMTP_PORT=587
SMTP_USER=[from-supabase-dashboard]
SMTP_PASSWORD=[from-supabase-dashboard]
EMAIL_FROM=noreply@yourdomain.com
```

## Step 4: Verify Email Domain (Production)

For production, you'll need to:
1. Verify your email domain with your SMTP provider
2. Set up SPF/DKIM records for better deliverability
3. Use a verified "from" email address

## Step 5: Test Email Sending

Once configured, test by:
1. Running your backend
2. Triggering a registration or password reset
3. Check your email inbox (and spam folder)

## Troubleshooting

### Emails not sending?
- Check SMTP credentials are correct
- Verify SMTP port (587 for TLS, 465 for SSL)
- Check firewall/network restrictions
- Review SMTP provider logs

### Emails going to spam?
- Verify your domain with SPF/DKIM
- Use a verified sender email
- Avoid spam trigger words in subject/body

## Recommended: Resend Setup

Resend is popular with Supabase users and easy to set up:

1. **Sign up**: [resend.com](https://resend.com)
2. **Get API key**: Dashboard → API Keys
3. **Add to .env**:
   ```env
   SMTP_HOST=smtp.resend.com
   SMTP_PORT=587
   SMTP_USER=resend
   SMTP_PASSWORD=re_your_api_key_here
   EMAIL_FROM=onboarding@resend.dev  # Use their test domain first
   ```
4. **Verify domain** (for production): Add DNS records in Resend dashboard


