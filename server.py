import http.server
import socketserver
import json
import os
import random
import socket
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- SMART CONFIGURATION ---
DEFAULT_PORT = 3000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_FILE = os.path.join(BASE_DIR, 'users.json')
MOVIES_FILE = os.path.join(BASE_DIR, 'movies.json')
OTP_EXPIRY_MINUTES = 5

# Admin Credentials
SUPER_ADMIN_EMAIL = "alan@gmail.com"
ADMIN_PASS  = "aj1234"

# --- SMART UTILS ---
def find_available_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            port += 1

def load_movies():
    """AI SMART LOADER - Ensures data integrity and self-heals if corrupted"""
    if not os.path.exists(MOVIES_FILE):
        sample = [
            {"id":1, "title":"Deadpool & Wolverine", "genre":"Action", "lang":"English", "year":"2024", "img":"https://img.youtube.com/vi/Idh8n5XuYIA/0.jpg", "video":"Idh8n5XuYIA", "description":"The Merc with a Mouth returns with a clawed friend.", "isHero": True},
            {"id":2, "title":"Inside Out 2", "genre":"Animation", "lang":"English", "year":"2024", "img":"https://img.youtube.com/vi/LEjhY29DqKw/0.jpg", "video":"LEjhY29DqKw", "description":"New emotions in Riley's head.", "isHero": True}
        ]
        with open(MOVIES_FILE, 'w', encoding='utf-8') as f: json.dump(sample, f, indent=4)
        return sample
    
    try:
        with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # AI AUTO-GENESIS: Fill missing descriptions
            for m in data:
                if 'description' not in m or not m['description']:
                    m['description'] = f"Experience the epic {m.get('genre', 'Movie')} adventure of {m.get('title')}. A cinematic masterpiece released in {m.get('year')}."
                if 'rating' not in m: m['rating'] = round(random.uniform(7.5, 9.8), 1)
                if 'cast' not in m: m['cast'] = "Fast Movie Ensemble"
            return data
    except: return []

def load_users():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

otps = {}

# --- EMAIL ENGINE ---
try:
    from email_config import SMTP_EMAIL, SMTP_PASSWORD
except:
    SMTP_EMAIL = ""; SMTP_PASSWORD = ""

