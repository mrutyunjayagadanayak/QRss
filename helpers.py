from urllib.parse import urlparse

def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False