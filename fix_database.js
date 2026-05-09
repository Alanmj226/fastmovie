const fs = require('fs');
let movies = JSON.parse(fs.readFileSync('movies.json', 'utf8'));

movies = movies.map(m => {
    // Extract video ID
    let vid = m.video;
    if (vid.includes('embed/')) vid = vid.split('embed/')[1];
    if (vid.includes('watch?v=')) vid = vid.split('watch?v=')[1];
    m.video = vid;

    // Use YouTube thumbnail for all
    m.img = `https://img.youtube.com/vi/${vid}/hqdefault.jpg`;
    
    return m;
});

fs.writeFileSync('movies.json', JSON.stringify(movies, null, 2));
console.log("Fixed " + movies.length + " movies in movies.json");