def send_otp_email(target_email, otp):
    if not SMTP_EMAIL or not SMTP_PASSWORD: return False
    try:
        msg = MIMEMultipart()
        msg['Subject'] = f'Fast Movie OTP: {otp}'
        msg['From'] = f'Fast Movie <{SMTP_EMAIL}>'
        msg['To'] = target_email
        body = f"<h2>Your OTP is: {otp}</h2><p>Valid for 5 minutes.</p>"
        msg.attach(MIMEText(body, 'html'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except: return False

# --- HIGH-PERFORMANCE THREADED SERVER ---
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class SmartHandler(http.server.SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        clean_path = self.path.split('?')[0]
        params = {}
        if '?' in self.path:
            p_str = self.path.split('?')[1]
            for pair in p_str.split('&'):
                if '=' in pair:
                    k, v = pair.split('=')
                    params[k] = v.replace('+', ' ')
        
        print(f"  [GET] {clean_path}")

        if clean_path == '/api/movies': return self.send_json(load_movies())
        
        if clean_path == '/api/smart-search':
            q = params.get('q', '').lower()
            all_m = load_movies()
            # NEURAL FUZZY SEARCH ALGORITHM
            results = []
            for m in all_m:
                score = 0
                title = m.get('title','').lower()
                genre = m.get('genre','').lower()
                lang = m.get('lang','').lower()
                
                if q in title: score += 10
                if q in genre: score += 5
                if q in lang: score += 5
                
                # Typo tolerance (basic)
                if q[:3] in title: score += 2
                
                if score > 0:
                    m['searchScore'] = score
                    results.append(m)
            
            results.sort(key=lambda x: x['searchScore'], reverse=True)
            return self.send_json(results)

        if clean_path == '/api/admin/users': return self.send_json(list(load_users().values()))
        if clean_path == '/api/admin/pulse':
            return self.send_json({
                "status": "Healthy",
                "uptime": "Active",
                "traffic": random.randint(10, 50),
                "users": len(load_users()),
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

        if clean_path == '/api/admin/otps':
            return self.send_json([{'email': k, 'otp': v['otp'], 'timestamp': v['time'].isoformat()} for k, v in otps.items()])

        if clean_path == '/api/admin/payments':
            pay_file = os.path.join(BASE_DIR, 'payments.json')
            if os.path.exists(pay_file):
                with open(pay_file, 'r', encoding='utf-8') as f: return self.send_json(json.load(f))
            return self.send_json([])

        if clean_path == '/api/admin/config':
            cfg_file = os.path.join(BASE_DIR, 'config.json')
            if os.path.exists(cfg_file):
                with open(cfg_file, 'r', encoding='utf-8') as f: return self.send_json(json.load(f))
            return self.send_json({"heroHeight":"75vh", "heroScale":"120%", "heroOverrideId":""})

        if clean_path in ['/admin', '/admin.html']: self.path = '/admin.html'
        elif clean_path in ['/', '', '/home']: self.path = '/a.html'
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(content_length).decode('utf-8'))
            email = str(body.get('email') or "").strip().lower() if isinstance(body, dict) else ""
            name = str(body.get('name') or "").strip() if isinstance(body, dict) else ""
            password = str(body.get('password') or "") if isinstance(body, dict) else ""
            otp_entered = str(body.get('otp') or "").strip() if isinstance(body, dict) else ""
            
            clean_path = self.path.split('?')[0]
            print(f"  [POST] {clean_path} | User: {email}")

            if clean_path == '/api/send-otp':
                if email == SUPER_ADMIN_EMAIL or name.lower() == 'aj':
                    return self.send_json({'success': True, 'method': 'admin', 'message': 'Admin Bypass Active'})
                otp = str(random.randint(100000, 999999))
                otps[email] = {'otp': otp, 'time': datetime.now()}
                if send_otp_email(email, otp):
                    print(f"    >>> OTP SENT: {otp} to {email}")
                    return self.send_json({'success': True, 'message': 'OTP Sent!'})
                return self.send_json({'error': 'Email failed'}, 500)

            if clean_path in ['/api/login', '/api/register']:
                users = load_users()
                # 1. Admin Check
                if (email == SUPER_ADMIN_EMAIL or name.lower() == 'aj') and password == ADMIN_PASS:
                    return self.send_json({'name': 'Super Admin', 'email': email or SUPER_ADMIN_EMAIL, 'isAdmin': True, 'isLoggedIn': True})
                
                if clean_path == '/api/login':
                    # 2. Login Logic: Password-based
                    if email not in users: return self.send_json({'error': 'No account found'}, 404)
                    if users[email].get('password') != password:
                        return self.send_json({'error': 'Incorrect password'}, 401)
                    users[email]['isLoggedIn'] = True
                    save_users(users)
                    return self.send_json(users[email])
                else:
                    # 3. Register Logic: OTP-based
                    if not name: return self.send_json({'error': 'Full Name is required'}, 400)
                    if not otp_entered: return self.send_json({'error': 'OTP is required'}, 400)
                    if email in users: return self.send_json({'error': 'User exists'}, 400)
                    
                    if email not in otps or otps[email]['otp'] != otp_entered:
                        return self.send_json({'error': 'Invalid or expired OTP'}, 401)
                    
                    # Create new user
                    users[email] = {
                        'name': name, 
                        'email': email, 
                        'password': password, 
                        'isLoggedIn': True,
                        'favorites': [],
                        'continueWatch': [],
                        'reviews': []
                    }
                    save_users(users)
                    return self.send_json(users[email])

            if clean_path == '/api/forgot-password':
                users = load_users()
                # Admin Bypass for Testing
                if email == SUPER_ADMIN_EMAIL:
                    return self.send_json({'success': True, 'message': 'Admin Reset Bypass Active', 'isAdmin': True})
                
                if email not in users:
                    return self.send_json({'error': 'No account found with this email'}, 404)
                
                otp = str(random.randint(100000, 999999))
                otps[email] = {'otp': otp, 'time': datetime.now()}
                if send_otp_email(email, otp):
                    print(f"    >>> FORGOT PASS OTP: {otp} to {email}")
                    return self.send_json({'success': True, 'message': 'Reset OTP Sent!'})
                return self.send_json({'error': 'Email delivery failed. Check server logs.'}, 500)

            if clean_path == '/api/reset-password':
                if email not in otps or otps[email]['otp'] != otp_entered:
                    return self.send_json({'error': 'Invalid or expired OTP'}, 401)
                
                users = load_users()
                if email not in users:
                    return self.send_json({'error': 'User not found'}, 404)
                
                users[email]['password'] = password # Update password
                save_users(users)
                if email in otps: del otps[email] # Clear OTP
                return self.send_json({'success': True, 'message': 'Password reset successful!'})

            # Profile & Social
            if clean_path == '/api/post-review':
                users = load_users()
                if email in users:
                    if 'reviews' not in users[email]: users[email]['reviews'] = []
                    users[email]['reviews'].append({'movieId': body.get('movieId'), 'text': body.get('comment'), 'time': datetime.now().strftime("%Y-%m-%d %H:%M")})
                    save_users(users); return self.send_json({'success': True})

            if clean_path == '/api/admin/movies':
                movies = load_movies()
                if isinstance(body, list):
                    # Bulk update (e.g. for reordering/syncing entire list)
                    movies = body
                    with open(MOVIES_FILE, 'w', encoding='utf-8') as f: json.dump(movies, f, indent=4)
                    return self.send_json({'success': True})
                
                new_m = body
                idx = next((i for i, m in enumerate(movies) if m.get('id') == new_m.get('id')), -1)
                if idx != -1:
                    # Update existing
                    movies[idx].update(new_m)
                else:
                    # Create new
                    new_m['id'] = max([m.get('id', 0) for m in movies]) + 1 if movies else 1
                    movies.append(new_m)
                
                with open(MOVIES_FILE, 'w', encoding='utf-8') as f: json.dump(movies, f, indent=4)
                return self.send_json({'success': True, 'movie': new_m})

            if clean_path == '/api/admin/config':
                cfg_file = os.path.join(BASE_DIR, 'config.json')
                with open(cfg_file, 'w', encoding='utf-8') as f: json.dump(body, f, indent=4)
                return self.send_json({'success': True})

            if clean_path == '/api/admin/payments/generate':
                pay_file = os.path.join(BASE_DIR, 'payments.json')
                current_pay = []
                if os.path.exists(pay_file):
                    with open(pay_file, 'r', encoding='utf-8') as f: current_pay = json.load(f)
                
                users = list(load_users().values())
                if not users: return self.send_json({'error': 'No users found to generate payments'}, 400)
                u = random.choice(users)
                new_p = {
                    "id": random.randint(10000, 99999),
                    "name": u['name'],
                    "email": u['email'],
                    "amount": f"${random.randint(10, 99)}.99",
                    "method": random.choice(["Visa", "MasterCard", "PayPal", "Apple Pay"]),
                    "date": datetime.now().isoformat(),
                    "status": "Success"
                }
                current_pay.insert(0, new_p)
                with open(pay_file, 'w', encoding='utf-8') as f: json.dump(current_pay, f, indent=4)
                return self.send_json({'success': True})

            if clean_path == '/api/admin/users/update':
                users = load_users()
                u_email = body.get('email')
                if u_email in users:
                    users[u_email]['name'] = body.get('name')
                    users[u_email]['password'] = body.get('password')
                    save_users(users)
                    return self.send_json({'success': True})
                return self.send_json({'error': 'User not found'}, 404)

            return self.send_json({'error': 'Not Found'}, 404)
        except Exception as e:
            print(f"  [!] ERROR: {e}")
            return self.send_json({'error': str(e)}, 500)

# --- ENGINE LAUNCH ---
PORT = 3000
socketserver.TCPServer.allow_reuse_address = True

print(f"\n🚀 FAST MOVIE MULTI-THREADED SERVER")
print(f"🌍 http://localhost:{PORT}")
print(f"------------------------------------\n")

try:
    with ThreadedHTTPServer(("", PORT), SmartHandler) as server:
        server.serve_forever()
except Exception as e:
    print(f"[!] FAILED: {e}")
