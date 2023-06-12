# Generated by Django 4.2 on 2023-06-12 04:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tipitaka', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonreference',
            name='structure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tipitaka.structure', verbose_name='Structure'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='code',
            field=models.CharField(db_index=True, max_length=5, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='description',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='script',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tipitaka.script', verbose_name='Script'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='title',
            field=models.CharField(db_index=True, max_length=80, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='version',
            field=models.CharField(blank=True, max_length=10, verbose_name='Version'),
        ),
        migrations.AlterField(
            model_name='script',
            name='code',
            field=models.CharField(db_index=True, max_length=20, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='script',
            name='description',
            field=models.CharField(blank=True, max_length=80, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='table_of_content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tipitaka.tableofcontent', verbose_name='Table of contents'),
        ),
        migrations.AlterField(
            model_name='tableofcontent',
            name='code',
            field=models.CharField(db_index=True, max_length=20, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='tableofcontent',
            name='wordlist_version',
            field=models.ManyToManyField(related_name='wordlist_version', to='tipitaka.wordlistversion', verbose_name='Wordlist version'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='book_cover',
            field=models.ImageField(blank=True, null=True, upload_to='tipitaka_book_cover', verbose_name='Book cover'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='edition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tipitaka.edition', verbose_name='Edition'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='total_pages',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Total pages'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='volume_number',
            field=models.IntegerField(db_index=True, verbose_name='Number'),
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='code',
            field=models.SlugField(default='', max_length=20, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='edition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tipitaka.edition', verbose_name='Edition'),
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='line_number',
            field=models.IntegerField(default=0, null=True, verbose_name='Line no'),
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='page',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='volume', chained_model_field='volume', on_delete=django.db.models.deletion.CASCADE, to='tipitaka.page', verbose_name='Page'),
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='position',
            field=models.IntegerField(default=0, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='volume',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='edition', chained_model_field='edition', on_delete=django.db.models.deletion.CASCADE, to='tipitaka.volume', verbose_name='Volume'),
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='word',
            field=models.CharField(default='', max_length=150, verbose_name='Word'),
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='word_roman_script',
            field=models.CharField(default='', max_length=150, null=True, verbose_name='Word in roman script'),
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='word_seq',
            field=models.CharField(default='', max_length=150, verbose_name='Word sequence'),
        ),
        migrations.AlterField(
            model_name='wordlist',
            name='wordlist_version',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='edition', chained_model_field='edition', on_delete=django.db.models.deletion.CASCADE, to='tipitaka.wordlistversion', verbose_name='Wordlist version'),
        ),
        migrations.AlterField(
            model_name='wordlistversion',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AlterField(
            model_name='wordlistversion',
            name='edition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tipitaka.edition', verbose_name='Edition'),
        ),
        migrations.AlterField(
            model_name='wordlistversion',
            name='version',
            field=models.IntegerField(default=0, verbose_name='Version'),
        ),
    ]