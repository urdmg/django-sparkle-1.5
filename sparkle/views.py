from django.shortcuts import render, get_object_or_404
from django.contrib.sites.models import Site
from django.utils import timezone
from sparkle.models import Application, Version, SystemProfileReport, SystemProfileReportRecord
from django.template.response import TemplateResponse


def appcast(request, application_slug):
    """Generate the appcast for the given application while recording any system profile reports"""
    
    application = get_object_or_404(Application, slug=application_slug)
    
    # if there are get parameters from the system profiling abilities
    if len(request.GET):
        # create a report and records of the keys/values
        report = SystemProfileReport.objects.create(ip_address=request.META.get('REMOTE_ADDR'))
        for key, value in request.GET.iteritems():
            record = SystemProfileReportRecord.objects.create(report=report, key=key, value=value)
    
    format = request.GET.get('format', 'xml')

    ct = {
	'xml': 'application/xml',
	'json': 'application/json',
    }

    t = TemplateResponse(request, 'sparkle/appcast.%s' % format, {'application': application}, content_type=ct[format])
    t.render()

    return t.render()
    #print(t.content)
    #return render(request, 'sparkle/appcast.xml', {'application': application})
    