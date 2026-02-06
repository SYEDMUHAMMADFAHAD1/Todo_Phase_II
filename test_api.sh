#!/bin/bash

API="http://localhost:8000/api"
EMAIL="testuser_$(date +%s)@test.com"
PASSWORD="Pass123456"

echo "=== Testing Todo API ==="
echo ""
echo "Email: $EMAIL"
echo "Password: $PASSWORD"
echo ""

# Step 1: Signup
echo "[STEP 1] Signing up..."
SIGNUP_RESPONSE=$(curl -s -X POST "$API/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\",\"name\":\"TestUser\"}")

echo "Signup Response:"
echo "$SIGNUP_RESPONSE" | head -100
TOKEN=$(echo "$SIGNUP_RESPONSE" | grep -oP '"token":"?\K[^"]*' | head -1)

if [ -z "$TOKEN" ]; then
  echo "[ERROR] Could not extract token from response"
  exit 1
fi

echo ""
echo "[SUCCESS] Got token: ${TOKEN:0:40}..."
echo ""

# Step 2: Create Todo
echo "[STEP 2] Creating a todo..."
CREATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Buy coffee supplies","description":"Get beans from the store"}')

HTTP_CODE=$(echo "$CREATE_RESPONSE" | tail -1)
BODY=$(echo "$CREATE_RESPONSE" | head -n -1)

echo "HTTP Status: $HTTP_CODE"
echo "Response:"
echo "$BODY"
echo ""

if [ "$HTTP_CODE" = "201" ]; then
  echo "[SUCCESS] Todo created successfully!"
  TODO_ID=$(echo "$BODY" | grep -oP '"id":"?\K[^"]*' | head -1)
  echo "Todo ID: $TODO_ID"
else
  echo "[ERROR] Failed to create todo (HTTP $HTTP_CODE)"
fi

echo ""
echo "[STEP 3] Fetching todos..."
FETCH_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$API/tasks" \
  -H "Authorization: Bearer $TOKEN")

HTTP_CODE=$(echo "$FETCH_RESPONSE" | tail -1)
BODY=$(echo "$FETCH_RESPONSE" | head -n -1)

echo "HTTP Status: $HTTP_CODE"
echo "Response:"
echo "$BODY"
echo ""

if [ "$HTTP_CODE" = "200" ]; then
  COUNT=$(echo "$BODY" | grep -oP '"id"' | wc -l)
  echo "[SUCCESS] Fetched todos successfully ($COUNT found)"
else
  echo "[ERROR] Failed to fetch todos (HTTP $HTTP_CODE)"
fi

echo ""
echo "=== Test Complete ==="
