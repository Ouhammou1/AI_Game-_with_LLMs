#!/bin/bash

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2ODA5Mzg0LCJpYXQiOjE3NzY4MDIxODQsImp0aSI6IjM4NzUyMDI2YTA3NDRkNDRhZTQ0ODQ4NjBhMmIyNjVjIiwidXNlcl9pZCI6IjU1OWNhYjM1LTE3ZjgtNGMzOS05YzZlLTZhMDk3OThiNWI4NSJ9.C_tPwWtH7GQtlSm1yXWMDrEOM9GB3EsGE9gz_WzuXXE"
BASE="https://localhost:8443/chatbot"

echo "=== 1. Get sessions ==="
SESSIONS=$(curl -sk -H "Cookie: access_token=$TOKEN" $BASE/sessions)
echo $SESSIONS | python3 -m json.tool

SESSION_ID=$(echo $SESSIONS | python3 -c "import sys,json; s=json.load(sys.stdin); print(s[0]['session_id']) if s else print('')")
echo "Using session_id: $SESSION_ID"

echo ""
echo "=== 2. Delete session ==="
curl -sk -X DELETE $BASE/delete-session \
  -H "Content-Type: application/json" \
  -H "Cookie: access_token=$TOKEN" \
  -d "{\"session_id\": \"$SESSION_ID\"}" | python3 -m json.tool

echo ""
echo "=== 3. Verify deleted ==="
curl -sk -H "Cookie: access_token=$TOKEN" $BASE/sessions | python3 -m json.tool