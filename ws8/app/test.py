from auth import create_access_token, verify_token
from schemas import TokenData
from datetime import timedelta

# Simulate user data
user_data = {"sub": "ahmed123"}

# 1. Create token
token = create_access_token(data=user_data, expires_delta=timedelta(minutes=5))
print("🔐 JWT Token:\n", token)

# 2. Decode token (simulate verification)
try:
    token_data = verify_token(token, credentials_exception=Exception("Invalid token"))
    print("\n✅ Token verified! Username:", token_data.username)
except Exception as e:
    print("\n❌ Token verification failed:", e)
