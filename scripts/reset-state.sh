#!/usr/bin/env sh
# Resets state.json so next run posts fresh Discord messages
echo '{}' > "$(dirname "$0")/../state.json"
echo "state.json reset to {}"
