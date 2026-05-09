// FAST MOVIE - CORE NEURAL ENGINE (v2.0 Modular)
// Powered by __AJ__2026

const FALLBACK_DATABASE = [
    { id: 1, title: "John Wick: Chapter 4", genre: "Action", lang: "English", year: "2023", type: "movie", img: "https://img.youtube.com/vi/qEVUtrk8_B4/hqdefault.jpg", video: "qEVUtrk8_B4", description: "John Wick uncovers a path to defeating The High Table.", isHero: true },
    { id: 45, title: "Panchayat", genre: "Comedy", lang: "Hindi", year: "2024", type: "tv", img: "https://img.youtube.com/vi/9XInQJRqGW4/hqdefault.jpg", video: "9XInQJRqGW4", description: "An engineer takes a job in a remote village.", isHero: true },
    { id: 46, title: "Gullak", genre: "Comedy", lang: "Hindi", year: "2024", type: "tv", img: "https://img.youtube.com/vi/yAN5svZdw_o/hqdefault.jpg", video: "yAN5svZdw_o", description: "The everyday life of a middle-class family." },
    // ... rest of the massive database ...
    { id: 161, title: "Asian Cup 2024", genre: "Football", lang: "Global", year: "2024", type: "sport", img: "https://img.youtube.com/vi/qEVUtrk8_B4/hqdefault.jpg", video: "qEVUtrk8_B4", description: "Qatar vs Jordan." }
];

// STATE MANAGEMENT
let movies = [];
let watchlist = JSON.parse(localStorage.getItem('watchlist')) || [];
let history = JSON.parse(localStorage.getItem('history')) || [];
let currentHeroIndex = 0;
let heroInterval;
let isAdmin = false;
let authMode = 'login';
let appConfig = { heroRotationDuration: 8000, heroAutoRotation: true };
let currentSiteLanguage = 'English';

// ATTACH TO WINDOW FOR LEGACY HTML COMPATIBILITY
window.init = init;
window.handleSearch = handleSearch;
window.showPage = showPage;
window.openWatch = openWatch;
window.toggleWatchlist = toggleWatchlist;
window.filterLang = filterLang;
window.doLogout = doLogout;
window.setMode = setMode;
window.searchAll = searchAll;
window.toggleChat = toggleChat;
window.sendMessage = sendMessage;
window.submitUserReview = submitUserReview;
window.startVoiceAI = startVoiceAI;
window.toggleHeroMute = toggleHeroMute;
window.jumpHero = jumpHero;
window.selectAvatar = selectAvatar;
window.handleAvatarUpload = handleAvatarUpload;
window.toggleAvatarPicker = toggleAvatarPicker;
window.saveProfileUpdates = saveProfileUpdates;
window.setSiteLanguage = setSiteLanguage;

async function init() {
    try {
        let data = [];
        let cfg = null;

        try {
            const moviesRes = await fetch(`/api/movies?t=${Date.now()}`);
            if (moviesRes.ok) data = await moviesRes.json();
        } catch(err) { console.warn("Movies API unreachable"); }

        try {
            const configRes = await fetch(`/api/config?t=${Date.now()}`);
            if (configRes.ok) cfg = await configRes.json();
        } catch(err) { console.warn("Config API unreachable"); }
        
        if (data && data.length > 0) {
            movies = data;
        } else {
            movies = [...FALLBACK_DATABASE];
        }

        if (cfg) {
            appConfig = { ...appConfig, ...cfg };
            const heroRow = document.querySelector('.hero-row');
            if (heroRow) heroRow.style.height = cfg.heroHeight || "75vh";
            const heroVideo = document.getElementById('heroVideo');
            if (heroVideo) {
                heroVideo.style.width = cfg.heroScale || "120%";
                heroVideo.style.height = cfg.heroScale || "120%";
            }
            
            if (cfg.heroOverrideId) {
                const cleanOverrideId = getYoutubeId(cfg.heroOverrideId);
                let overrideMovie = movies.find(m => getYoutubeId(m.video) === cleanOverrideId);
                
                if (!overrideMovie) {
                    overrideMovie = {
                        title: "FEATURED PREMIERE",
                        description: "This premium content has been hand-selected by the Master Admin for its cinematic excellence.",
                        video: cleanOverrideId,
                        isHero: true,
                        id: 9999
                    };
                }
                setTimeout(() => {
                    updateHero(overrideMovie);
                    stopHeroRotation();
                }, 500);
            } else if (appConfig.heroAutoRotation) {
                startHeroRotation();
            } else {
                setTimeout(() => {
                    const trending = movies.filter(m => m.isHero === true);
                    if (trending.length) updateHero(trending[0]);
                    stopHeroRotation();
                }, 500);
            }
        }
    } catch (e) {
        console.warn("Loading from offline database...");
        movies = [...FALLBACK_DATABASE];
        startHeroRotation();
    }
    renderAllRows(movies);
    renderContinueWatching();
    renderAISuggestions();
    setMode('login');
    
    const user = localStorage.getItem('currentUser');
    if (user) {
        const data = JSON.parse(user);
        document.getElementById('loginPage').style.display = 'none';
        document.getElementById('app').style.display = 'block';
        document.getElementById('profName').innerText = data.name;
        document.getElementById('profEmail').innerText = data.email;
        if (data.isAdmin) document.getElementById('adminLink').style.display = 'flex';
        showPage('home');
    }

    setTimeout(() => {
        const splash = document.getElementById('splashScreen');
        if(splash) {
            splash.style.pointerEvents = 'none';
            splash.style.opacity = '0';
            setTimeout(() => splash.style.display = 'none', 800);
        }
    }, 1000);
}

