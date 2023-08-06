import base64
import hashlib
import hmac


def generate_signature(
        http_method: str,
        path: str,
        query_string: str,
        access_token: str,
        timestamp: int,
        request_body: str,
        signing_key: str
) -> str:
    body_hash = _base64_encode(_sha256(request_body))
    string_to_sign = ":".join(
        [
            http_method,
            path,
            query_string,
            access_token,
            str(timestamp),
            body_hash,
        ]
    )

    return _base64_encode(_hmac_sha256(signing_key, string_to_sign))


def _base64_encode(text: bytes) -> str:
    return base64.b64encode(text).decode()


def _sha256(text: str) -> bytes:
    return hashlib.sha256(text.encode()).digest()


def _hmac_sha256(signing_key: str, text: str) -> bytes:
    return hmac.new(signing_key.encode(), text.encode(), hashlib.sha256).digest()
