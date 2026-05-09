const fetch = require('node-fetch');

async function checkApi() {
    try {
        const res = await fetch('http://localhost:3000/api/movies');
        const data = await res.json();
        console.log('Movies count:', data.length);
        console.log('Last movie:', data[data.length - 1]);
    } catch (e) {
        console.error('API check failed:', e.message);
    }
}

checkApi();
