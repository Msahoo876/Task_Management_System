from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from .models import Crud, User, Assign, Feedback
from django.http import HttpResponse, JsonResponse
from pymongo import MongoClient
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

global_data = ""

def Home(request):
    return render(request,'Home.html')

def sign(request):
    return render(request, 'sign.html')


def signup_task(request):
    if request.method == 'POST':
        # Retrieve data from the form
        fast_name = request.POST.get('fast')
        last_name = request.POST.get('last')
        email_id = request.POST.get('email')
        password = request.POST.get('paaswd')  # Corrected misspelling of "password"

        # Create a new User instance and save it to the database
        User.objects.create(
            Fast_name=fast_name,
            Last_name=last_name,
            Email_Id=email_id,
            Password=password
        )
    return HttpResponseRedirect(reverse('Home'))
    # return render({'success': True, 'message': 'Search successful'})
        # Optionally, you can redirect the user to another page after successful signup
        # return redirect('signup_success')  # Replace 'signup_success' with the URL name of your success page

def login_task(request):
    global global_data
    if request.method == 'POST':
        email1 = request.POST.get('email1')
        passwd1 = request.POST.get('passwd1')
        global_data = email1
        try:
            user = User.objects.filter(Email_Id=email1).first()  # Querying using Email_Id and getting the first user
            if user is not None and user.Password == passwd1:
                return render(request, 'crud.html', {'user': user})
            else:
                return HttpResponse("Incorrect email or password")
        except User.DoesNotExist:
            return HttpResponse("User does not exist")
    # return render(request, 'login.html')
        
def logout_view(request):
    logout(request)  # Log out the user
    return HttpResponseRedirect(reverse('Home'))

def crud(request):
    return render(request,'crud.html')

def create(request):
    return render(request,'Create.html')

def update(request):
    return render(request,'Update.html')

def delete(request):
    return render(request,'Delete.html')

def view_t(request):
    return render(request,'View.html')

def assign(request):
    return render(request,'Assign.html')

def profile(request):
    return render(request, 'Profile.html')

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        
        Crud.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status
        )
    return render(request, 'crud.html')
        # tasks = Crud.objects.all()
        # return render(request, 'Create.html', {'tasks': tasks})
    
def get_tasks(request):
    tasks = Crud.objects.all().values()  # Get all tasks from the database
    return render(request, 'Create.html', {'tasks': tasks})

def update_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        try:
            # Fetch all tasks with the specified title
            tasks = Crud.objects.filter(title=title)

            # Update each task
            for task in tasks:
                task.description = description
                task.due_date = due_date
                task.priority = priority
                task.status = status
                task.save()

            return JsonResponse({'success': True, 'message': 'Tasks updated successfully'})
        except Crud.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No tasks with the specified title'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def get_tasks1(request):
    tasks = Crud.objects.all()  # Get all tasks from the database
    return render(request, 'Update.html', {'tasks': tasks})

def delete_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')

        # Select the database and collection
        db = client['Task_Management_System']
        collection = db['Home_crud']

        try:
            # Delete the task based on title
            result = collection.delete_one({'title': title})

            if result.deleted_count == 1:
                return JsonResponse({'success': True, 'message': 'Task deleted successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Task does not exist'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_tasks2(request):
    tasks = Crud.objects.all()  # Get all tasks from the database
    return render(request, 'Delete.html', {'tasks': tasks})

def search_task(request):
    if request.method == 'POST':
        title = request.POST.get('search-title')
        
        if title is not None:  # Check if title is not None
            tasks = Crud.objects.filter(title__icontains=title)
            
            search_results = [{'title': task.title, 'description': task.description, 'due_date': task.due_date, 'priority': task.priority, 'status': task.status} for task in tasks]
            return render(request,'View.html',{'results': search_results})
            # return JsonResponse({'success': True, 'message': 'Search successful', 'results': search_results})
        else:
            return JsonResponse({'success': False, 'message': 'Title cannot be empty'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_tasks3(request):
    search_results = Crud.objects.all()  # Get all tasks from the database
    return render(request, 'View.html', {'results': search_results})

def assign_task(request):
    users = User.objects.values('Fast_name', 'Last_name')
    tasks = Crud.objects.values('title')
    search_results = None  # Initialize search_results outside the conditional block
    
    if request.method == "POST":
        title = request.POST.get('task')
        email = request.POST.get('email')
        userlist = request.POST.get('userlist')
        
        Assign.objects.create(
            Task_Title=title,
            Assigned_User=userlist,
            Created_User=email
        )
        
        search_results = Assign.objects.all()
    
    return render(request, 'Assign.html', {'users': users, 'results': search_results, 'tasks': tasks})

def profile_task(request):
    global global_data  # Declare global_data as global within the function
    # Fetch user data from MongoDB
    user_data = User.objects.all()
    for user in user_data:
        if user.Email_Id == global_data:
            fast = user.Fast_name
            last = user.Last_name
            email = user.Email_Id
            passwd = user.Password
            # Assuming only one user matches the email, you can break the loop here
            break
    else:
        # Handle the case where no user matches the email
        fast = None
        last = None
        email = None
        passwd = None
    
    # Pass user data to the HTML template
    search_results = Assign.objects.all()
    search_results1 = Crud.objects.all()
    return render(request, 'profile.html', {'fast': fast,'last':last, 'email':email, 'passwd':passwd, 'result':search_results, 'result1':search_results1 })

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Feedback.objects.create(
            Name=name,
            Email=email,
            Message=message
        )

        subject = 'Thank you for your feedback'
        message = 'Dear {},\n\nThank you for submitting the feedback. Your message has been received and we will get back to you soon.'.format(name)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]  # Note: recipient_list should be a list even if there's only one recipient
        
        send_mail(subject, message, from_email, recipient_list)
        
        return render({'success': True, 'message': 'Search successful'})  # Render a confirmation template
    else:
        return render(request, 'Home.html')

def back(request):
    logout(request)  # Log out the user
    return HttpResponseRedirect(reverse('crud'))