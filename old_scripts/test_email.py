"""
Fast Movie - Quick Email OTP Test
Run this to check if your Gmail config is working.
Usage: python test_email.py
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from email_config import SMTP_EMAIL, SMTP_PASSWORD
except ImportError:
    print("❌ email_config.py not found!")
    exit()

# ── Change this to the email you want to receive the test OTP ──
TEST_SEND_TO = "rh8709088@gmail.com"   # ← change to your personal Gmail to receive test
TEST_OTP     = "123456"
TEST_NAME    = "Alan"
# ──────────────────────────────────────────────────────────────

print(f"\n{'='*50}")
print(f"  Fast Movie - Email OTP Test")
print(f"{'='*50}")
print(f"  Sender  : {SMTP_EMAIL}")
print(f"  Send To : {TEST_SEND_TO}")
print(f"  OTP     : {TEST_OTP}")
print(f"{'='*50}\n")

if SMTP_EMAIL == "your_gmail@gmail.com":
    print("❌ email_config.py not configured! Please set SMTP_EMAIL and SMTP_PASSWORD.")
    exit()

try:
    print("🔄 Connecting to Gmail SMTP...")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'Your Fast Movie OTP: {TEST_OTP}'
    msg['From']    = f'Fast Movie <{SMTP_EMAIL}>'
    msg['To']      = TEST_SEND_TO

    html = f"""
    <html><body style="margin:0;padding:0;background:#0f1014;font-family:'Segoe UI',sans-serif;">
      <div style="max-width:480px;margin:40px auto;background:#181a22;border-radius:16px;
                  box-shadow:0 8px 32px rgba(0,0,0,0.6);overflow:hidden;">
        <div style="background:linear-gradient(135deg,#1f80e0,#00d2ff);padding:30px;text-align:center;">
          <h1 style="color:#fff;margin:0;font-size:26px;">⚡ Fast Movie</h1>
        </div>
        <div style="padding:36px 32px;">
          <p style="color:#ccc;font-size:16px;margin-top:0;">Hi <strong style="color:#fff;">{TEST_NAME}</strong>,</p>
          <p style="color:#aaa;font-size:15px;">Your One-Time Password is:</p>
          <div style="background:#0f1014;border:2px solid #1f80e0;border-radius:12px;
                      text-align:center;padding:20px;margin:24px 0;">
            <span style="font-size:40px;font-weight:900;letter-spacing:14px;color:#00d2ff;">{TEST_OTP}</span>
          </div>
          <p style="color:#888;font-size:13px;margin:0;">⏳ Valid for <strong style="color:#fff;">10 minutes</strong>.</p>
        </div>
        <div style="background:#111318;padding:18px;text-align:center;">
          <p style="color:#555;font-size:12px;margin:0;">© 2025 Fast Movie · TEST EMAIL</p>
        </div>
      </div>
    </body></html>"""

    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, TEST_SEND_TO, msg.as_string())

    print(f"✅ SUCCESS! Test OTP email sent to: {TEST_SEND_TO}")
    print(f"   Check your inbox for the Fast Movie email!\n")

except smtplib.SMTPAuthenticationError:
    print("❌ AUTHENTICATION FAILED!")
    print("   → Make sure 2-Step Verification is ON for rh8709088@gmail.com")
    print("   → Make sure the App Password in email_config.py is correct\n")

except smtplib.SMTPException as e:
    print(f"❌ SMTP Error: {e}\n")

except Exception as e:
    print(f"❌ Error: {e}\n")
