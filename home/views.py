from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Expense
from .forms import ExpenseForm

# Update the Expenses data
@login_required(login_url='/login/')
def update_expense(request, id):
    queryset = Expense.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        price = float(data.get('price', 0))  # Change int() to float()

        # Update the expense object
        queryset.name = name
        queryset.amount = price  # Use 'amount' instead of 'price' based on your model
        queryset.save()
        return redirect('/')

    context = {'expense': queryset}
    return render(request, 'update_expenses.html', context)

# Delete the Expenses data
@login_required(login_url='/login/')
def delete_expense(request, id):
    queryset = Expense.objects.get(id=id)
    queryset.delete()
    return redirect('/')

# Login page for user
def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username).first()
            if not user_obj:
                messages.error(request, "Username not found")
                return redirect('/login/')
            user_auth = authenticate(username=username, password=password)
            if user_auth:
                login(request, user_auth)
                return redirect('expenses')
            messages.error(request, "Wrong Password")
            return redirect('/login/')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register/')
    return render(request, "login.html")

# Register page for user
def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('/login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register')
    return render(request, "register.html")

# Logout function
def custom_logout(request):
    logout(request)
    return redirect('login')

# Generate the Bill
@login_required(login_url='/login/')
def pdf(request):
    expenses = Expense.objects.all()
    total_sum = sum(expense.amount for expense in expenses)

    # Handle salary input from the user
    if request.method == "POST":
        salary = float(request.POST.get('salary', 0))
        suggestions = []

        # Generate suggestions based on salary and expenses
        if salary <= 0:
            suggestions.append("Please enter a valid salary.")
        else:
            if total_sum > salary:
                suggestions.append("Your expenses exceed your salary. Consider cutting back on non-essential spending.")
            if total_sum > salary * 0.5:
                suggestions.append("You are spending more than half of your salary. Review your expenses.")
            if total_sum > 0.8 * salary:
                suggestions.append("Consider setting a budget to manage your expenses more effectively.")

        # Render the template with salary input and suggestions
        context = {
            'expenses': expenses,
            'total_sum': total_sum,
            'username': request.user.username,
            'salary': salary,
            'suggestions': suggestions,
        }
        return render(request, 'pdf.html', context)

    # If not a POST request, show the initial page without salary input
    context = {
        'expenses': expenses,
        'total_sum': total_sum,
        'username': request.user.username,
        'salary': 0,  # Default salary value if not provided
        'suggestions': [],
    }
    return render(request, 'pdf.html', context)

# Add Expense function
def add_expense(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')

        # Create a new Expense object and save it to the database
        Expense.objects.create(name=name, amount=amount)
        return redirect('your_expenses_page')  # Change this to the name of your expense listing page

    # Display the form and existing expenses
    expenses = Expense.objects.all()
    total_sum = sum(exp.amount for exp in expenses)  # Sum up all expenses
    return render(request, 'expenses.html', {'expenses': expenses, 'total_sum': total_sum})

# List all expenses
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})

# Expense view function
@login_required(login_url='/login/')
def expenses(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = float(request.POST.get('amount', 0))  # Capture the amount correctly

        # Create a new Expense entry
        Expense.objects.create(
            name=name,
            amount=amount  # Ensure this matches your model field
        )
        return redirect('expenses')  # Redirect back to the expense list page

    # Retrieve all Expense records
    queryset = Expense.objects.all()
    total_sum = sum(expense.amount for expense in queryset)  # Correctly sum the amounts

    context = {'expenses': queryset, 'total_sum': total_sum}
    return render(request, 'expenses.html', context)