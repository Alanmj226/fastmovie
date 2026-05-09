# =============================================
# FAST MOVIE - Email & OTP Configuration
# =============================================
#
# HOW TO ENABLE GMAIL OTP (EMAIL):
# ----------------------------------
# 1. Open: https://myaccount.google.com/apppasswords
#    (You MUST have 2-Step Verification enabled on your Google account)
# 2. Under "Select app" choose "Mail"
# 3. Under "Select device" choose "Other" → type "Fast Movie"
# 4. Click "Generate" → copy the 16-character password
# 5. Paste your Gmail and that App Password below
#
# HOW TO ENABLE SMS OTP (PHONE):
# ----------------------------------
# SMS is sent via carrier email-to-SMS gateways (FREE, no API needed).
# The user selects their carrier on the login page.
# Make sure SMTP_EMAIL and SMTP_PASSWORD are configured above first.
# Note: Indian carriers (Jio, Airtel, Vi) have limited gateway support.
#       For best results, use EMAIL mode instead.
#
# =============================================

SMTP_EMAIL    = "rh8709088@gmail.com"    # ✅ Your sender Gmail
SMTP_PASSWORD = "vwnuwowtohsksxnf"   # ✅ Gmail App Password (16 chars, no spaces)
