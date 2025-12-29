#!/usr/bin/env python3
"""Cloud Sync on /continue (v3.1) - Multi-device workflow"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Fix Windows encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def cloud_sync():
    config_file = Path.home() / ".claude-memory" / ".config.json"
    
    if not config_file.exists():
        return
    
    try:
        with open(config_file) as f:
            config = json.load(f)
        
        cloud_path = config.get("cloud_path", "")
        sync_enabled = config.get("sync_enabled", False)
        
        if not sync_enabled or not cloud_path:
            return
        
        # Expand tilde
        cloud_path_expanded = os.path.expanduser(cloud_path)
        
        if not Path(cloud_path_expanded).exists():
            print(f"[WARN] Cloud path not found: {cloud_path}")
            print("Continuing with local memory only...")
            return
        
        print("[SYNC] Syncing with cloud memory...")
        orig_dir = os.getcwd()
        os.chdir(cloud_path_expanded)
        
        try:
            # Fetch from remote
            subprocess.run(["git", "fetch", "origin"], 
                          stderr=subprocess.DEVNULL, check=False)
            
            # Check if behind
            local = subprocess.run(["git", "rev-parse", "@"], 
                                  capture_output=True, text=True, check=False).stdout.strip()
            remote = subprocess.run(["git", "rev-parse", "@{u}"], 
                                   capture_output=True, text=True, check=False).stdout.strip()
            
            if local and remote and local != remote:
                print("[PULL] Pulling updates from other devices...")
                
                result = subprocess.run(["git", "pull", "--rebase", "origin", "main"],
                                       capture_output=True, text=True, check=False)
                
                if result.returncode == 0:
                    print("[OK] Cloud memory synced!")
                else:
                    print("[CONFLICT] Conflict detected. Resolve manually:")
                    print(f"   cd {cloud_path_expanded}")
                    print("   git rebase --abort  # Skip sync")
                    print("   git pull --no-rebase  # Merge instead")
            else:
                print("[OK] Cloud memory up-to-date")
        finally:
            os.chdir(orig_dir)
            
    except Exception as e:
        print(f"[ERROR] Cloud sync error: {e}")
        print("Continuing with local memory...")

if __name__ == "__main__":
    cloud_sync()
