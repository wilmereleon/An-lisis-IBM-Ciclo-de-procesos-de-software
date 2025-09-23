const fs = require('fs');
const path = require('path');

/**
 * Simple Logger for IBM Quality Management System
 * Implementa logging básico con niveles y archivos rotativos
 */
class Logger {
    constructor() {
        this.logDir = path.join(__dirname, '../../logs');
        this.ensureLogDirectory();
    }
    
    ensureLogDirectory() {
        if (!fs.existsSync(this.logDir)) {
            fs.mkdirSync(this.logDir, { recursive: true });
        }
    }
    
    getCurrentDate() {
        return new Date().toISOString().split('T')[0];
    }
    
    formatMessage(level, message, meta = {}) {
        const timestamp = new Date().toISOString();
        const logMessage = {
            timestamp,
            level,
            message,
            ...meta
        };
        return JSON.stringify(logMessage);
    }
    
    writeToFile(level, message, meta = {}) {
        const logFile = path.join(this.logDir, `${this.getCurrentDate()}.log`);
        const formattedMessage = this.formatMessage(level, message, meta);
        
        fs.appendFile(logFile, formattedMessage + '\n', (err) => {
            if (err) {
                console.error('Error writing to log file:', err);
            }
        });
    }
    
    info(message, meta = {}) {
        console.log(`[INFO] ${message}`, meta);
        this.writeToFile('INFO', message, meta);
    }
    
    error(message, meta = {}) {
        console.error(`[ERROR] ${message}`, meta);
        this.writeToFile('ERROR', message, meta);
    }
    
    warn(message, meta = {}) {
        console.warn(`[WARN] ${message}`, meta);
        this.writeToFile('WARN', message, meta);
    }
    
    debug(message, meta = {}) {
        if (process.env.NODE_ENV === 'development') {
            console.log(`[DEBUG] ${message}`, meta);
            this.writeToFile('DEBUG', message, meta);
        }
    }
}

module.exports = new Logger();