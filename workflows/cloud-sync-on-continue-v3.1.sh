#!/usr/bin/env bash
# Cloud Sync on /continue (v3.1)
# Non-blocking cloud memory sync for multi-device workflow

config_file=~/.claude-memory/.config.json

if [ -f "$config_file" ]; then
    # Read config (matches actual .config.json structure)
    cloud_path=$(jq -r '.cloud_path // empty' "$config_file")
    sync_enabled=$(jq -r '.sync_enabled // false' "$config_file")

    if [ "$sync_enabled" = "true" ] && [ -n "$cloud_path" ]; then
        # Expand tilde
        cloud_path_expanded="${cloud_path/#\~/$HOME}"
        
        echo "🔄 Syncing with cloud memory..."

        if cd "$cloud_path_expanded" 2>/dev/null; then
            # Pull latest from cloud (multi-device sync)
            git fetch origin 2>/dev/null

            # Check if we're behind
            LOCAL=$(git rev-parse @ 2>/dev/null)
            REMOTE=$(git rev-parse @{u} 2>/dev/null)

            if [ -n "$LOCAL" ] && [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
                echo "📥 Pulling updates from other devices..."

                # Pull with rebase (preserve local uncommitted work)
                if git pull --rebase origin main 2>/dev/null; then
                    echo "✅ Cloud memory synced!"
                else
                    echo "⚠️ Conflict detected. Resolve manually:"
                    echo "   cd $cloud_path_expanded"
                    echo "   git rebase --abort  # Skip sync"
                    echo "   git pull --no-rebase  # Merge instead"
                fi
            else
                echo "✅ Cloud memory up-to-date"
            fi

            cd - >/dev/null
        else
            echo "⚠️ Cloud path not found: $cloud_path"
            echo "Continuing with local memory only..."
        fi
    fi
fi
