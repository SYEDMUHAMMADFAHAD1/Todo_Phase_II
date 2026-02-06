#!/bin/bash

# Test direct API call without JSON parsing
EMAIL="test_$(date +%s)@example.com"
PASSWORD="TestPassword123!"
API="http://localhost:8000/api"

echo "🚀 Testing Todo Creation"
echo "Email: $EMAIL"
echo ""

# Step 1: Sign Up
echo "📝 Step 1: Signing up..."
SIGNUP=$(curl -s -X POST "$API/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\",\"name\":\"Test User\"}")

echo "Response: $SIGNUP"
echo ""

# Extract token from signup response
TOKEN=$(echo "$SIGNUP" | grep -o '"token":"[^"]*' | cut -d'"' -f4)
USER_ID=$(echo "$SIGNUP" | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)

echo "✅ Token: ${TOKEN:0:30}..."
echo "✅ User ID: $USER_ID"
echo ""

# Step 2: Create Todo
echo "📝 Step 2: Creating todo..."
TODO=$(curl -s -X POST "$API/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Buy coffee supplies","description":"Get espresso beans and milk"}')

echo "Response:"
echo "$TODO"
echo ""

# Check if it's an error
if echo "$TODO" | grep -q "detail"; then
  echo "❌ ERROR in response!"
else
  echo "✅ Todo created!"
fi
