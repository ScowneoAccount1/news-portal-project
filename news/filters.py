from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post, Author
from django.forms.widgets import SelectDateWidget


# создаём фильтр
class SearchFilter(FilterSet):
    date_create = DateFilter(field_name='date_create', lookup_expr='gt', label='Позднее даты (mm-dd-yyyy)', widget=SelectDateWidget)
    heading = CharFilter(field_name='heading', lookup_expr='icontains', label='По названию')
    post_user = CharFilter(field_name='post_user__user__username', label='По автору')
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = {'date_create', 'heading', 'post_user'}  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)



