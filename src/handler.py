"""
Lambda function: Generate Content
Generates content using Amazon Bedrock (Claude 3 Haiku) and saves to S3.
"""
import json
import os
from typing import Dict
from datetime import datetime

import boto3

from config import CATEGORY_CONFIG
from utils import create_response, parse_request_body, generate_filename, get_http_method
from templates import render_html_page


# Initialize AWS clients
bedrock_runtime = boto3.client('bedrock-runtime')
s3_client = boto3.client('s3')

# Configuration from environment
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET_NAME', '')
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-haiku-20240307-v1:0')


def generate_with_bedrock(prompt: str) -> str:
    """Generate content using Amazon Bedrock Claude 3 Haiku."""
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    
    response = bedrock_runtime.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=body
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']


def generate_content(topic: str, category: str) -> Dict:
    """Generate content for a topic and category."""
    
    if category not in CATEGORY_CONFIG:
        raise ValueError(f"Unknown category: {category}")
    
    category_config = CATEGORY_CONFIG[category]
    
    # Build the prompt
    prompt = category_config['prompt_template'].format(topic=topic)
    prompt += """

Format the article in clean HTML suitable for a blog post. Include:
- A compelling <h1> title
- Use <h2> and <h3> for section headers
- Use <p> tags for paragraphs
- Use <ul>/<ol> and <li> for lists where appropriate
- Use <strong> and <em> for emphasis
- Do NOT include <html>, <head>, or <body> tags - just the article content
- Make the content engaging, well-researched, and approximately 800-1200 words"""

    # Generate content
    content = generate_with_bedrock(prompt)
    
    # Generate meta description
    meta_prompt = f"""Write a compelling meta description (150-160 characters) for a blog article about "{topic}" focusing on {category_config['name'].lower()}. 
The description should be engaging and include the main keyword. Return ONLY the meta description text, nothing else."""
    
    meta_description = generate_with_bedrock(meta_prompt).strip()[:160]
    
    return {
        'content': content,
        'meta_description': meta_description,
        'category_name': category_config['name'],
    }


def save_to_s3(topic: str, category: str, content: str, meta_description: str, category_name: str) -> str:
    """Save generated HTML to S3 and return the key."""
    
    html = render_html_page(
        topic=topic,
        category=category,
        category_name=category_name,
        content=content,
        meta_description=meta_description,
    )
    
    filename = generate_filename(topic, category)
    key = f"output/{filename}"
    
    s3_client.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=key,
        Body=html.encode('utf-8'),
        ContentType='text/html',
        CacheControl='public, max-age=86400',
    )
    
    return key


def handler(event, context):
    """
    Lambda handler for generating content.
    
    POST /generate
    Body: {
        "topics": ["topic1", "topic2"],
        "categories": ["facts", "history"]
    }
    
    Returns: {
        "success": true,
        "generated": [...],
        "failed": [...]
    }
    """
    # Handle OPTIONS for CORS
    method = get_http_method(event)
    if method == 'OPTIONS':
        return create_response(200, {})
    
    if method != 'POST':
        return create_response(405, {'error': 'Method not allowed'})
    
    body = parse_request_body(event)
    
    topics = body.get('topics', [])
    categories = body.get('categories', [])
    
    if not topics:
        return create_response(400, {'error': 'At least one topic is required'})
    
    if not categories:
        return create_response(400, {'error': 'At least one category is required'})
    
    # Validate categories
    invalid_categories = [c for c in categories if c not in CATEGORY_CONFIG]
    if invalid_categories:
        return create_response(400, {'error': f'Invalid categories: {invalid_categories}'})
    
    if not OUTPUT_BUCKET:
        return create_response(500, {'error': 'OUTPUT_BUCKET_NAME not configured'})
    
    generated = []
    failed = []
    
    for topic in topics:
        for category in categories:
            try:
                # Generate content
                result = generate_content(topic, category)
                
                # Save to S3
                s3_key = save_to_s3(
                    topic=topic,
                    category=category,
                    content=result['content'],
                    meta_description=result['meta_description'],
                    category_name=result['category_name'],
                )
                
                generated.append({
                    'topic': topic,
                    'category': category,
                    'output_path': s3_key,
                    'created_at': datetime.utcnow().isoformat(),
                })
                
            except Exception as e:
                failed.append({
                    'topic': topic,
                    'category': category,
                    'error': str(e),
                })
    
    return create_response(200, {
        'success': len(failed) == 0,
        'generated': generated,
        'failed': failed,
        'total_generated': len(generated),
        'message': f"Generated {len(generated)} pages. {len(failed)} failed." if failed else f"Successfully generated {len(generated)} pages.",
    })