function startHeroRotation() {
    stopHeroRotation(); 
    if (!appConfig.heroAutoRotation) return;
    
    const scheduleNext = () => {
        const trending = movies.filter(m => m.isHero === true);
        if (!trending.length) return;
        
        currentHeroIndex = (currentHeroIndex + 1) % trending.length;
        const nextMovie = trending[currentHeroIndex];
        updateHero(nextMovie);
        
        const nextDuration = nextMovie.heroDuration || parseInt(appConfig.heroRotationDuration) || 8000;
        heroInterval = setTimeout(scheduleNext, nextDuration);
    };

    const trending = movies.filter(m => m.isHero === true);
    if (trending.length) {
        const currentMovie = trending[currentHeroIndex];
        const initialDuration = currentMovie.heroDuration || parseInt(appConfig.heroRotationDuration) || 8000;
        heroInterval = setTimeout(scheduleNext, initialDuration);
    }
}

function stopHeroRotation() {
    if (heroInterval) clearTimeout(heroInterval);
}

function getYoutubeId(url) {
    if (!url) return '';
    if (url.length === 11) return url;
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : url;
}

let heroMuted = true;
function toggleHeroMute() {
    heroMuted = !heroMuted;
    document.getElementById('heroMuteBtn').innerText = heroMuted ? '🔇' : '🔊';
    const trending = movies.filter(m => m.isHero === true);
    updateHero(trending[currentHeroIndex]);
}

