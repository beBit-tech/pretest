from rest_framework.permissions import BasePermission
from django.conf import settings

ACCEPTED_TOKEN = ('omni_pretest_token')



# 以 permission 類 
class TokenValid(BasePermission):
    def has_permission(self,request,view):
        # 驗證提交方法以及 token 內容

        get_token= request.data.get('token')

        return request.method=='POST' and get_token == getattr(settings, 'API_TOKEN', None)
