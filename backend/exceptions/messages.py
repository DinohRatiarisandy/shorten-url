MESSAGES = {
    404: "This link doesn't exist or has expired.",
    409: "This alias is already taken.",
    400: "Bad request.",
    500: "Internal server error.",
}


def make_error_page(status_code: int, message: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{status_code} - Error</title>
        <style>
            body {{ font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; background: #f9fafb; }}
            h1 {{ font-size: 4rem; margin: 0; }}
            p {{ color: #6b7280; }}
        </style>
    </head>
    <body>
        <h1>🔗 {status_code}</h1>
        <p>{message}</p>
    </body>
    </html>
    """
