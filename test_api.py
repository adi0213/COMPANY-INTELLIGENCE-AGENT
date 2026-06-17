import sys, json, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

# Quick health check
try:
    req = urllib.request.Request('http://localhost:8000/api/v1/health')
    with urllib.request.urlopen(req, timeout=5) as resp:
        print('Backend health:', resp.read().decode())
except Exception as e:
    print(f'Backend not ready: {e}')
    sys.exit(1)

# Test the analyze endpoint
print('Testing analyze endpoint with Amazon...')
data = json.dumps({'company': 'Amazon'}).encode()
req = urllib.request.Request(
    'http://localhost:8000/api/v1/company/analyze', 
    data=data, 
    headers={'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read().decode())
        print(f'Company: {result.get("company")}')
        
        for section in ['overview', 'key_technologies', 'executive_summary', 'salary_insights']:
            sec_data = result.get(section, {})
            if isinstance(sec_data, dict):
                content = sec_data.get('content', '')
                confidence = sec_data.get('confidence', 'N/A')
            else:
                content = str(sec_data)
                confidence = 'N/A'
            
            print(f'\n=== {section.upper()} ===')
            print(f'Confidence: {confidence}')
            print(f'Length: {len(content)} chars')
            print(f'Preview: {content[:250]}...')
            
            # Check for old bad patterns
            bad = ['No formal description', 'no data available', 'Compensation benchmarks for Software']
            for pat in bad:
                if pat in content:
                    print(f'  *** FOUND OLD PATTERN: "{pat}" ***')
                    
except Exception as e:
    print(f'Analyze failed: {e}')
