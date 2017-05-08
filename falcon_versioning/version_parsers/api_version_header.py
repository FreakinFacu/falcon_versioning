def parse_api_version_header(req):
    if "API-VERSION" in req.headers:
        return req.headers["API-VERSION"]
    return None
