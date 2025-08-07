#!/usr/bin/env node

/**
 * YT-Search CLI Wrapper
 * This file ensures the package works globally when installed via npm
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Find Python executable
function findPython() {
    const pythonCommands = process.platform === 'win32' 
        ? ['python', 'python3'] 
        : ['python3', 'python'];
    
    const { execSync } = require('child_process');
    
    for (const cmd of pythonCommands) {
        try {
            execSync(`${cmd} --version`, { stdio: 'ignore' });
            return cmd;
        } catch (e) {
            continue;
        }
    }
    
    console.error('Error: Python 3 is not installed or not in PATH.');
    console.error('Please install Python 3.7 or higher from https://python.org');
    process.exit(1);
}

// Main execution
const pythonCmd = findPython();
const scriptDir = path.join(__dirname, '..');
const args = ['-m', 'yt_search.main', ...process.argv.slice(2)];

// Set Python path
process.env.PYTHONPATH = scriptDir + (process.env.PYTHONPATH ? ':' + process.env.PYTHONPATH : '');

// Spawn Python process
const python = spawn(pythonCmd, args, {
    stdio: 'inherit',
    cwd: scriptDir,
    env: process.env
});

python.on('error', (err) => {
    if (err.code === 'ENOENT') {
        console.error('Error: Python executable not found.');
        console.error('Please ensure Python 3 is installed and in your PATH.');
    } else {
        console.error('Error starting YT-Search:', err);
    }
    process.exit(1);
});

python.on('exit', (code) => {
    process.exit(code || 0);
});