function updateHero(m) {
    if (!m || (m.id !== 9999 && !m.isHero)) return;
    const heroTitle = document.getElementById('heroTitle');
    const heroDesc = document.getElementById('heroDesc');
    const heroVideo = document.getElementById('heroVideo');
    const heroPlayBtn = document.getElementById('heroPlayBtn');
    const heroListBtn = document.getElementById('heroListBtn');
    const dotsContainer = document.getElementById('heroDots');

    const trending = movies.filter(x => x.isHero === true);
    dotsContainer.innerHTML = trending.map((_, i) => `
        <div class="dot ${i === currentHeroIndex ? 'active' : ''}" onclick="jumpHero(${i})"></div>
    `).join('');

    heroTitle.style.opacity = '0';
    heroVideo.style.opacity = '0';
    
    setTimeout(() => {
        heroTitle.innerText = m.title;
        heroDesc.innerText = (m.description || '').substring(0, 150) + '...';
        const videoId = getYoutubeId(m.video);
        const muteParam = heroMuted ? 1 : 0;
        heroVideo.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=${muteParam}&controls=0&loop=1&playlist=${videoId}&rel=0&modestbranding=1&enablejsapi=1`;
        heroPlayBtn.onclick = () => openWatch(m.id);
        heroListBtn.onclick = () => toggleWatchlist(m.id);
        heroListBtn.innerText = watchlist.includes(m.id) ? '✓ IN LIST' : '+ MY LIST';
        heroTitle.style.opacity = '1';
        heroVideo.style.opacity = '0.85';
    }, 500);
}

function jumpHero(index) {
    currentHeroIndex = index;
    const trending = movies.filter(m => m.isHero === true);
    updateHero(trending[index]);
    startHeroRotation();
}

function openWatch(id) {
    const m = movies.find(x => x.id == id);
    if (!m) return;
    const videoId = getYoutubeId(m.video);
    const backdrop = document.getElementById('watchBackdrop');
    if (backdrop) backdrop.style.backgroundImage = `url(${m.img})`;
    document.getElementById('player').src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
    document.getElementById('watchTitle').innerText = m.title;
    document.getElementById('watchMeta').innerText = `${m.year} • ${m.genre} • ${m.lang} • Ultra HD 4K`;
    document.getElementById('watchDesc').innerText = m.description;
    document.getElementById('watchCast').innerText = m.cast || 'Fast Movie Ensemble';
    document.getElementById('watchRating').innerText = `⭐ ${m.rating || '8.5'}/10`;
    document.getElementById('watchReview').innerText = `"${m.review || 'An absolute must-watch for all movie lovers!'}"`;
    const watchListBtn = document.getElementById('watchListBtn');
    watchListBtn.innerText = watchlist.includes(m.id) ? '✓ In List' : '+ My List';
    watchListBtn.onclick = () => toggleWatchlist(m.id);
    const related = movies.filter(x => x.genre === m.genre && x.id !== m.id).slice(0, 8);
    document.getElementById('relatedContainer').innerHTML = related.map(r => `
        <div class="movie-card" onclick="openWatch(${r.id})" style="width:100%; display:flex; gap:15px; height:90px; background:rgba(255,255,255,0.05); border-radius:16px; overflow:hidden; border: 1px solid rgba(255,255,255,0.05); cursor:pointer;">
            <img src="${r.img}" style="width:120px; height:100%; object-fit:cover; transition:0.3s;">
            <div style="padding:10px; display:flex; flex-direction:column; justify-content:center;">
                <div style="font-weight:bold; font-size:15px; color:white;">${r.title}</div>
                <div style="font-size:12px; color:var(--accent); margin-top:4px;">${r.year} • ⭐ ${r.rating || '8.2'}</div>
            </div>
        </div>
    `).join('');
    showPage('watch');
    window.scrollTo(0, 0);
    const user = JSON.parse(localStorage.getItem('currentUser'));
    if (!(user && user.privacy === true)) {
        history = history.filter(x => x != m.id);
        history.unshift(m.id);
        localStorage.setItem('history', JSON.stringify(history.slice(0, 20)));
        renderContinueWatching();
    }
}

function toggleWatchlist(id) {
    if (watchlist.includes(id)) {
        watchlist = watchlist.filter(x => x !== id);
    } else {
        watchlist.push(id);
    }
    localStorage.setItem('watchlist', JSON.stringify(watchlist));
    renderAllRows(movies);
    const heroListBtn = document.getElementById('heroListBtn');
    if (heroListBtn) heroListBtn.innerText = watchlist.includes(id) ? '✓ IN LIST' : '+ MY LIST';
    const watchListBtn = document.getElementById('watchListBtn');
    if (watchListBtn) watchListBtn.innerText = watchlist.includes(id) ? '✓ IN LIST' : '+ MY LIST';
}

function createMovieCard(m) {
    const imgUrl = m.img || '';
    const isNew = m.year === '2024';
    return `
        <div class="movie-card" onclick="openWatch(${m.id})">
            <div class="poster-wrap" style="width:100%; height:100%; position:relative;">
                <img src="${imgUrl.includes('maxresdefault') ? imgUrl.replace('maxresdefault', 'hqdefault') : imgUrl}" 
                     class="movie-poster"
                     loading="lazy"
                     onload="this.style.opacity='1'"
                     style="opacity:0; transition: opacity 0.5s;"
                     onerror="this.parentElement.innerHTML = '<div class=\'poster-placeholder\'><div>🎬</div><div style=\'margin-top:10px\'>${m.title.toUpperCase()}</div><div style=\'font-size:8px; opacity:0.5; margin-top:5px\'>POSTER NOT FOUND</div></div>'">
            </div>
            ${isNew ? '<div style="position:absolute; top:15px; left:15px; background:var(--accent-gradient); padding:4px 12px; border-radius:10px; font-size:10px; font-weight:900; z-index:10; box-shadow:0 0 15px var(--accent-glow); border: 1px solid rgba(255,255,255,0.2);">NEW 2024</div>' : ''}
            <div class="movie-info">
                <div class="movie-name">${m.title}</div>
                <div class="movie-meta"><span>${m.genre}</span><span style="opacity:0.4;">|</span><span>${m.year}</span><span style="opacity:0.4;">|</span><span style="color: #00ff88;">HD</span></div>
            </div>
            ${watchlist.includes(m.id) ? '<div style="position:absolute; top:15px; right:15px; background:rgba(255,255,255,0.1); backdrop-filter:blur(10px); padding:4px 10px; border-radius:10px; font-size:10px; font-weight:800; z-index:10; border:1px solid var(--glass-border);">✓ LIST</div>' : ''}
        </div>
    `;
}

function renderAllRows(data) {
    renderSection('movie', 'movieRows', data);
    renderSection('tv', 'tvRows', data);
    renderSection('sport', 'sportsRows', data);
}

function renderSection(type, containerId, data) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '';
    const filtered = data.filter(m => (m.type || 'movie') === type);
    if (!filtered.length) return;
    const title = type === 'movie' ? 'Blockbuster Movies' : type === 'tv' ? 'Must-Watch Series' : 'Live Sports & Highlights';
    const row = document.createElement('div');
    row.className = 'row skeleton-row';
    row.style.minHeight = '300px';
    row.innerHTML = `<div class="row-title" style="opacity:0.3;">Loading...</div><div class="row-container"><div class="movie-card skeleton" style="height:250px;"></div><div class="movie-card skeleton" style="height:250px;"></div><div class="movie-card skeleton" style="height:250px;"></div><div class="movie-card skeleton" style="height:250px;"></div></div>`;
    container.appendChild(row);
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                row.className = 'row';
                row.style.minHeight = 'auto';
                row.innerHTML = `<div class="row-title"><div style="width:4px; height:24px; background:var(--accent); border-radius:4px; box-shadow:0 0 15px var(--accent);"></div>${title}</div><div class="row-container">${filtered.map(m => createMovieCard(m)).join('')}</div>`;
                observer.unobserve(row);
            }
        });
    }, { rootMargin: '100px' });
    observer.observe(row);
}

function renderContinueWatching() {
    const container = document.getElementById('continueWatchingContainer');
    const row = document.getElementById('continueWatchingRow');
    if (!container || !row) return;
    if (!history || history.length === 0) { row.style.display = 'none'; return; }
    const cards = history.map(id => {
        const m = movies.find(x => x.id == id);
        return m ? createMovieCard(m) : '';
    }).filter(c => c !== '').join('');
    if (cards) { row.style.display = 'block'; container.innerHTML = cards; }
    else { row.style.display = 'none'; }
}

function renderAISuggestions() {
    const aiRow = document.getElementById('aiRow');
    const container = document.getElementById('aiContainer');
    if (!aiRow || !container) return;
    if (!history.length) {
        aiRow.style.display = 'block';
        const defaults = movies.filter(m => m.year === '2024').slice(0, 8);
        container.innerHTML = defaults.map(m => createMovieCard(m)).join('');
        return;
    }
    aiRow.style.display = 'block';
    const lastMovie = movies.find(m => m.id == history[0]);
    if (!lastMovie) return;
    const suggestions = movies.filter(m => m.genre === lastMovie.genre && !history.includes(m.id)).slice(0, 10);
    container.innerHTML = suggestions.map(m => createMovieCard(m)).join('');
}

function filterLang(l, el) {
    document.querySelectorAll('.nav-tabs .tab-item').forEach(i => i.classList.remove('active'));
    if (el) el.classList.add('active');
    if (l === 'All') { renderAllRows(movies); }
    else {
        const filtered = movies.filter(m => m.lang === l);
        document.getElementById('movieRows').innerHTML = `<div class="row"><div class="row-title">✨ ${l} Hits</div><div class="row-container" style="flex-wrap: wrap;">${filtered.map(m => createMovieCard(m)).join('')}</div></div>`;
        document.getElementById('tvRows').innerHTML = '';
        document.getElementById('sportsRows').innerHTML = '';
    }
}

let lastHomeScroll = 0;
function showPage(pageId) {
    const currentPage = Array.from(document.querySelectorAll('.page')).find(p => p.style.display !== 'none');
    if (currentPage && currentPage.id === 'homePage') lastHomeScroll = window.scrollY;
    document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
    let targetId = pageId;
    if (pageId === 'home') targetId = 'homePage';
    if (pageId === 'tv') targetId = 'tvPage';
    if (pageId === 'sports') targetId = 'sportsPage';
    if (pageId === 'categories') targetId = 'categoriesPage';
    if (pageId === 'watch') targetId = 'watchPage';
    if (pageId === 'profile') targetId = 'profilePage';
    if (pageId === 'search') targetId = 'searchPage';
    const target = document.getElementById(targetId);
    if (target) {
        target.style.display = 'block';
        if (pageId === 'home') window.scrollTo({ top: lastHomeScroll, behavior: 'instant' });
        else window.scrollTo({ top: 0, behavior: 'instant' });
    }
}

let searchTimeout;
async function handleSearch(q) {
    const loader = document.getElementById('searchLoader');
    const queryLabel = document.getElementById('searchQuery');
    const container = document.getElementById('searchResults');
    if (!q || q.length < 1) {
        queryLabel.innerText = "Trending Now...";
        container.innerHTML = movies.slice(0, 12).map(m => createMovieCard(m)).join('');
        return;
    }
    showPage('search');
    if(loader) loader.style.display = 'block';
    queryLabel.innerText = `Searching for "${q}"...`;
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(async () => {
        let results = [];
        try {
            const res = await fetch(`/api/smart-search?q=${encodeURIComponent(q)}`);
            if (res.ok) results = await res.json();
            else throw new Error("API Down");
        } catch (e) {
            const lowerQ = q.toLowerCase();
            results = movies.filter(m => m.title.toLowerCase().includes(lowerQ) || m.genre.toLowerCase().includes(lowerQ) || (m.description && m.description.toLowerCase().includes(lowerQ)));
        } finally {
            if(loader) loader.style.display = 'none';
            if (results.length > 0) {
                queryLabel.innerText = `Found ${results.length} results for "${q}"`;
                container.innerHTML = results.map(m => createMovieCard(m)).join('');
            } else {
                queryLabel.innerText = "";
                container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 100px 20px; background: var(--glass); border-radius: 32px; border: 1px solid var(--glass-border);"><div style="font-size: 64px; margin-bottom: 20px; opacity: 0.5;">🔍</div><h2 style="font-size: 24px; font-weight: 800; margin-bottom: 10px;">No matches found for "${q}"</h2><p style="color: var(--text-muted); font-size: 14px; max-width: 300px; margin: 0 auto;">Try checking your spelling or search for another movie, genre, or actor.</p><button onclick="handleSearch('')" style="margin-top: 30px; background: var(--accent); border: none; color: white; padding: 12px 30px; border-radius: 12px; font-weight: 800; cursor: pointer;">View Trending Content</button></div>`;
            }
        }
    }, 400); 
}

