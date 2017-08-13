import csv
import pytz
import sys
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import smart_str
from django.http import HttpResponse

def format_date(self, obj):
    date = timezone.localtime(obj.valid_till, pytz.timezone(settings.TIME_ZONE))
    return date.strftime('%d/%m/%y %H:%M:%S')


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=None, data_modify_function=None):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta

        if not fields:
            field_names = [field.name for field in opts.fields]
        else:
            field_names = fields

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % opts

        writer = csv.writer(response, quoting=csv.QUOTE_ALL)
        if not header:
            writer.writerow(field_names)
        else:
            writer.writerow(header)
        for obj in queryset:
            row = [getattr(obj, field)() if callable(getattr(obj, field)) else getattr(obj, field) for field in
                   field_names]
            if data_modify_function:
                row = data_modify_function(row)
            orow = []
            for item in row:
                if hasattr(item, 'now'):
                    orow.append(format_date(item, obj))
                else:
                    orow.append(smart_str(item))
            writer.writerow(orow)
        return response

    export_as_csv.short_description = description
    return export_as_csv