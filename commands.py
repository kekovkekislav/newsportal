import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsportal.settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsPaper.settings")
# os.environ.setdefault("TEAMVAULT_CONFIG_FILE", "/etc/teamvault.cfg")

import django
django.setup()


from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment


import random 

def todo():    
    User.objects.all().delete()
    Category.objects.all().delete()
    
    # создание пользователей
    alex_user = User.objects.create_user(username = 'Alex', email = 'Alex@mail.ru', password = 'alex_password')
    mark_user = User.objects.create_user(username = 'Mark', email = 'Mark@mail.ru', password = 'mark_password')
    
    # создание объектов авторов
    alex = Author.objects.create(user = alex_user)
    mark = Author.objects.create(user = mark_user)
    
    # создание категорий
    cat_sport = Category.objects.create(name = "Спорт")
    cat_music = Category.objects.create(name = "Музыка")
    cat_cinema = Category.objects.create(name = "Кино")
    cat_IT = Category.objects.create(name = "IT")
    
    # создание текстов статей/новостей
    text_article_sport_cinema = """Статья Алекса про спорт"""
    
    text_article_music = """Статья Марка про музыку"""
    
    text_news_IT = """Новость Марка про IT"""
    
    # создание двух статей и новости
    article_alex = Post.objects.create(author = alex, post_type = Post.article, title = "статья_спорт_кино_Джонни", text = text_article_sport_cinema)
    article_mark = Post.objects.create(author = mark, post_type = Post.article, title = "статья_музыка_Томми", text = text_article_music)
    news_mark = Post.objects.create(author = mark, post_type = Post.news, title = "новость_IT_Томми", text = text_news_IT)
    
    # присваивание категорий этим объектам
    PostCategory.objects.create(post = article_alex, category = cat_sport)
    PostCategory.objects.create(post = article_alex, category = cat_cinema)
    PostCategory.objects.create(post = article_mark, category = cat_music)
    PostCategory.objects.create(post = news_mark, category = cat_IT)
    
    # создание комментариев
    comment1 = Comment.objects.create(post = article_alex, user = mark.user, text = "коммент Марка №1 к статье Алекса")
    comment2 = Comment.objects.create(post = article_mark, user = alex.user, text = "коммент Алекса №2 к статье Марка")
    comment3 = Comment.objects.create(post = news_mark, user = mark.user, text = "коммент Марка №3 к новости Марка")
    comment4 = Comment.objects.create(post = news_mark, user = alex.user, text = "коммент Алекса №4 к новости Марка")
    

    # список всех объектов, которые можно лайкать
    list_for_like = [article_alex,
                    article_mark,
                    news_mark,
                    comment1,
                    comment2,
                    comment3,
                    comment4]
    
    # 100 рандомных лайков/дислайков
    for i in range(100):
        random_obj = random.choice(list_for_like)
        if i % 2:
            random_obj.like()
        else:
            random_obj.dislike()
            
    # подсчет рейтинга Алекса
    rating_johny = (sum([post.rating*3 for post in Post.objects.filter(author=alex)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(user=alex.user)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=alex)]))
    alex.update_rating(rating_johny) # и обновление
    
    # подсчет рейтинга Марка
    rating_tommy = (sum([post.rating*3 for post in Post.objects.filter(author=mark)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(user=mark.user)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=mark)]))
    mark.update_rating(rating_tommy) # и обновление
    
    # лучший автор
    best_author = Author.objects.all().order_by('-rating')[0]
    
    print("Лучший автор")
    print("username:", best_author.user.username)
    print("Рейтинг:", best_author.rating)
    print("")
    
    # лучшая статья(!) - именно статья (ВАЖНО)
    best_article = Post.objects.filter(post_type = Post.article).order_by('-rating')[0]
    print("Лучшая статья")
    print("Дата:", best_article.created)
    print("Автор:", best_article.author.user.username)
    print("Рейтинг:", best_article.rating)
    print("Заголовок:", best_article.title)
    print("Превью:", best_article.preview())
    print("")
    
    # печать комментариев к ней. Обязательно цикл, потому что комментарий может быть не один и нужен универсальный код
    print("Комментарии к ней")
    for comment in Comment.objects.filter(post = best_article):
        print("Дата:", comment.created)
        print("Автор:", comment.user.username)
        print("Рейтинг:", comment.rating)
        print("Комментарий:", comment.text)
        print("")

todo()