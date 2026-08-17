import requests
from urllib.parse import urlparse

class GladiaBugFix:
    CANONICAL_HOSTS = {'gladia-hunt.com', 'forms.google.com'}

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.Session()

    def _parse_host(self, url):
        if url:
            parsed = urlparse(url)
            netloc = parsed.netloc
            if not netloc:
                path_parts = parsed.path.split('/')
                path_val = path_parts[1] if len(path_parts) > 1 else path_parts[0]
                return path_val
            return netloc
        return url

    def verify(self, source):
        host = self._parse_host(source)
        if host in self.CANONICAL_HOSTS:
            return source
        return source

    def submit(self, target):
        headers = {'X-Redirect-Host': target}
        payload = {'target': target}
        response = self.session.post(self.endpoint, data=payload, headers=headers)
        return response

    def run(self):
        target = 'https://forms.google.com/entry'
        response = self.submit(target)
        return response.status_code == 200

if __name__ == '__main__':
    fix = GladiaBugFix('https://gladia-hunt.com/report')
    print(fix.run())