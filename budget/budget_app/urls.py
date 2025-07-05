from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('add/', views.add_expense, name='add_expense'),
    path('predict-category/', views.predict_category_view, name='predict_category_view'),
    path('predict-income-category/', views.predict_income_category_view, name='predict_income_category_view'),

    path('new_income/', views.new_income, name='new_income'),
    path('add_income/', views.add_income, name='add_income'),  # Make sure this exists
    path('new_expense/', views.new_expense, name='new_expense'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),
    path('budget/', views.budget, name='budget'),
    path('report/', views.report_page, name='report'),

    # path('api/expenses/grouped/', views.grouped_expenses, name='grouped_expenses'),

    # Login and Logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Password Reset Views 
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Sign up
    path('signup/', views.signup, name='signup'),
]
