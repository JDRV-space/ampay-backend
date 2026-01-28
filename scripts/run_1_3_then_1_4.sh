#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_ROOT/logs"
DATA_DIR="$PROJECT_ROOT/data"

echo "=== Monitoring Phase 1.3 ==="
while true; do
    BATCHES=$(ls $DATA_DIR/votes/batch_*.json 2>/dev/null | wc -l | tr -d ' ')
    echo "$(date +%H:%M:%S): $BATCHES/112 batches"
    
    if [ "$BATCHES" -ge 112 ]; then
        echo "Phase 1.3 complete!"
        break
    fi
    sleep 30
done

echo ""
echo "=== Running Phase 1.4 ==="
cd "$PROJECT_ROOT"
python3 scripts/aggregate_positions.py 2>&1 | tee $LOG_DIR/phase_1_4_full.log

echo ""
echo "=== DONE ==="
echo "Files created:"
ls -la $DATA_DIR/votes_categorized.json $DATA_DIR/party_positions.json
