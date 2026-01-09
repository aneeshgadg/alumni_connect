"""
Email service for sending verification and password reset emails
"""

from typing import Optional
from app.core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
    
    def _send_email(self, to_email: str, subject: str, html_body: str, text_body: str = None) -> bool:
        """
        Send an email using SMTP
        
        Supports:
        - Resend (smtp.resend.com)
        - SendGrid (smtp.sendgrid.net)
        - Generic SMTP servers
        
        Returns True if successful, False otherwise
        """
        if not self.smtp_host or not self.smtp_user:
            # In development, just log instead of sending
            print(f"[EMAIL] Would send to {to_email}: {subject}")
            print(f"[EMAIL] Body: {html_body}")
            return True
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_from
            msg['To'] = to_email
            
            # Add both plain text and HTML versions
            if text_body:
                text_part = MIMEText(text_body, 'plain')
                msg.attach(text_part)
            
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Send email via SMTP
            # Use TLS for port 587, SSL for port 465
            if self.smtp_port == 465:
                # SSL connection
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            else:
                # TLS connection (default)
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
            
            # Authenticate
            server.login(self.smtp_user, self.smtp_password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            print(f"[EMAIL] Successfully sent email to {to_email}")
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"[EMAIL] Authentication error: {e}")
            return False
        except smtplib.SMTPException as e:
            print(f"[EMAIL] SMTP error: {e}")
            return False
        except Exception as e:
            print(f"[EMAIL] Error sending email: {e}")
            return False
    
    def send_verification_email(self, to_email: str, verification_token: str, user_name: Optional[str] = None) -> bool:
        """Send email verification email"""
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
        
        subject = "Verify your Alumni Connect account"
        html_body = f"""
        <html>
          <body>
            <h2>Welcome to Alumni Connect!</h2>
            <p>Hi {user_name or 'there'},</p>
            <p>Thank you for signing up. Please verify your email address by clicking the link below:</p>
            <p><a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
            <p>Or copy and paste this link into your browser:</p>
            <p>{verification_url}</p>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't create an account, you can safely ignore this email.</p>
          </body>
        </html>
        """
        
        text_body = f"""
        Welcome to Alumni Connect!
        
        Please verify your email address by visiting:
        {verification_url}
        
        This link will expire in 24 hours.
        """
        
        return self._send_email(to_email, subject, html_body, text_body)
    
    def send_password_reset_email(self, to_email: str, reset_token: str, user_name: Optional[str] = None) -> bool:
        """Send password reset email"""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        subject = "Reset your Alumni Connect password"
        html_body = f"""
        <html>
          <body>
            <h2>Password Reset Request</h2>
            <p>Hi {user_name or 'there'},</p>
            <p>You requested to reset your password. Click the link below to create a new password:</p>
            <p><a href="{reset_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
            <p>Or copy and paste this link into your browser:</p>
            <p>{reset_url}</p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request a password reset, you can safely ignore this email.</p>
          </body>
        </html>
        """
        
        text_body = f"""
        Password Reset Request
        
        Click the link below to reset your password:
        {reset_url}
        
        This link will expire in 1 hour.
        """
        
        return self._send_email(to_email, subject, html_body, text_body)


# Create singleton instance
email_service = EmailService()

