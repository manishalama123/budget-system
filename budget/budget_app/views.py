from .classifier import predict_category as predict_expense_category


from .income_classifier import predict_category as predict_income_category


from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Income, Expense, Budget
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Sum 
from django.utils import timezone
from django.http import JsonResponse
from django.http import HttpResponse  # Add this line at the top
from collections import defaultdict
from calendar import monthrange
from datetime import datetime, date
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
import calendar
from calendar import month_name
from collections import OrderedDict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



# def predict_category_view(request):
#     # Get the description or name based on the form
#     description = request.GET.get('description', '')
#     name = request.GET.get('name', '')

#     if description:
#         predicted = predict_category(description)  # Predict based on description
#         return JsonResponse({'category': predicted})  # Return as JSON response
#     elif name:
#         predicted = predict_category(name)  # Predict based on name for the budget form
#         return JsonResponse({'category': predicted})  # Return as JSON response
#     else:
#         return JsonResponse({'error': 'No description or name provided'}, status=400)
def predict_category_view(request):
    description = request.GET.get('description', '')
    name = request.GET.get('name', '')

    if description:
        predicted = predict_expense_category(description)  # Use the expense classifier
        return JsonResponse({'category': predicted})
    elif name:
        predicted = predict_expense_category(name)  # Use the expense classifier
        return JsonResponse({'category': predicted})
    else:
        return JsonResponse({'error': 'No description or name provided'}, status=400)



# def predict_income_category(request):
#     if request.method == 'GET':  # Check if the request method is GET
#         description = request.GET.get('description', '')
#         if description:
#             category = predict_category(description)
#             return JsonResponse({'category': category})
#         return JsonResponse({'category': 'Others'})  # Default category if no description
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

def predict_income_category_view(request):
    if request.method == 'GET':
        description = request.GET.get('description', '')
        if description:
            # Use the imported income classifier function
            category = predict_income_category(description)
            return JsonResponse({'category': category})
        return JsonResponse({'category': 'Others'})  # Default category if no description
    return JsonResponse({'error': 'Invalid request method'}, status=400)

# SIGNUP
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
# LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('dashboard')  # Redirect to dashboard
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'login.html')

