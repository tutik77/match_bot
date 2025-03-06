from django.db import models

class User(models.Model):
    user_tg_id = models.BigIntegerField(unique=True, primary_key=True)
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    description_keywords = models.TextField()

    class Meta:
        db_table = 'Users'


class UserQuery(models.Model):
    id = models.AutoField(primary_key=True)
    query_text = models.CharField(max_length=255)
    user_tg_id = models.BigIntegerField()

    class Meta:
        db_table = 'UserQueries'
