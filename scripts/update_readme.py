import os
import re
from datetime import datetime

def main():
    # Get the API response from environment variable
    api_response = os.environ.get('API_RESPONSE', '')
    
    print("=== GitHub Action Debug ===")
    print("API Response length:", len(api_response))
    print("API Response preview:", api_response[:200] + "..." if len(api_response) > 200 else api_response)
    
    # Extract stats from your API response format
    contributions_match = re.search(r'Total contributions.*?: (\d+)', api_response)
    streak_match = re.search(r'Current streak: (\d+) days', api_response)
    last_active_match = re.search(r'Last active day: (\d{4}-\d{2}-\d{2})', api_response)
    
    # Use extracted values or defaults
    contributions = contributions_match.group(1) if contributions_match else "0"
    streak = streak_match.group(1) if streak_match else "0"
    last_active = last_active_match.group(1) if last_active_match else "N/A"
    
    print(f"Parsed - Contributions: {contributions}, Streak: {streak}, Last Active: {last_active}")
    
    # Read current README
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        print("README.md not found, creating basic one")
        readme_content = "# Norizara\n\n<!-- STATS_START --><!-- STATS_END -->"
    
    # Create new stats section
    new_stats_section = f"""<!-- STATS_START -->
## 📈 Live GitHub Stats

**🔥 Current Streak:** {streak} days  
**📅 Last 30 Days:** {contributions} contributions  
**⚡ Last Active:** {last_active}  

*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*
<!-- STATS_END -->"""
    
    # Replace or add the stats section
    if '<!-- STATS_START -->' in readme_content and '<!-- STATS_END -->' in readme_content:
        # Replace existing section
        start_tag = '<!-- STATS_START -->'
        end_tag = '<!-- STATS_END -->'
        start_index = readme_content.find(start_tag)
        end_index = readme_content.find(end_tag) + len(end_tag)
        
        updated_readme = readme_content[:start_index] + new_stats_section + readme_content[end_index:]
    else:
        # Add new section at the beginning
        updated_readme = new_stats_section + "\n\n" + readme_content
    
    # Write updated README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(updated_readme)
    
    print("README updated successfully!")
    print("=== Debug Complete ===")

if __name__ == "__main__":
    main()