# Create your views here.
from datetime import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.utils import simplejson
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import  csrf_protect
from SmartChecklist.calculations import *
from SmartChecklist.email_service import *
from SmartChecklist.forms import SubmitForm, RegistrationForm, UploadPromotedItemForm, DictionaryItemForm
from SmartChecklist.models import *
from settings import FIRST_PAGE_REDIRECT_URL, BUILD_ID, MEDIA_ROOT

@never_cache
@csrf_protect
def index(request):
    request_context = RequestContext(request)
    request_context['BUILD_ID'] = BUILD_ID
    return render_to_response('index.html', {}, context_instance=request_context)


@never_cache
def last_page(request):
    request_context = RequestContext(request)
    return render_to_response('last_page.html', {}, context_instance=request_context)


@never_cache
def first_page(request):
    request_context = RequestContext(request)
    request_context['BUILD_ID'] = BUILD_ID
    return render_to_response('first_page.html', {}, context_instance=request_context)


@never_cache
def activate_user(request):
    if request.method == 'GET' and 'id' in request.GET:
        filter = User.objects.filter(id=request.GET['id'])
        if filter.exists():
            user = filter[0]
            user.is_active = True
            user.save()

        return render_to_response('activate_user.html', {}, context_instance=RequestContext(request))

    return HttpResponseRedirect(FIRST_PAGE_REDIRECT_URL)


