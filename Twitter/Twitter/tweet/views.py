from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-create_at')
    context = {"tweets": tweets}
    return render(request, 'tweet_list.html', context)

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False) #data will not save directly in database, but will hold by the variable
            tweet.user = request.user
            tweet.save() # user will be added now with the data in database
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {"form": form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    print("tweet id",tweet)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False) #data will not save directly in database, but will hold by the variable
            tweet.user = request.user
            tweet.save() # user will be added now with the data in database
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
        
    return render(request, 'tweet_form.html', {"form": form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    
    return render(request, 'tweet_confirm_delete.html', {"tweet": tweet})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {"form": form})


def search_view(request):
    search_query = request.GET.get('search_query', '')
    if search_query:
        tweets = Tweet.objects.filter(text__icontains=search_query)
        print("done", tweets)
    else:
        tweets = Tweet.objects.all()
        print("not done", tweets)
    
    context = {
        'search_by': search_query,
        'tweets': tweets,
    }
    return render(request, 'search_results.html', context)

def error404_view(request, exception):
    return render(request, '404.html', {})