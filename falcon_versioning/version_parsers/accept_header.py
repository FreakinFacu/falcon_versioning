def parse_accept_header(req):
    if "ACCEPT" in req.headers:
        accept = req.headers['ACCEPT']
        parts = accept.split(";")

        for part in parts:
            values = part.split("=")
            if values[0].lower() == "version":
                return values[1]
    return None
