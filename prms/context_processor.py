# Description: Context processor for global context.
def global_context_processor(request):
    global_context = request.session.get('global_context', 'No data found')
    return {'global_context': global_context}