from django.shortcuts import render, redirect
from .models import Article
from django.utils import timezone
from .forms import ArticleForm

def article_list(request):
    articles = Article.objects.filter(end_time__gt=timezone.now()).order_by('end_time')
    ret = []
    if request.user.is_authenticated:
        articles = Article.objects.filter(end_time__gt=timezone.now()).order_by('end_time')
        for article in articles:
            if request.user in article.voter.all():
                ret.append(article.id)

    ctx = {
        'articles' : articles,
        'ret' : ret,
    }
    return render(request, 'article_list.html', ctx)


def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.end_time = timezone.now() + timezone.timedelta(days=1)
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'article_edit.html', {'form': form})

def article_vote(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:
            article = Article.objects.get(pk=id)
            amount = float(request.POST['amount'])

            article.voted_token_amount += amount
            article.voter.add(request.user)
            request.user.info.token_amount -= amount

            article.save()
            request.user.info.save()
            request.user.save()
            return redirect('article_list')

def article_detail(request, id):
    article = Article.objects.get(pk=id)

    ctx = {
        'article': article,
    }
    return render(request, 'article_detail.html', ctx)