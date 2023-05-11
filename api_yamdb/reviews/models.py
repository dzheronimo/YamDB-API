from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import year_validate
from users.models import User

FIRST_MOVIE = 1895


class BaseModel(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ('id',)

    def __str__(self):
        return self.name


class Category(BaseModel):
    pass


class Genre(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(FIRST_MOVIE), year_validate])
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='genres')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='titles')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='titles', null=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    @property
    def rating(self):
        avg_score = self.reviews.aggregate(rating=models.Avg('score'))
        return avg_score['rating']


class ExtendedBaseModel(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('pub_date',)


class Review(ExtendedBaseModel):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta(ExtendedBaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_title')]

    def __str__(self):
        return f'{self.title} {self.score}'


class Comment(ExtendedBaseModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.review} {self.author}'
