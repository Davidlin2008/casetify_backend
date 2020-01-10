from django.urls import path 
from .views import (
    SignUpView, 
    SignInView, 
    MyprofileView, 
    MyprofileEditView, 
    MyShippingAddressEditView
)

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/myprofile', MyprofileView.as_view()),
    path('/myprofile-edit', MyprofileEditView.as_view()),
    path('/myshippingaddress-edit', MyShippingAddressEditView.as_view()),
]