# DASHBOARD
@login_required(login_url='/login/')
def dashboard(request):
    # Basic totals
    total_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    remaining = total_income - total_expense

    # Recent transactions
    incomes = Income.objects.filter(user=request.user).order_by('-date')[:5]
    expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]

    # Pie chart data - expense distribution by category
    expense_categories = Expense.objects.filter(user=request.user).values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    pie_labels = [item['category'] for item in expense_categories]
    pie_values = [float(item['total']) for item in expense_categories]

    # Bar chart data - Daily expenses for last 7 days
    today = timezone.now().date()
    daily_data = []
    daily_labels = []
    
    for i in range(6, -1, -1):  # Last 7 days
        day = today - timedelta(days=i)
        day_expenses = Expense.objects.filter(
            user=request.user,
            date=day
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        daily_data.append(float(day_expenses))
        daily_labels.append(day.strftime('%a'))  # Mon, Tue, etc.

    # Monthly expenses for current year
    current_year = today.year
    monthly_data = []
    monthly_labels = []
    
    for month in range(1, 13):
        month_expenses = Expense.objects.filter(
            user=request.user,
            date__year=current_year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_data.append(float(month_expenses))
        monthly_labels.append(calendar.month_abbr[month])

    # Yearly expenses for last 5 years
    yearly_data = []
    yearly_labels = []
    
    for year in range(current_year - 4, current_year + 1):
        year_expenses = Expense.objects.filter(
            user=request.user,
            date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        yearly_data.append(float(year_expenses))
        yearly_labels.append(str(year))

    # Budget data
    budgets = Budget.objects.filter(user=request.user).order_by('-start_date')[:4]
    budget_list = []

    for budget in budgets:
        used = Expense.objects.filter(
            user=request.user, 
            category__iexact=budget.category,
            date__gte=budget.start_date,
            date__lte=budget.end_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        percent = min(int((used / budget.amount) * 100), 100) if budget.amount > 0 else 0
        budget.percentage_used = percent
        budget.used = used
        budget_list.append(budget)

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'remaining': remaining,
        'incomes': incomes,
        'expenses': expenses,
        
        # Pie chart data
        'labels': json.dumps(pie_labels),
        'values': json.dumps(pie_values),
        
        # Bar chart data
        'daily_labels': json.dumps(daily_labels),
        'daily_data': json.dumps(daily_data),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_data': json.dumps(monthly_data),
        'yearly_labels': json.dumps(yearly_labels),
        'yearly_data': json.dumps(yearly_data),
        
        'budgets': budget_list,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def new_income(request):
    return render(request, 'new_income.html')

@login_required
def new_expense(request):
    return render(request, 'new_expense.html')

@login_required
def add_income(request):
    if request.method == "POST":
        # Capture form data
        amount = Decimal(request.POST["amount"])
        description = request.POST["description"]
        date = request.POST["date"]
        category = request.POST["category"]  # Capture the category

        # If category is "Others", predict the category
        if category.lower() == "others":
            # Call your classifier to predict the category based on the description
            predicted_income_category = predict_income_category(description)  # Use the imported function directly
            category = predicted_income_category  # Update the category to predicted one

        # Create the income record
        Income.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            date=date,
            category=category  # Save the predicted category (or user-selected)
        )

        messages.success(request, "Income added successfully!")
        return redirect('dashboard')
    
    return HttpResponse("Invalid response", status=404)


@login_required
def add_expense(request):
    if request.method == "POST":
        amount = Decimal(request.POST["amount"])
        description = request.POST["description"]
        category = request.POST["category"]
        date = request.POST["date"]

        # Only predict if category is set to "other"
        if category.lower() == "other":
            category = predict_expense_category(description)  # Use the imported function
            print(f"Predicted category: {category}")

        Expense.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            category=category,
            date=date
        )
        messages.success(request, "Expense added successfully!")
        return redirect('dashboard')
    return HttpResponse("Invalid response", status=404)


@login_required
def history(request):
    # Filter transactions for the logged-in user
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    # Convert to a unified transaction format
    transactions = [
        {
            "date": income.date,
            "category": "Income",  # Default category for Income
            "amount": income.amount,
            "description": income.description,
            "type": "Income"
        }
        for income in incomes
    ] + [
        {
            "date": expense.date,
            "category": expense.category,  # Use category for Expense
            "amount": expense.amount,
            "description": expense.description,
            "type": "Expense"
        }
        for expense in expenses
    ]

    # Sort transactions by date (latest first)
    transactions.sort(key=lambda x: x["date"], reverse=True)
     # Add Pagination (5 transactions per page)
    paginator = Paginator(transactions, 5)  # Change 5 to any number of transactions per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "history.html", {"page_obj": page_obj})

@login_required
def budget(request):
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        end_date = request.POST.get('end_date')
        
        # Predict category only if user selects "other"
        # Only predict if category is set to "other"
        if category.lower() == "other":
            category = predict_expense_category(name)
        # Ensure the date is in the correct format
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Create and save the new Budget
        new_budget = Budget(
            user=request.user,
            name=name,
            amount=amount,
            category=category,
            start_date=timezone.now().date(),  # Current date as start date
            end_date=end_date
        )
        new_budget.save()
        messages.success(request, "Budget added successfully!")
        return redirect('budget')  # Redirect to the dashboard after saving
    

    budgets = Budget.objects.filter(user=request.user)
    budget_data = []

    for budget in budgets:
        
        budget_category = budget.category.strip().lower()
        matching_expenses = Expense.objects.filter(
            user=request.user,
            category__iexact=budget_category,
            date__gte=budget.start_date,
            date__lte=budget.end_date
        )
        total_spent = matching_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        budget_data.append({
            'budget': budget,
            'spent': total_spent,
            'remaining': budget.amount - total_spent,
            'percentage': round((total_spent / budget.amount) * 100, 2) if budget.amount > 0 else 0
        })

    return render(request, 'budget.html', {'budget_data': budget_data})

# REPORT
def report_page(request):
    user = request.user

    # Step 1: Get selected month (YYYY-MM) or use current
    selected_month = request.GET.get('month')
    if selected_month:
        year, month = map(int, selected_month.split('-'))
    else:
        today = date.today()
        year, month = today.year, today.month

    # Step 2: Get start and end dates for filtering
    start_date = date(year, month, 1)
    end_date = date(year, month, monthrange(year, month)[1])

    # Step 3: Filter data by logged-in user and date range
    monthly_income = Income.objects.filter(
    user=user,
    date__range=(start_date, end_date)
    )

    
    monthly_expenses = Expense.objects.filter(
        user=user,
        date__range=(start_date, end_date)
    )

    monthly_budgets = Budget.objects.filter(
        user=user,
        start_date__lte=end_date,
        end_date__gte=start_date
    )

    # Step 4: Calculate totals
    total_income = sum(i.amount for i in monthly_income)
    total_expense = sum(e.amount for e in monthly_expenses)
    total_budget = sum(b.amount for b in monthly_budgets)
    remaining = total_budget - total_expense

    # Step 5: Category-wise breakdown (for chart)
    category_totals = defaultdict(float)
    for expense in monthly_expenses:
        category_totals[expense.category] += float(expense.amount)

    category_labels = list(category_totals.keys())
    category_data = list(category_totals.values())

    context = {
        'monthly_expenses': monthly_expenses,
        'total_budget': total_budget,
        'total_expense': total_expense,
        'total_income' : total_income,
        'remaining': remaining,
        'category_labels': category_labels,
        'category_data': category_data,
        'selected_month': f"{year}-{month:02d}"
    }

    return render(request, 'report.html', context)