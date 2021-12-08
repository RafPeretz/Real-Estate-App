from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact


# Create your views here.

def contact(request):
    if request.method == "POST":
        listing = request.POST['listing']
        listing_id = request.POST['listing_id']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        # contact_date = request.POST['contact_date']
        user_id = request.POST['user_id']
        name = request.POST['name']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, "You have already made an inquery for this listing")
                return redirect(f'../listings/{listing_id}/listing/')

        contact = Contact(
            listing=listing,
            listing_id=listing_id,
            name=name,
            email=email,
            phone=phone,
            message=message,
            # contact_date=contact_date,
            user_id=user_id
        )
        contact.save()
        # SENDMAIL
        send_mail(
            'Property Listing Inquiry',
            f'There has been an inquiry for {listing}. Sign into the admin panel for more information.',
            'rafaelperetz2@gmail.com',
            [realtor_email, 'rafaelperetz2@gmail.com'],
            fail_silently=False
        )

        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon.')
        return redirect('/listings/' + listing_id)