function searchAll(q) {
    const input = document.getElementById('aiSearchInput');
    if (input) input.value = q;
    handleSearch(q);
}

function setMode(m) {
    authMode = m;
    document.getElementById('tabLogin').className = m === 'login' ? 'active' : '';
    document.getElementById('tabRegister').className = m === 'register' ? 'active' : '';
    const nameGroup = document.getElementById('nameGroup');
    const passBox = document.getElementById('passBox');
    const otpBtn = document.getElementById('otpBtn');
    const otpBox = document.getElementById('otpBox');
    const authBtn = document.getElementById('authBtn');
    if (m === 'login') {
        nameGroup.style.display = 'none'; otpBtn.style.display = 'none'; otpBox.style.display = 'none';
        passBox.style.display = 'block'; authBtn.style.display = 'block'; authBtn.innerText = 'Sign In';
    } else if (m === 'register') {
        nameGroup.style.display = 'block'; otpBtn.style.display = 'block'; otpBox.style.display = 'none';
        passBox.style.display = 'block'; authBtn.style.display = 'block'; authBtn.innerText = 'Create Account';
    }
}

function doLogout() {
    localStorage.removeItem('currentUser');
    location.reload();
}

function toggleChat() {
    const chat = document.getElementById('chatBox');
    chat.style.display = chat.style.display === 'flex' ? 'none' : 'flex';
}

function sendMessage() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;
    const container = document.getElementById('chatMessages');
    container.innerHTML += `<div class="msg user">${msg}</div>`;
    input.value = '';
    setTimeout(() => {
        container.innerHTML += `<div class="msg bot">Analyzing Neural Database... I found some ${msg} content for you! <span style="color:var(--accent); cursor:pointer;" onclick="searchAll('${msg}')">Click to view</span></div>`;
        container.scrollTop = container.scrollHeight;
    }, 1000);
}

// ... more functions from index.html ...
// (Omitting some for brevity in this scratch, but will include all in the final write)

init();
