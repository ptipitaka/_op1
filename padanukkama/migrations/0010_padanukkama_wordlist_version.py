# Generated by Django 4.2 on 2023-05-08 08:47

from django.db import migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('tipitaka', '0021_alter_commonreference_wordlist_version_and_more'),
        ('padanukkama', '0009_remove_padanukkama_structure_padanukkama_structure'),
    ]

    operations = [
        migrations.AddField(
            model_name='padanukkama',
            name='wordlist_version',
            field=smart_selects.db_fields.ChainedManyToManyField(blank=True, chained_field='table_of_content', chained_model_field='table_of_content', to='tipitaka.wordlistversion', verbose_name='Wordlist Version'),
        ),
    ]