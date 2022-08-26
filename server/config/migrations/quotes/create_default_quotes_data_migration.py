import json

from django.db import migrations


def create_default_quotes(apps, schema_editor):

    with open('apps/quotes/models/default_quotes.json', 'r') as json_default_quotes:
        default_quotes_text = json.load(json_default_quotes)

    Quote = apps.get_model('quotes', 'Quote')

    if not Quote.objects.exists():
        default_quotes = []

        for quote_text in default_quotes_text:
            default_quote = Quote(text=quote_text)
            default_quotes.append(default_quote)

        Quote.objects.bulk_create(default_quotes)


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_quotes),
    ]
