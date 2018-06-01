const winston = require('winston');

module.exports = class Queue {
    // Create a Queue with the given delay and callback.
    constructor({delay = 0, name = 'Untitled', callback}) {
        this.name = name;
        this.delay = delay;
        this.callback = callback;
        this.items = [];
    }

    // Push an item to the queue.
    // Start processing the queue if this is the first push.
    push(item) {
        winston.info(`Queue[${this.name}].push`, {item});
        this.items.push(item);
        if (!this.started) {
            this.tick();
        }
    }

    // If an item exists in the queue, process it and call tick() after `delay` ms.
    // Otherwise call tick() after `delay` ms.
    tick() {
        this.started = true;
        const item = this.items.shift();
        const next = () => {
            setTimeout(() => this.tick(), this.delay);
        };
        if (item) {
            winston.info(`Queue[${this.name}]: Processing`, {item});
            this.callback(item).then(() => {
                winston.info(`Queue[${this.name}]: Success`);
                next();
            }).catch(error => {
                console.log(error);
                winston.error(`Queue[${this.name}]: Error`, {error});
                next();
            });
        } else {
            next();
        }
    }
};
