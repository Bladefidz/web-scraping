const Nightmare = require('nightmare');
const moment = require('moment');

const config = require('./config');

if (process.argv.length != 4) {
    console.log('Usage: node flights.js <source> <destination>');
    process.exit(1);
}

const [, , from, to] = process.argv;

async function main() {
    const nightmare = Nightmare({
        show: !true,
        webPreferences: {
            partition: 'nopersist',
        },
        executionTimeout: 15 * 60 * 1000, // 15 minutes
    });

    await nightmare
        .goto(config.url)
        .click(config.selectors.from)
        .wait(2000)
        // Type `from` followed by a RET.
        .type(config.selectors.from, from + '\r')
        .wait(5000)
        .click(config.selectors.to)
        // Type `to` followed by a RET.
        .type(config.selectors.to, to + '\r')
        .wait(5000);

    const data = await nightmare.evaluate(async (config) => {
        const $ = selector => document.querySelector(selector);
        const $$ = selector => [].slice.call(document.querySelectorAll(selector));
        const click = selector => $(selector).click();
        const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

        const data = [];

        click(config.selectors.departure);
        await sleep(5000);

        for (let i = 0; i < config.months; i++) {
            for (let j = 0; j < $$(config.selectors.greenPrice).length; j++) {
                click(config.selectors.departure);
                await sleep(3000);
                const green = $$(config.selectors.greenPrice)[j];
                if (!green) {
                    break;
                }
                const start = {
                    monthOffset: i,
                    date: parseInt(green.previousSibling.textContent, 10),
                };
                green.click();
                await sleep(3000);
                $$(config.selectors.greenPrice).forEach(el => {
                    const end = {
                        monthOffset: i,
                        date: parseInt(el.previousSibling.textContent, 10),
                    };
                    data.push({
                        start,
                        end,
                        price: parseInt(el.textContent.replace(/[^0-9]/g, ''), 10),
                    });
                });
                $$(config.selectors.nextGreenPrice).forEach(el => {
                    const end = {
                        monthOffset: i + 1,
                        date: parseInt(el.previousSibling.textContent, 10),
                    };
                    data.push({
                        start,
                        end,
                        price: parseInt(el.textContent.replace(/[^0-9]/g, ''), 10),
                    });
                });
            }
            click(config.selectors.departure);
            await sleep(5000);
            click(config.selectors.nextMonth);
            await sleep(5000);
        }
        return data;
    }, config);

    await nightmare.end();

    return data.map(({start, end, price}) => {
        const date = ({monthOffset, date}) => moment().add(monthOffset, 'months').date(date).format('YYYYMMDD');
        return {
            start: date(start),
            end: date(end),
            price,
        };
    }).filter(({start, end}) => {
        // Reject entries that are less than `config.duration.min` days or more than
        // `config.duration.max` days.
        start = moment(start, 'YYYYMMDD');
        end = moment(end, 'YYYYMMDD');
        const diff = end.diff(start, 'days');
        return config.duration.min <= diff && diff <= config.duration.max;
    });
}

main().then(data => {
    console.log(JSON.stringify(data, null, 4));
}).catch(error => {
    console.log(JSON.stringify({error}));
});
