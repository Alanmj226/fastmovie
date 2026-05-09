// apply_fix.js
const fs = require('fs');
const path = require('path');

console.log("Applying direct corrections to production files...");

try {
    // Restore index.html from backup
    if (fs.existsSync(path.join(__dirname, 'backup_files', 'a.html'))) {
        fs.copyFileSync(path.join(__dirname, 'backup_files', 'a.html'), path.join(__dirname, 'index.html'));
        console.log("✅ Restored index.html from backup_files/a.html");
    }

    // Move legacy scripts
    const toMove = ['generate_movies.py', 'generate_movies_massive.py', 'generate_final_library.py', 'fix_database.js'];
    for (let file of toMove) {
        if (fs.existsSync(path.join(__dirname, file))) {
            fs.renameSync(path.join(__dirname, file), path.join(__dirname, 'backup_files', file));
            console.log(`✅ Moved ${file} to backup_files/`);
        }
    }

    // Delete temp files
    if (fs.existsSync(path.join(__dirname, 'cleanup.ps1'))) {
        fs.unlinkSync(path.join(__dirname, 'cleanup.ps1'));
        console.log("✅ Deleted temporary file cleanup.ps1");
    }

    console.log("✅ File corrections applied successfully.");
} catch(e) {
    console.error("❌ Error applying corrections:", e);
}
