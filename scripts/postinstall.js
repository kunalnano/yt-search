#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

console.log('📦 YT-Search Post-Install Setup');
console.log('================================\n');

// Check Python installation
function checkPython() {
    const pythonCommands = ['python3', 'python'];
    
    for (const cmd of pythonCommands) {
        try {
            const version = execSync(`${cmd} --version 2>&1`).toString().trim();
            console.log(`✅ Found ${version}`);
            return cmd;
        } catch (e) {
            // Continue to next command
        }
    }
    
    console.error('❌ Python 3 is required but not found!');
    console.error('Please install Python 3.7 or higher:');
    console.error('  macOS: brew install python3');
    console.error('  Ubuntu/Debian: sudo apt-get install python3');
    console.error('  Windows: Download from https://python.org');
    process.exit(1);
}

// Create global command wrapper
function createWrapper() {
    const wrapperPath = path.join(__dirname, '..', 'bin', 'yt-search');
    const pythonCmd = checkPython();
    
    const wrapperContent = `#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const scriptPath = path.join(__dirname, '..', 'yt_search');
const python = spawn('${pythonCmd}', ['-m', 'yt_search.main', ...process.argv.slice(2)], {
    stdio: 'inherit',
    cwd: path.join(__dirname, '..')
});

python.on('error', (err) => {
    if (err.code === 'ENOENT') {
        console.error('Error: Python 3 is not installed or not in PATH.');
    } else {
        console.error('Error:', err);
    }
    process.exit(1);
});

python.on('exit', (code) => {
    process.exit(code || 0);
});
`;

    fs.writeFileSync(wrapperPath, wrapperContent);
    
    // Make executable
    if (process.platform !== 'win32') {
        fs.chmodSync(wrapperPath, '755');
    }
    
    console.log('✅ Command wrapper created');
}

// Main setup
try {
    createWrapper();
    
    console.log('\n✨ Installation complete!');
    console.log('\nYou can now use:');
    console.log('  yt-search          - Launch interactive mode');
    console.log('  yt-search "query"  - Direct search');
    console.log('  yts "query"        - Short alias\n');
    
} catch (error) {
    console.error('❌ Installation failed:', error.message);
    process.exit(1);
}
