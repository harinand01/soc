# from logs.models import RequestLog

# class RequestLogMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         # Ignore requests to static or media to prevent noise if any, but since the requirement 
#         # is just a basic SOC-style logging, we'll log everything except maybe some very internal stuff.
#         # But we can just log all.
        
#         # We should only log after getting the response to capture status code.
#         ip_address = request.META.get('REMOTE_ADDR', '')
#         # Handle proxy setups like X-Forwarded-For if needed, but basic REMOTE_ADDR is requested
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip_address = x_forwarded_for.split(',')[0]
            
#         user_agent = request.META.get('HTTP_USER_AGENT', '')
#         user = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'anonymous'
#         request_path = request.path
#         http_method = request.method
#         status_code = response.status_code

#         # Save to DB
#         # To avoid infinite loops or logging the log API itself too much, we might want to skip the API endpoint itself.
#         # But logging it is also fine. Let's avoid logging the log fetching itself to prevent database explosion.
#         if request_path != '/api/logs/':
#             try:
#                 RequestLog.objects.create(
#                     user=user,
#                     ip_address=ip_address,
#                     request_path=request_path,
#                     http_method=http_method,
#                     status_code=status_code,
#                     user_agent=user_agent
#                 )
#             except Exception as e:
#                 # Silently ignore DB errors during logging to not break the site
#                 pass

#         return response
