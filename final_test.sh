#!/bin/bash

API="http://localhost:8000/api"

echo "=========================================="
echo "FINAL TODO CREATION TEST"
echo "=========================================="
echo ""

# 1. Signup
echo "[1] SIGNUP TEST"
SIGNUP=$(curl -s -X POST "$API/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"finaltest_$(date +%s)@test.com\",\"password\":\"Pass123456\",\"name\":\"TestUser\"}")

TOKEN=$(echo "$SIGNUP" | grep -oP '"token":"?\K[^"]*' | head -1)

if [ -z "$TOKEN" ]; then
  echo "❌ FAILED: Could not get token"
  echo "Response: $SIGNUP"
  exit 1
fi

echo "✅ PASSED"
echo "   Token: ${TOKEN:0:50}..."
echo ""

# 2. Create Todo
echo "[2] CREATE TODO TEST"
TODO_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Buy coffee supplies for the office","description":"Get espresso beans, milk, and filters from supplier"}')

HTTP_CODE=$(echo "$TODO_RESPONSE" | tail -1)
BODY=$(echo "$TODO_RESPONSE" | head -n -1)

echo "   HTTP Status: $HTTP_CODE"

if [ "$HTTP_CODE" = "201" ]; then
  echo "✅ PASSED"
  TODO_ID=$(echo "$BODY" | grep -oP '"id":"?\K[^"]*' | head -1)
  echo "   Todo ID: $TODO_ID"
  echo "   Body: $BODY"
else
  echo "❌ FAILED"
  echo "   Response: $BODY"
  exit 1
fi

echo ""

# 3. Fetch Todos
echo "[3] FETCH TODOS TEST"
FETCH_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$API/tasks" \
  -H "Authorization: Bearer $TOKEN")

HTTP_CODE=$(echo "$FETCH_RESPONSE" | tail -1)
BODY=$(echo "$FETCH_RESPONSE" | head -n -1)

echo "   HTTP Status: $HTTP_CODE"

if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ PASSED"
  COUNT=$(echo "$BODY" | grep -oP '"id"' | wc -l)
  echo "   Todos found: $COUNT"
else
  echo "❌ FAILED"
  echo "   Response: $BODY"
  exit 1
fi

echo ""
echo "=========================================="
echo "✨ ALL TESTS PASSED! ✨"
echo "=========================================="
echo ""
echo "Summary:"
echo "  ✓ User signup successful"
echo "  ✓ Todo created successfully"
echo "  ✓ Todos fetched successfully"
echo ""
echo "Todo creation is WORKING!"
