failed=0

for f in test_valid.py test_edge.py; do
    echo "===== $f ====="
    python "$f" || failed=1
    echo
done

if [ "$failed" -eq 0 ]; then
    echo "ALL TEST CASES PASSED"
else
    echo "ONE OR MORE TEST CASES FAILED"
fi
    exit "$failed"