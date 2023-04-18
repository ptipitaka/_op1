# Generated by Django 4.2 on 2023-04-17 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tipitaka', '0025_alter_wordlist_edition_alter_wordlist_page_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordListVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(default=0, verbose_name='version')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tipitaka.edition', verbose_name='edition')),
            ],
        ),
        migrations.AddField(
            model_name='wordlist',
            name='wordlistversion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tipitaka.wordlistversion', verbose_name='Wordlist version'),
        ),
    ]
