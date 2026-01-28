#!/bin/bash
# Wait for Phase 1.3 to complete, then run 1.4 and 1.5

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_ROOT/data"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"
LOG_DIR="$PROJECT_ROOT/logs"

echo "=== Waiting for Phase 1.3 to complete ==="
while true; do
    BATCH_COUNT=$(ls $DATA_DIR/votes/batch_*.json 2>/dev/null | wc -l | tr -d ' ')
    echo "$(date): $BATCH_COUNT/112 batches"
    
    if [ "$BATCH_COUNT" -ge 112 ]; then
        echo "Phase 1.3 complete!"
        break
    fi
    sleep 30
done

echo ""
echo "=== Running Phase 1.4: Aggregate Party Positions ==="
cd "$PROJECT_ROOT"
python3 $SCRIPTS_DIR/aggregate_positions.py 2>&1 | tee $LOG_DIR/phase_1_4_log.txt

echo ""
echo "=== Running Phase 1.5: Detect AMPAYs ==="
python3 $SCRIPTS_DIR/detect_ampays.py --all 2>&1 | tee $LOG_DIR/phase_1_5_log.txt

echo ""
echo "=== All phases complete ==="
echo "Final files:"
ls -la $DATA_DIR/*.json