@never_cache
@csrf_protect
def join_now(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        context['form'] = form

        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(user=user)

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.is_active = False
            user.save()

            context['message'] = send_confirmation_mail(user, request.get_host())

    return render_to_response('join_now.html', {}, context_instance=context)


@never_cache
@csrf_protect
def checklist(request):
    checklist_dict = {}
    if request.user.is_authenticated() and 'id' in request.GET:
        created_checklists_exist = CheckList.objects.filter(creator=request.user, id=request.GET['id']).exists()
        profile_checklists_exist = UserProfile.objects.filter(user=request.user, checklists__id=request.GET['id']).exists()

        if created_checklists_exist or profile_checklists_exist:
            checklist = CheckList.objects.get_or_create(id=request.GET['id'])[0]
            for item in checklist.items.all():
                if not item.category.name in checklist_dict:
                    checklist_dict[item.category.name] = list()
                if not hasattr(item, "promoteditem"):
                    checklist_dict[item.category.name].append(item)
                else:
                    checklist_dict[item.category.name].append(item.promoteditem)

    context = RequestContext(request)
    context['checklist'] = checklist_dict
    return render_to_response('checklist.html', {}, context_instance=context)


@never_cache
@csrf_protect
def history(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return HttpResponseRedirect(FIRST_PAGE_REDIRECT_URL)

        context = RequestContext(request)
        context['checklists'] = CheckList.objects.filter(creator=request.user).all()
        context['BUILD_ID'] = BUILD_ID

        return render_to_response('history.html', {}, context_instance=context)

    raise Http404


@never_cache
@csrf_protect
def check_done(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseRedirect(FIRST_PAGE_REDIRECT_URL)

        checklist = CheckList.objects.filter(id=request.POST['checklist_id'])[0]
        checklist.last_update_time = datetime.today()
        checklist.save()

        return HttpResponse()

@never_cache
@csrf_protect
def my_desk(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return HttpResponseRedirect(FIRST_PAGE_REDIRECT_URL)

        profile = request.user.get_profile()
        context = RequestContext(request)
        context['checklists'] = profile.checklists.all()
        context['BUILD_ID'] = BUILD_ID

        return render_to_response('my_desk.html', {}, context_instance=context)

    raise Http404

@never_cache
@csrf_protect
def statistics(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return HttpResponseRedirect(FIRST_PAGE_REDIRECT_URL)

        context = RequestContext(request)
        profile = request.user.get_profile()
        query = profile.checklists.annotate(Sum('items__price')).values_list('creation_time', 'last_update_time', 'items__price__sum')

        output = []
        for item in query:
            if item[1]:
                output.append([item[1].strftime("%s"), str(item[2])])
            else:
                output.append([item[0].strftime("%s"), str(item[2])])

        output.sort()
        context['weekly_data'] = simplejson.dumps(output)
        context['BUILD_ID'] = BUILD_ID

        return render_to_response('statistics.html', {}, context_instance=context)

    raise Http404

@csrf_protect
def stores(request):
    if request.method == 'GET':
        context = RequestContext(request)
        context['stores'] = Store.objects.all()
        context['BUILD_ID'] = BUILD_ID

        return render_to_response('stores.html', {}, context_instance=context)

    raise Http404


@never_cache
@csrf_protect
def offers(request):
    if request.method == 'GET':
        context = RequestContext(request)
        context['offers'] = PromotedItem.objects.filter(store=request.GET['store_id'])
        context['store_id'] = request.GET['store_id']
        context['BUILD_ID'] = BUILD_ID

        return render_to_response('offers.html', {}, context_instance=context)

    raise Http404


@never_cache
def contact_us(request):
    if request.method == 'POST':
        context = RequestContext(request)
        admin = User.objects.filter(is_superuser=True)[0]
        context['message'] = send_message(admin.email, request.POST['email'], request.POST['message'])
        return render_to_response('contact_us.html', {}, context_instance=context)
    else:
        return render_to_response('contact_us.html', {}, context_instance=RequestContext(request))


@never_cache
def send_checklist(request):
    if request.method == 'POST':
        return HttpResponse(send_checklist_mail(request.POST['recipient'], request.POST['plain_html'], request.POST['plain_text']))
    else:
        return render_to_response('send_checklist.html', {}, context_instance=RequestContext(request))


@never_cache
def create_checklist(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if not form.is_valid():
            return HttpResponse('Data is not valid!')
        elif not request.user.is_authenticated():
            return HttpResponse('Please login for sending!')
        else:
            items = []
            checklists = []
            recipient = form.cleaned_data['recipient']
            recipient_user = User.objects.filter(username=recipient)
            offers_json = simplejson.loads(form.cleaned_data['offers_json'])
            checklist_json = simplejson.loads(form.cleaned_data['checklist_json'])

            if not len(checklist_json):
                return HttpResponse('Checklist is empty! Please try again.')
            if not recipient_user:
                return HttpResponse('User doesn\'t exist! Please try again.')
            if len(recipient_user) > 1:
                return HttpResponse('Multiple users are found! Please try again.')

            if len(offers_json) > 0:
                items.extend(PromotedItem.objects.filter(id__in=offers_json))

            for obj in checklist_json:
                category = obj if type(checklist_json) is dict else 'N/A'
                dict_items = checklist_json[obj] if type(checklist_json) is dict else [obj]
                found_category = DictionaryCategory.objects.get_or_create(name=category)[0]
                for item in dict_items:
                    item_to_add = DictionaryItem.objects.create(name=item, category=found_category)
                    items.append(item_to_add)
                    item_to_add.save()

            checklist = CheckList(name=form.cleaned_data['name'], description=form.cleaned_data['desc'], creator=request.user)
            checklist.save()

            checklists.append(checklist)
            checklist.items = items
            checklist.save()

            profile = recipient_user[0].get_profile()
            checklists.extend(profile.checklists.all())
            profile.checklists = checklists
            profile.save()

            return HttpResponse('Your checklist was successfully sent!')

    raise Http404


@never_cache
def get_categories(request):
    if request.method == 'POST':
        categorized = categorize(request.POST['words'])
        return HttpResponse(simplejson.dumps(categorized), mimetype='application/json')

    raise Http404


@never_cache
def get_simple_checklist(request):
    if request.method == 'POST':
        checklist = get_checklist(request.POST['words'])
        return HttpResponse(simplejson.dumps(checklist), mimetype='application/json')

    raise Http404


@never_cache
def get_todo_list(request):
    if request.method == 'POST':
        todo_list = get_todo_items(request.POST['words'].lower())
        return HttpResponse(simplejson.dumps(todo_list), mimetype='application/json')

    raise Http404


@never_cache
def get_delimited(request):
    if request.method == 'POST':
        delimited_list = get_delimited_items(request.POST['words'].lower())
        return HttpResponse(simplejson.dumps(delimited_list), mimetype='application/json')

    raise Http404


@never_cache
@csrf_protect
def details(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(FIRST_PAGE_REDIRECT_URL)

    if request.method == 'GET':
        item = DictionaryItem.objects.get(id=request.GET['id'])
        return render(request, 'details.html', {'form': DictionaryItemForm(instance=item), 'id': item.id})
    elif request.method == 'POST':
        item = DictionaryItem.objects.get(id=request.POST['id'])
        form = DictionaryItemForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            checklist = CheckList.objects.filter(items__id=item.id)[0]
            return render(request, 'details.html', {'form': form, 'id': item.id, 'checklist_id': checklist.id})

        return render(request, 'details.html', {'form': form, 'id': item.id})

    raise Http404


@never_cache
@csrf_protect
def store_admin(request):
    if not request.user.is_authenticated() or not request.user.is_staff:
        return HttpResponseRedirect(FIRST_PAGE_REDIRECT_URL)

    if request.method == 'GET':
        return render(request, 'store_admin.html', {'form': UploadPromotedItemForm()})
    elif request.method == 'POST':
        form = UploadPromotedItemForm(request.POST, request.FILES)
        if form.is_valid():
            promoted_item = form.save()

            with open("%s/promoted_items/%s.jpg" % (MEDIA_ROOT, promoted_item.id), 'wb+') as destination:
                for chunk in request.FILES['image'].chunks():
                    destination.write(chunk)

        return render(request, 'store_admin.html', {'form': form})
