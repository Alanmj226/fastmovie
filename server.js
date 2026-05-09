const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
// --- ROUTES ---

app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'index.html')));
app.get('/admin', (req, res) => res.sendFile(path.join(__dirname, 'admin.html')));

app.use(express.static(__dirname));

const ADMIN_EMAIL = "admin@fastmovie.com";
const SUPER_ADMIN_EMAIL = "alan@gmail.com";
const ADMIN_PASS = "aj1234";

let users = {};
if (fs.existsSync('users.json')) {
    try { users = JSON.parse(fs.readFileSync('users.json')); } catch(e) {}
}

let movies = [];
if (fs.existsSync('movies.json')) {
    try { movies = JSON.parse(fs.readFileSync('movies.json')); } catch(e) { console.error("Error loading movies.json", e); }
}

let config = {
    heroHeight: "75vh",
    heroScale: "120%",
    heroOverrideId: ""
};
if (fs.existsSync('config.json')) {
    try { config = JSON.parse(fs.readFileSync('config.json')); } catch(e) {}
}

let recentOTPs = [];
let payments = [];
if (fs.existsSync('payments.json')) {
    try { payments = JSON.parse(fs.readFileSync('payments.json')); } catch(e) {}
}

app.get('/api/config', (req, res) => res.json(config));

app.post('/api/admin/config', (req, res) => {
    config = { ...config, ...req.body };
    fs.writeFileSync('config.json', JSON.stringify(config, null, 2));
    res.json({ success: true, config });
});

app.get('/api/movies', (req, res) => res.json(movies));

app.post('/api/send-otp', (req, res) => {
    const name = (req.body.name || "").trim().toLowerCase();
    const email = (req.body.email || "").trim().toLowerCase();
    
    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    recentOTPs.unshift({ email, otp, timestamp: new Date().toISOString() });
    if (recentOTPs.length > 50) recentOTPs.pop();

    if (name === "aj" || email === SUPER_ADMIN_EMAIL || email === ADMIN_EMAIL) {
        console.log(`[ADMIN] Bypass Triggered for ${email}. OTP: aj1234 (Override)`);
        return res.json({ success: true, method: "admin" });
    }
    
    console.log(`[AUTH] OTP for ${email}: ${otp}`);
    res.json({ success: true, method: "terminal", message: `OTP: ${otp}` });
});

app.get('/api/admin/otps', (req, res) => res.json(recentOTPs));

app.post('/api/forgot-password', (req, res) => {
    const email = (req.body.email || "").trim().toLowerCase();
    if (!users[email]) return res.status(404).json({ error: "No account found with this email" });
    console.log(`[AUTH] Forgot Password OTP: 654321 to ${email}`);
    res.json({ success: true, message: "Reset OTP Sent!" });
});

app.post('/api/reset-password', (req, res) => {
    const { email, password } = req.body;
    const e = (email || "").trim().toLowerCase();
    if (!users[e]) return res.status(404).json({ error: "User not found" });
    users[e].password = password;
    fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
    res.json({ success: true, message: "Password reset successful!" });
});

app.post(['/api/login', '/api/register'], (req, res) => {
    const { name, email, password } = req.body;
    const n = (name || "").trim().toLowerCase();
    const e = (email || "").trim().toLowerCase();

    // Admin Bypass
    const isAdmin = (n === "aj" || e === SUPER_ADMIN_EMAIL || e === ADMIN_EMAIL);

    if (isAdmin && password === ADMIN_PASS) {
        const adminUser = {
            name: (n === "aj") ? "Super Admin" : "Administrator",
            email: e || SUPER_ADMIN_EMAIL,
            isAdmin: true,
            isLoggedIn: true,
            favorites: [],
            continueWatch: []
        };
        // Ensure admin exists in DB so they can save settings
        if (!users[adminUser.email]) {
            users[adminUser.email] = adminUser;
            fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
        }
        return res.json(adminUser);
    }

    if (req.path === '/api/login') {
        if (!users[e]) return res.status(404).json({ error: "Account not found" });
        users[e].isLoggedIn = true;
        return res.json(users[e]);
    } else {
        users[e] = { name, email: e, password, favorites: [], continueWatch: [], isLoggedIn: true };
        fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
        return res.json(users[e]);
    }
});

app.get('/api/admin/users', (req, res) => res.json(Object.values(users)));

app.post('/api/admin/movies', (req, res) => {
    const data = req.body;
    if (Array.isArray(data)) {
        movies = data;
    } else {
        const movie = data;
        const index = movies.findIndex(m => m.id === movie.id);
        if (index !== -1) {
            movies[index] = movie;
        } else {
            movie.id = movies.length > 0 ? Math.max(...movies.filter(m => m.id).map(m => m.id)) + 1 : 1;
            movies.push(movie);
        }
    }
    fs.writeFileSync('movies.json', JSON.stringify(movies, null, 2));
    res.json({ success: true, moviesCount: movies.length });
});

app.delete('/api/admin/movies/:id', (req, res) => {
    const id = parseInt(req.params.id);
    movies = movies.filter(m => m.id !== id);
    fs.writeFileSync('movies.json', JSON.stringify(movies, null, 2));
    res.json({ success: true });
});

app.get('/api/admin/pulse', (req, res) => {
    res.json({
        users: Object.keys(users).length,
        movies: movies.length,
        admins: 1,
        activeSessions: Object.values(users).filter(u => u.isLoggedIn).length
    });
});

app.post('/api/admin/users/update', (req, res) => {
    const { email, name, password } = req.body;
    const e = (email || "").trim().toLowerCase();
    if (!users[e]) return res.status(404).json({ error: "User not found" });
    
    if (name) users[e].name = name;
    if (password) users[e].password = password;
    
    fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
    res.json({ success: true, user: users[e] });
});

app.post('/api/update-profile', (req, res) => {
    const { email, ...settings } = req.body;
    const e = (email || "").trim().toLowerCase();
    if (!users[e]) return res.status(404).json({ success: false, error: "User not found" });
    
    // Dynamically update all provided settings
    users[e] = { ...users[e], ...settings };
    
    fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
    res.json({ success: true });
});

app.get('/api/admin/backup', (req, res) => {
    const backup = {
        users,
        movies,
        config,
        payments,
        timestamp: new Date().toISOString()
    };
    res.json(backup);
});

app.get('/api/admin/payments', (req, res) => res.json(payments));

app.post('/api/admin/payments/generate', (req, res) => {
    const userEmails = Object.keys(users);
    if (userEmails.length === 0) return res.status(400).json({ error: "No users found to charge" });
    
    const randomEmail = userEmails[Math.floor(Math.random() * userEmails.length)];
    const amount = (Math.random() * 50 + 9).toFixed(2);
    const newPayment = {
        id: Date.now(),
        email: randomEmail,
        name: users[randomEmail].name,
        amount: `$${amount}`,
        date: new Date().toISOString(),
        status: Math.random() > 0.1 ? "Success" : "Failed",
        method: ["Credit Card", "UPI", "PayPal", "Apple Pay"][Math.floor(Math.random() * 4)]
    };
    
    payments.unshift(newPayment);
    if (payments.length > 100) payments.pop();
    fs.writeFileSync('payments.json', JSON.stringify(payments, null, 2));
    res.json({ success: true, payment: newPayment });
});

app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'index.html')));
app.get('/admin', (req, res) => res.sendFile(path.join(__dirname, 'admin.html')));

app.listen(PORT, () => console.log(`Server running at http://localhost:${PORT}`));
