const child_process = require('child_process');

const axios = require('axios');
const express = require('express');
const winston = require('winston');

const config = require('./config');

const Queue = require('./queue');

const app = express();

const isHeadless = process.argv.some(arg => arg === '--headless');

// Executes `command` with `args`, running the thing in `xvfb-run` if `isHeadless` is true above.
// Returns a Promise that resolves to the stdout of the process when the process exits.
const run = (command, args) => {
    return new Promise((resolve, reject) => {
        if (isHeadless) {
            args = [command].concat(args);
            command = 'xvfb-run';
        }
        winston.info('run', {command, args});
        const process = child_process.spawn(command, args);
        let output = '';
        process.stdout.on('data', (data) => {
            output += data.toString();
        });
        process.on('close', (code) => {
            winston.info('process.close', {code});
            if (code === 0) {
                try {
                    resolve(JSON.parse(output));
                } catch (e) {
                    reject(e);
                }
            } else {
                reject({code});
            }
        });
    });
};

const LoadDates = new Queue({
    name: 'LoadDates',
    delay: 5000,
    callback: async ([origin, destination]) => {
        winston.info('LoadDates', {origin, destination});
        const data = await run('node', ['flights.js', origin, destination]);
        winston.info(`LoadDates: Found ${data.length} entries.`);
        winston.info('LoadDates', {origin, destination, data});
        winston.info(`LoadDates: POST ${config.post}`);
        await axios.post(config.post, {origin, destination, data});
    },
});

app.get('/load_dates', async (req, resp) => {
    const {origin, destination} = req.query;
    winston.info('GET /load_dates', {origin, destination});
    if (origin && destination) {
        winston.info('LoadDates.push', [origin, destination]);
        // Enqueue the job.
        LoadDates.push([origin, destination]);
        resp.end('OK');
    } else {
        resp.status(500).end('origin or destination missing');
    }
});

const port = process.env.PORT || 4000;
app.listen(port, () => {
    console.log(`Listening on http://127.0.0.1:${port}`);
});