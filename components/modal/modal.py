from django_components import component
# import static urls
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.conf import settings

@component.register('modal')
class Modal(component.Component):
    template_name = 'modal.html'
    
    def get_context_data(self, title, body, footer):
        return {
            'title': title,
            'body': body,
            'footer':   footer,
        }
    
    class Media:
        css = 'modal.css'
        js = 'modal.js'
