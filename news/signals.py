from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.conf import settings
from .models import Post, User, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@receiver(m2m_changed, sender=Post.categ.through)
def save_posts(instance, action, pk_set, *args, **kwargs):

    if action == "post_add":
        html_save = render_to_string('send_post.html', {'post': instance})
        subject = f'В категориях, на которые вы подписаны новая статья'

        for pk in pk_set:
            category = Category.objects.get(pk=pk)
            print(category)
            subscribers_list = [user.email for user in category.subscr_user.all()]
            print(subscribers_list)

            msg = EmailMultiAlternatives(subject,
                                         body=f'В категориях, на которые вы подписаны появилась новая статья: \n\n'
                                              f'Ссылка: http://127.0.0.1:8000/news/{instance.id} \n\n'
                                              f'Заголовок: {instance.heading}\n'
                                              f'Превью: {instance.preview()}\n',
                                         from_email=settings.EMAIL_FROM,
                                         to=subscribers_list)

            msg.attach_alternative(html_save, "text/html")
            msg.send()


@receiver(post_save, sender=Post)
def post_save_post(created, **kwargs):
    post_instance = kwargs['instance']

    subscribers_list = {
        user.email
        for category in post_instance.categ.all()
        for user in category.subscr_user.all()

    }

    email_from = settings.EMAIL_FROM

    if created:
        subject = 'В категориях, на которые вы подписаны новая статья'
        text_message = f'В категориях, на которые вы подписаны появилась новая статья: \n\n' \
                       f'Ссылка: http://127.0.0.1:8000/posts/{post_instance.id}/\n\n' \
                       f'Заголовок: {post_instance.heading}\n' \
                       f'Превью: {post_instance.preview()}\n'

        render_html_template = render_to_string('send_post.html', {'post': post_instance, 'subject': subject})

        msg = EmailMultiAlternatives(subject, text_message, email_from, list(subscribers_list))

        msg.attach_alternative(render_html_template, 'text/html')

        msg.send()

    else:
        subject = 'В категориях, на которые вы подписаны была изменена статья'
        text_message = f'В категориях, на которые вы подписаны была изменена статья: \n\n' \
                       f'Ссылка: http://127.0.0.1:8000/posts/{post_instance.id}/\n\n' \
                       f'Заголовок: {post_instance.heading}\n' \
                       f'Превью: {post_instance.preview()}\n'

        render_html_template = render_to_string('send_post.html', {'post': post_instance, 'subject': subject})

        msg = EmailMultiAlternatives(subject, text_message, email_from, list(subscribers_list))

        msg.attach_alternative(render_html_template, 'text/html')

        msg.send()


@receiver(post_save, sender=User)
def post_save_user(created, **kwargs):
    user_instance = kwargs['instance']
    email_from = settings.EMAIL_FROM

    if created:
        subject = 'Приветствуем у нас на портале!'
        text_message = 'Приветственный текст'

        render_html_template = render_to_string('hello_message.html', {'user': user_instance,
                                                                       'subject': subject,
                                                                       'text': text_message})

        msg = EmailMultiAlternatives(subject, text_message, email_from, [user_instance.email, ])

        msg.attach_alternative(render_html_template, 'text/html')

        msg.send()
