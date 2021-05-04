from django.urls import path
from user.views import UserLikeView, UserFundView, SignUpView, SignInView, UserInfoView

urlpatterns = [
   path('/signup', SignUpView.as_view()),
   path('/signin', SignInView.as_view()),
   path('/likelist', UserLikeView.as_view()), 
   path('/fundinglist', UserFundView.as_view()),
   path('', UserInfoView.as_view())
]

