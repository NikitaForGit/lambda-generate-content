# Configuration for Lambda function

# Category configurations with prompts for content generation
CATEGORY_CONFIG = {
    "facts": {
        "name": "Facts",
        "description": "Interesting statistics and factual information",
        "prompt_template": """Write an engaging article about interesting facts related to "{topic}". 
Include:
- 7-10 fascinating and verified facts
- Statistics and numbers where relevant
- Brief explanations for each fact
- Why these facts matter

Write in an informative but engaging blog style. Use headers to organize the content."""
    },
    "history": {
        "name": "History",
        "description": "Historical background and evolution",
        "prompt_template": """Write a comprehensive article about the history of "{topic}".
Include:
- Origins and early development
- Key milestones and turning points
- Important figures or organizations involved
- Timeline of major events
- How it evolved to its current state

Write in an engaging narrative style suitable for a blog article. Use headers to organize chronologically."""
    },
    "future_analysis": {
        "name": "Future Analysis",
        "description": "Predictions and trend forecasting",
        "prompt_template": """Write an analytical article about the future of "{topic}".
Include:
- Current trends and trajectory
- Expert predictions and forecasts
- Potential developments in 5-10 years
- Challenges and opportunities ahead
- Factors that could influence the future

Write in an analytical yet accessible blog style. Use headers to organize predictions by timeframe or theme."""
    },
    "how_it_works": {
        "name": "How It Works",
        "description": "Technical/scientific explanation",
        "prompt_template": """Write an explanatory article about how "{topic}" works.
Include:
- Basic principles and concepts
- Step-by-step explanation of key processes
- Technical details made accessible
- Real-world examples and analogies
- Common misconceptions clarified

Write in an educational blog style that makes complex topics understandable. Use headers to break down concepts."""
    },
    "comparisons": {
        "name": "Comparisons",
        "description": "Compare with alternatives/competitors",
        "prompt_template": """Write a comparative analysis article about "{topic}" and its alternatives or competitors.
Include:
- Overview of main options/alternatives
- Key differences and similarities
- Pros and cons of each
- Use cases where each excels
- Recommendations for different scenarios

Write in an objective, balanced blog style. Use comparison tables or lists where helpful."""
    },
    "common_myths": {
        "name": "Common Myths",
        "description": "Debunking misconceptions",
        "prompt_template": """Write a myth-busting article about common misconceptions regarding "{topic}".
Include:
- 5-8 common myths or misconceptions
- The truth behind each myth
- Why these misconceptions exist
- Evidence and facts that debunk them
- What people should know instead

Write in an engaging, enlightening blog style. Use clear myth vs. reality formatting."""
    },
    "getting_started": {
        "name": "Getting Started",
        "description": "Practical beginner's guide",
        "prompt_template": """Write a comprehensive beginner's guide to "{topic}".
Include:
- What beginners need to know first
- Step-by-step getting started instructions
- Essential tools, resources, or requirements
- Common beginner mistakes to avoid
- Next steps after the basics

Write in a friendly, encouraging blog style perfect for newcomers. Use numbered steps and clear headers."""
    }
}
