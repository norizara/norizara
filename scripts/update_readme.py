import os
import re
from datetime import datetime

def main():
    # Get the API response from environment variable
    api_response = os.environ.get('API_RESPONSE', '')
    
    print("API Response received:")
    print(api_response[:500] + "..." if len(api_response) > 500 else api_response)
    
    # Extract stats from your API response
    streak_match = re.search(r'Current streak: (\d+) days', api_response)
    contributions_match = re.search(r'Total contributions.*?: (\d+)', api_response)
    last_active_match = re.search(r'Last active day: (\d{4}-\d{2}-\d{2})', api_response)
    
    # Default values if parsing fails
    streak = streak_match.group(1) if streak_match else "0"
    contributions = contributions_match.group(1) if contributions_match else "0"
    last_active = last_active_match.group(1) if last_active_match else "N/A"
    
    print(f"Parsed - Streak: {streak}, Contributions: {contributions}, Last Active: {last_active}")
    
    # Read current README
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Define the stats section pattern
    stats_pattern = r'<!-- STATS_START -->.*?<!-- STATS_END -->'
    
    # Create new stats section
    new_stats_section = f"""<!-- STATS_START -->
## 📈 Live GitHub Stats

| Metric | Value | Last Updated |
|--------|-------|--------------|
| **🔥 Current Streak** | `{streak} days` | {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} |
| **📅 Last 30 Days** | `{contributions} contributions` | [View Details](https://gitcommittracker.up.railway.app/norizara) |
| **⚡ Last Active** | `{last_active}` | Auto-updated daily |

<!-- STATS_END -->"""
    
    # Replace or add the stats section
    if re.search(stats_pattern, readme_content, re.DOTALL):
        # Replace existing section
        updated_readme = re.sub(stats_pattern, new_stats_section, readme_content, flags=re.DOTALL)
    else:
        # Add new section at the top
        updated_readme = new_stats_section + "\n\n" + readme_content
    
    # Write updated README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(updated_readme)
    
    print("README updated successfully!")

if __name__ == "__main__":
    main()