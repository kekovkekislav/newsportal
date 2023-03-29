import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsportal.settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsPaper.settings")
# os.environ.setdefault("TEAMVAULT_CONFIG_FILE", "/etc/teamvault.cfg")

import django
django.setup()

from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

import random 

def fill_data():    
    User.objects.all().delete()
    Category.objects.all().delete()
    
    # создание пользователей
    alex_user = User.objects.create_user(username = 'Alex', email = 'Alex@mail.ru', password = 'alex_password')
    mark_user = User.objects.create_user(username = 'Mark', email = 'Mark@mail.ru', password = 'mark_password')
    
    # создание объектов авторов
    alex = Author.objects.create(user = alex_user)
    mark = Author.objects.create(user = mark_user)
    
    # создание категорий
    category_sport = Category.objects.create(name = "Спорт")
    category_politic = Category.objects.create(name = "Политика")
    category_tourism = Category.objects.create(name = "Туризм")
    category_IT = Category.objects.create(name = "IT")
    
    # Тексты статей и новости
    sport_tourism_text = """Статья Алекса про спорт и туризм """ 
    politic_text = """Статья Марка про политику """
    news_IT = """Новость Марка про IT """
    
    # Две статьи и новость
    article_alex = Post.objects.create(author = alex, post_type = Post.article, title = "Статья алекса про спорт и туризм", text = sport_tourism_text)
    article_mark = Post.objects.create(author = mark, post_type = Post.article, title = "Статья марка про политику", text =politic_text)
    news_mark = Post.objects.create(author = mark, post_type = Post.news, title = "Новость от марка про IT", text = news_IT)
    
    # присваивание категорий этим объектам
    PostCategory.objects.create(post = article_alex, category = category_sport)
    PostCategory.objects.create(post = article_alex, category = category_tourism)
    PostCategory.objects.create(post = article_mark, category = category_politic)
    PostCategory.objects.create(post = news_mark, category = category_IT)
    
    #комментарии
    comment1 = Comment.objects.create(post = article_alex, user = mark.user, text = "коммент Марка №1 к статье Алекса")
    comment2 = Comment.objects.create(post = article_mark, user = alex.user, text = "коммент Алекса №2 к статье Марка")
    comment3 = Comment.objects.create(post = news_mark, user = mark.user, text = "коммент Марка №3 к новости Марка")
    comment4 = Comment.objects.create(post = news_mark, user = alex.user, text = "коммент Алекса №4 к новости Марка")
    

    # Список для лайков
    like_list = [article_alex,
                    article_mark,
                    news_mark,
                    comment1,
                    comment2,
                    comment3,
                    comment4]
    
    # Лайк/дизлайк
    for i in range(100):
        random_obj = random.choice(like_list)
        if i % 2:
            random_obj.like()
        else:
            random_obj.dislike()
            
    # подсчет рейтинга Алекса
    rating_alex = (sum([post.rating*3 for post in Post.objects.filter(author=alex)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(user=alex.user)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=alex)]))
    alex.update_rating(rating_alex) # и обновление
    
    # подсчет рейтинга Марка
    rating_mark = (sum([post.rating*3 for post in Post.objects.filter(author=mark)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(user=mark.user)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=mark)]))
    mark.update_rating(rating_mark) # и обновление
    
    # лучший автор
    best_author = Author.objects.all().order_by('-rating')[0]
    
    print(f"Лучший автор\n Имя: {best_author.user.username}\nРейтинг: {best_author.rating}")
    print("")
    
    # лучшая статья(!) - именно статья (ВАЖНО)
    best_article = Post.objects.filter(post_type = Post.article).order_by('-rating')[0]

    print(f"Лучшая статья\nДата: {best_article.created}\nАвтор: {best_article.author.user.username}\nРейтинг: {best_article.rating}\n"
          f"Заголовок: {best_article.title}\nПревью: {best_article.preview()}")
           
    # печать комментариев к ней
    print("")
    print("Комментарии к ней")
    for comment in Comment.objects.filter(post = best_article):
        print(f"Дата:{comment.created}\nАвтор: {comment.user.username}\nРейтинг: {comment.rating}\nКомментарий: {comment.text}")
    
fill_data()