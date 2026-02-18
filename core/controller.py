import os
import json
import argparse

DRIVERS_DIR = "/Users/pillar/clawd/auto-web/drivers"

def load_platform_config(platform):
    json_path = os.path.join(DRIVERS_DIR, f"{platform}.json")
    js_path = os.path.join(DRIVERS_DIR, f"{platform}.js")
    
    if not os.path.exists(json_path) or not os.path.exists(js_path):
        raise Exception(f"Driver for platform '{platform}' not found.")
        
    with open(json_path, 'r') as f:
        config = json.load(f)
    
    with open(js_path, 'r') as f:
        js_code = f.read()
        
    return config, js_code

def generate_injection_payload(platform, message):
    config, js_code = load_platform_config(platform)
    
    # Wrap the driver code and the execution call
    payload = f"""
{js_code}

(async () => {{
    try {{
        console.log("Auto-Web: Starting interaction for {platform}");
        const result = await window.autoWeb_{platform}.sendPrompt("{message}");
        return JSON.stringify(result);
    }} catch (e) {{
        return JSON.stringify({{ error: e.message }});
    }}
}})();
"""
    return payload

def main():
    parser = argparse.ArgumentParser(description="Auto-Web Controller")
    parser.add_argument("--platform", required=True, help="Target platform (doubao, gemini, xyq)")
    parser.add_argument("--message", required=True, help="Prompt message to send")
    
    args = parser.parse_args()
    
    try:
        payload = generate_injection_payload(args.platform, args.message)
        # We print the payload so the Agent can copy it into browser.act(type="eval")
        print("--- INJECTION PAYLOAD START ---")
        print(payload)
        print("--- INJECTION PAYLOAD END ---")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
