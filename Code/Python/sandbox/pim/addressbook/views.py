from django.shortcuts import render_to_response, get_object_or_404
from pim.addressbook.models import Contact

def index(request):
    contact_list = Contact.objects.all().order_by('first_name', 'last_name')
    
    return render_to_response('contact_list.html', {'contact_list': contact_list})

def detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id) 

    return render_to_response('contact_detail.html', {'contact': contact})

