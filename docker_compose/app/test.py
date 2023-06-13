import datetime

import pytz
from django.db import models
from django.db.models.functions import ExtractDay, Abs

filmwork_qs = Filmwork.objects.all()
date = timezone.make_aware(datetime.datetime(2018, 11, 8), timezone=pytz.UTC)
expr = ExtractDay(models.ExpressionWrapper(
    date - F('creation_date'),
    output_field=models.DateField(),
))
film = filmwork_qs.annotate(delta=expr).filter(delta__isnull=False).annotate(abs_delta=Abs('delta')).order_by('abs_delta').first()