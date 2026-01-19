"""
Utility functions for Lambda function
"""
import json
import re
from typing import Any, Dict
from datetime import datetime


def create_response(status_code: int, body: Any, headers: Dict[str, str] = None) -> Dict:
    """Create a properly formatted API Gateway response."""
    default_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    }
    
    if headers:
        default_headers.update(headers)
    
    return {
        "statusCode": status_code,
        "headers": default_headers,
        "body": json.dumps(body, default=str),
    }


def parse_request_body(event: Dict) -> Dict:
    """Parse the request body from API Gateway event (supports both v1 and v2 formats)."""
    body = event.get("body", "{}")
    
    # Handle base64 encoded body (common in API Gateway v2)
    if event.get("isBase64Encoded", False) and body:
        import base64
        body = base64.b64decode(body).decode('utf-8')
    
    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {}
    return body or {}


def get_http_method(event: Dict) -> str:
    """Get HTTP method from API Gateway event (supports both v1 and v2 formats)."""
    # v2 format
    if "requestContext" in event and "http" in event.get("requestContext", {}):
        return event["requestContext"]["http"].get("method", "GET")
    # v1 format
    return event.get("httpMethod", "GET")


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug[:100]


def generate_filename(topic: str, category: str) -> str:
    """Generate a filename for the HTML page."""
    topic_slug = slugify(topic)
    return f"{topic_slug}-{category}.html"


def get_current_timestamp() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.utcnow().isoformat()
