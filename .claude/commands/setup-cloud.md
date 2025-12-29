---
name: setup-cloud
description: "Enable cloud sync for multi-device memory access"
version: 1.0
---

# Setup Cloud Memory Sync

**Purpose**: Configure optional cloud sync to access memories from multiple devices

---

## Prerequisites Check

Agent should verify:

```bash
# 1. Check if git is configured
git config --global user.name
git config --global user.email

# If not configured:
echo "Git not configured. Please run:"
echo "  git config --global user.name 'Your Name'"
echo "  git config --global user.email 'your.email@example.com'"
exit 1

# 2. Check if already configured
if [ -d ~/.claude-memory-cloud ]; then
  echo "Cloud sync already configured!"
  echo "Cloud repo: $(cd ~/.claude-memory-cloud && git remote get-url origin)"
  exit 0
fi
```

---

## Interactive Setup

Agent prompts user:

```
🌐 Cloud Memory Setup

Cloud sync lets you:
✅ Access memories from any device
✅ Never lose context when switching machines
✅ Sync sessions across desktop, laptop, mobile

Requirements:
- A private Git repository (GitHub, GitLab, Gitea, etc.)
- Git configured on this machine ✅

Git configuration:
  User: {git_user}
  Email: {git_email}

Do you have a cloud memory repository already?
[1] Yes, I have a repo (clone existing)
[2] No, I need to create one (initialize new)
[3] Cancel

Choice:
```

---

## Option 1: Clone Existing Repo

User already set up cloud on another device.

```
You selected: Clone existing repository

This will download your memories from another device.

Enter your repository URL:
Examples:
  - https://github.com/username/claude-memory-cloud.git
  - git@github.com:username/my-memories.git
  - https://gitlab.com/username/memories.git

URL: {user_input}

Cloning...
$ git clone {url} ~/.claude-memory-cloud

✅ Repository cloned!
✅ Found {X} devices
✅ Last sync: {timestamp}

Updating config...
✅ Cloud sync enabled!

Your memories from other devices are now available.
Use /continue to see what you worked on elsewhere.
```

---

## Option 2: Initialize New Repo

First device setup.

```
You selected: Initialize new repository

I'll create the cloud memory structure for you.

Creating structure...
├── global/               ✅
├── devices/              ✅
├── projects/             ✅
├── providers/            ✅
├── sync/                 ✅
└── integration/          ✅

Initializing git...
$ git init ~/.claude-memory-cloud
$ git add .
$ git commit -m "Initial commit - Cloud Memory v2.3"

✅ Cloud memory initialized!

Next steps:
1. Create a PRIVATE repository at your git provider:
   - GitHub: https://github.com/new
   - GitLab: https://gitlab.com/projects/new
   - Or use your own git server

2. Name it whatever you want (e.g., "claude-memory-cloud")

3. Run these commands to link and push:

   cd ~/.claude-memory-cloud
   git remote add origin YOUR_REPO_URL
   git push -u origin main

4. When done, cloud sync will be active!

Want me to guide you through creating a GitHub repo? (y/N):
```

**If yes**:
```
Opening GitHub...
1. Go to: https://github.com/new
2. Repository name: claude-memory-cloud (or any name)
3. Visibility: PRIVATE ⚠️ (important for privacy!)
4. Don't add README, .gitignore, or license
5. Click "Create repository"

Once created, paste the URL here: {user_input}

Linking repository...
$ cd ~/.claude-memory-cloud
$ git remote add origin {url}
$ git push -u origin main

✅ Pushed to cloud!
✅ Cloud sync enabled!

Your memories are now backed up and accessible from other devices.
```

---

## Update Config

After successful setup:

```python
# Update ~/.claude-memory/.config.json
config = {
    "version": "2.3",
    "sync_enabled": True,
    "cloud_repo": user_provided_url,
    "cloud_path": "~/.claude-memory-cloud",
    "device_name": "laptop-work",  # or ask user
    "providers": ["claude"],
    "sync": {
        "on_session_start": True,
        "on_session_end": True,
        "auto_commit": True,
        "conflict_resolution": "latest-timestamp"
    },
    "privacy": {
        "redact_pii": True,
        "auto_redact": ["email", "phone", "address"],
        "cloud_safe_only": False
    }
}
```

---

## Register Device

Add this device to device registry:

```bash
cd ~/.claude-memory-cloud

# Create device entry
mkdir -p devices/laptop-work
cat > devices/laptop-work/info.md << 'EOF'
# Device: laptop-work

**Type**: Laptop
**OS**: Windows 11
**First Seen**: 2025-12-26
**Primary Use**: Work projects (Golfleet)

**Capabilities**:
- Claude CLI ✅
- LMStudio ❌
- Git ✅

**Notes**:
Work machine, fast SSD, good for development.
EOF

# Update registry
cat > sync/device-registry.json << 'EOF'
{
  "devices": {
    "laptop-work": {
      "type": "laptop",
      "os": "windows",
      "first_seen": "2025-12-26T15:30:00Z",
      "last_seen": "2025-12-26T15:30:00Z",
      "providers": ["claude"]
    }
  }
}
EOF

git add .
git commit -m "Register device: laptop-work"
git push
```

---

## Success Message

```
✅ Cloud memory setup complete!

Configuration:
  Device: laptop-work
  Cloud repo: {url}
  Sync: Enabled (auto on start/end)

What happens now:
- On /start: Pulls latest from cloud (gets updates from other devices)
- During session: Works with local memory (fast)
- On /end: Pushes to cloud (shares this session)

You can:
- Add more devices anytime (they'll auto-sync)
- Disable sync with /disable-cloud
- View sync status with /sync-status

Next: Use /start to begin your first synced session!
```

---

## Error Handling

### Git Not Configured
```
⚠️ Git is not configured on this machine.

Please run:
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"

Then try /setup-cloud again.
```

### Invalid URL
```
⚠️ Invalid repository URL: {url}

Valid examples:
  ✅ https://github.com/username/repo.git
  ✅ git@github.com:username/repo.git
  ✅ https://gitlab.com/username/repo.git

Try again with a valid URL.
```

### Clone Failed
```
⚠️ Failed to clone repository.

Possible reasons:
1. Repository doesn't exist
2. Repository is private and you don't have access
3. Network issue

Error: {git_error}

Fix and try again, or choose option [2] to initialize new repo.
```

### Push Failed
```
⚠️ Failed to push to cloud.

This might mean:
1. Repository doesn't exist (create it first)
2. No permission (check repository access)
3. Network issue

Error: {git_error}

Fix and run:
  cd ~/.claude-memory-cloud
  git push -u origin main
```

---

## Agent Behavior

**On /setup-cloud execution**:

1. ✅ Check prerequisites (git config)
2. ✅ Check if already configured (skip if yes)
3. ✅ Present options (clone vs initialize)
4. ✅ Execute chosen option
5. ✅ Update config file
6. ✅ Register device
7. ✅ Confirm success
8. ✅ Guide next steps

**Important**:
- Never assume git provider (support any)
- Never hardcode URLs
- Always verify success before updating config
- Handle errors gracefully
- Provide clear next steps

---

**End of Setup Guide**
