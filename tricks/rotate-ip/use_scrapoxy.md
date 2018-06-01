## Install scraproxy from NPM

```
sudo apt-get install build-essential
sudo npm install -g scrapoxy
scrapoxy init conf.json
```

Open `conf.json`.
Fill your own `password` in `commander` section.
Fill `accessKeyId`, `secretAccessKey` and `region` by your AWS credentials and parameters.

```
scrapoxy start conf.json -d
```

Open the GUI: `localhost:8889`
Interact with Scrapoxy through our scraper: `localhost:8888`

### Test
Wait for 3 minutes.
`scrapoxy test http://localhost:8888` or `curl --proxy http://127.0.0.1:8888 http://apo.ipify.org`


## Integrate with scrapy

```
apt-get install python-dev libxml2-dev libxslt1-dev libffi-dev
pip install scrapy scrapoxy
```

Edit scrapy setting at `<project_path>/settings.py`:
```
CONCURRENT_REQUESTS_PER_DOMAIN = 1
RETRY_TIMES = 0

# PROXY
PROXY = 'http://127.0.0.1:8888/?noconnect'

# SCRAPOXY
API_SCRAPOXY = 'http://127.0.0.1:8889/api'
API_SCRAPOXY_PASSWORD = 'CHANGE_THIS_PASSWORD'

DOWNLOADER_MIDDLEWARES = {
    'scrapoxy.downloadmiddlewares.proxy.ProxyMiddleware': 100,
    'scrapoxy.downloadmiddlewares.wait.WaitMiddleware': 101,
    'scrapoxy.downloadmiddlewares.scale.ScaleMiddleware': 102,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
}
```

	- PrixyMiddleware relays