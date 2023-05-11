# Generated by Django 4.2 on 2023-04-30 07:12

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('tipitaka', '0018_alter_tableofcontent_wordlist_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordlist',
            name='wordlist_version',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='edition', chained_model_field='edition', on_delete=django.db.models.deletion.CASCADE, to='tipitaka.wordlistversion', verbose_name='wordlist version'),
        ),
    ]