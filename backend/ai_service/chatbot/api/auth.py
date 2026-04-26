import os
import jwt
from flask import request


def get_user_id():
    token = request.cookies.get('access_token')
    print("\n\n\n\n\n\n\n\n\n\n\n\n  access_token  \n\n\n\n\n\n\n\n\n\n\n\n " , flush=True)
    print(f"token = {token} \n\n" , flush=True)
    if not token:
        return request.remote_addr
    try:
        decoded = jwt.decode(token, os.getenv('DJANGO_SECRET_KEY'), algorithms=['HS256'])
        return str(decoded.get('user_id'))
    except Exception as e:
        print(f"[JWT] Failed to decode token: {e}")
        return request.remote_addr
    












#     import os
# import jwt
# from flask import request


# def get_user_id():
#     """
#     Returns the authenticated user_id from JWT cookie.
#     Returns None if user is not authenticated or token is invalid.
#     """
#     token = request.cookies.get('access_token')
    
#     if not token:
#         print("[AUTH] No access_token cookie", flush=True)
#         return None
    
#     try:
#         decoded = jwt.decode(
#             token,
#             os.getenv('DJANGO_SECRET_KEY'),
#             algorithms=['HS256']
#         )
#         user_id = decoded.get('user_id')
#         if not user_id:
#             print("[AUTH] Token missing user_id field", flush=True)
#             return None
#         return str(user_id)
#     except jwt.ExpiredSignatureError:
#         print("[AUTH] Token expired", flush=True)
#         return None
#     except jwt.InvalidTokenError as e:
#         print(f"[AUTH] Invalid token: {e}", flush=True)
#         return None
#     except Exception as e:
#         print(f"[AUTH] Failed to decode token: {e}", flush=True)
#         return None