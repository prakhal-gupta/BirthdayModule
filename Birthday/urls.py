from django.urls import path
from Birthday.views import *

app_name = 'Birthday'
urlpatterns = [
 	path('registration/',User_registration),
	path('login/',User_login),
	path('Dash/',User_dash),
	path('logout/',Logout),
	path('Profile/register/',Profile_Creation),
	path('content/',Birthday_messg),
	path('Profile/delete/',Student_Faculty_Delete),
	path('Profile/detail/',Student_Faculty_detail),
	path('list/',Birthday_List),
	path('mail/',Birthday_Mail),
	path('Password/forgot/',Password_Forgot),
	path('Password/change/',Password_Change),
	path('OTP/verification/',OTP_Verification),
]