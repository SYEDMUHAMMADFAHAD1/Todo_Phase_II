#!/bin/bash

EMAIL="test_debug_$(date +%s)@example.com"
PASSWORD="TestPassword123!"
API="http://localhost:8000/api"

# Sign up
SIGNUP=$(curl -s -X POST "$API/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\",\"name\":\"Debug User\"}")

TOKEN=$(echo "$SIGNUP" | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])" 2>/dev/null)

echo "Token: ${TOKEN:0:50}..."

# Create todo with full response
echo ""
echo "Creating todo..."
curl -i -X POST "$API/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Test Todo","description":"This is a test"}'
