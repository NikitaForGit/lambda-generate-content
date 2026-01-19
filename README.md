# lambda-generate-content

AWS Lambda function that generates AI-powered content using Amazon Bedrock and saves to S3.

## API Endpoint

**POST** `/generate`

Generate content for topics in specified categories.

**Request Body:**
```json
{
  "topics": ["Artificial Intelligence", "Machine Learning"],
  "categories": ["facts", "history", "future_analysis"]
}
```

**Response:**
```json
{
  "success": true,
  "generated": [
    {
      "topic": "Artificial Intelligence",
      "category": "facts",
      "output_path": "output/artificial-intelligence-facts.html",
      "created_at": "2026-01-19T12:00:00"
    }
  ],
  "failed": [],
  "total_generated": 1,
  "message": "Successfully generated 1 pages."
}
```

## Features

- **AI Content Generation** - Uses Amazon Bedrock (Amazon Nova Lite) to generate high-quality articles
- **Multiple Categories** - Supports 7 different content categories (facts, history, future analysis, how it works, comparisons, common myths, getting started)
- **HTML Output** - Generates complete, styled HTML pages ready for publishing
- **S3 Storage** - Automatically saves generated content to S3
- **Meta Descriptions** - Generates SEO-optimized meta descriptions
- **Error Handling** - Gracefully handles failures and reports them

## Structure

```
.
├── src/
│   ├── handler.py      # Lambda handler function
│   ├── config.py       # Category configurations
│   ├── utils.py        # Helper functions (CORS, response formatting, slugify)
│   └── templates.py    # HTML page template
├── tests/              # Unit tests (if any)
├── .circleci/
│   └── config.yml      # CI/CD pipeline
├── requirements.txt    # Python dependencies (boto3)
└── README.md
```

## Environment Variables

This Lambda requires the following environment variables (set by Terraform):

- `OUTPUT_BUCKET_NAME` - S3 bucket where generated HTML files are saved
- `BEDROCK_MODEL_ID` - Bedrock model ID (default: amazon.nova-lite-v1:0)
- `ENVIRONMENT` - Environment name (prod, staging)

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

## Deployment

### Automatic (via CircleCI)

Commits to `main` or `master` trigger:
1. **Lint & Test** - Code quality checks
2. **Build** - Creates deployment package with boto3
3. **Deploy** - Uploads to S3 and updates Lambda function

### CircleCI Environment Variables

- `AWS_ROLE_ARN` - IAM role for AWS CLI
- `AWS_REGION` - AWS region (e.g., us-east-1)
- `LAMBDA_ARTIFACTS_BUCKET` - S3 bucket for deployment artifacts
- `PROJECT_NAME` - Project name prefix
- `ENVIRONMENT` - Environment name (prod, staging)

## Content Categories

The function supports these categories (defined in `src/config.py`):

1. **facts** - Interesting statistics and factual information
2. **history** - Historical background and evolution
3. **future_analysis** - Predictions and trend forecasting
4. **how_it_works** - Technical/scientific explanation
5. **comparisons** - Compare with alternatives/competitors
6. **common_myths** - Debunking misconceptions
7. **getting_started** - Practical beginner's guide

Each category has a custom prompt template optimized for that content type.

## AWS Permissions Required

This Lambda needs:
- **Bedrock** - `bedrock:InvokeModel` permission
- **S3** - `s3:PutObject` permission on OUTPUT_BUCKET_NAME

## Output Format

Generated HTML files are saved to S3 with:
- Path: `output/{topic-slug}-{category}.html`
- Content-Type: `text/html`
- Cache-Control: `public, max-age=86400`
- Fully styled, responsive HTML page ready to serve
