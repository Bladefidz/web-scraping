module.exports = {
    url: 'https://www.google.com/flights/?gl=US',
    months: 7,
    selectors: {
        from: 'input[placeholder="Where from?"]',
        to: 'input[placeholder="Where to?"]',
        calendar: '.OMOBOQD-p-j',
        departure: '.OMOBOQD-G-q input',
        nextMonth: '.datePickerNextButton',
        monthText: '.OMOBOQD-p-b',
        greenPrice: '.OMOBOQD-p-j td .OMOBOQD-p-f.OMOBOQD-o-c, .OMOBOQD-p-j td .OMOBOQD-p-f.OMOBOQD-o-b',
        price: '.OMOBOQD-p-j td .OMOBOQD-p-f',
        nextGreenPrice: '.OMOBOQD-p-o td .OMOBOQD-p-f.OMOBOQD-o-c, .OMOBOQD-p-o td .OMOBOQD-p-f.OMOBOQD-o-b',
    },
    post: 'https://requestb.in/1d84uie1',
    duration: {
        min: 5,
        max: 21,
    },
};
