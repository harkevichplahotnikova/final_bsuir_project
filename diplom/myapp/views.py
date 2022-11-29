from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from myapp.models import get_subscription_types, get_players, get_matches, get_current_user_email, get_predictions, get_subscription_types_by_id, insert_new_user_sub, get_matches_by_name, insert_new_user_prediction,get_subs_analysis, get_current_user_predictions_amount, get_current_user_subscription, get_matches_by_player_id, get_players_by_id, get_subs_analysis_by_date, load_new_today_matches
from django.contrib.auth.models import User
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def test_view(request):
    load_new_today_matches()
    subscription_ids, subscription_types, subscription_descs, subscription_prices = get_subscription_types()
    subscriptions = []
    for i in range(len(subscription_ids)):
        subscriptions.append({ 'subscription_id': subscription_ids[i],
                'subscription_type' : subscription_types[i],
                'subscription_price': subscription_prices[i],
                'subscription_desc': subscription_descs[i]})
    raw_user_context = get_current_user_email(request.user.id)
    user ={}
    for i in range(len(raw_user_context)):
        user['id'] = raw_user_context[i][0]
        user['email'] = raw_user_context[i][1]
        
    raw_user_context = get_current_user_predictions_amount(request.user.id)
    raw_sub_context = get_current_user_subscription(request.user.id)
    subscription_id = raw_sub_context[0][0]
    user['predictions'] = raw_user_context[0][0]
    context = { 'subscriptions' : subscriptions,
                'user' : user,
                'subscription_id': subscription_id}
    print(context)
    return render(request, 'base.html', context)


def players_view(request):
    raw_context = get_players()
    players = []
    for i in range(len(raw_context)):
        players.append({ 'player_id': raw_context[i][0],
                'player_first_name': raw_context[i][1],
                'player_last_name': raw_context[i][2],
                'player_full_name': raw_context[i][3],
                'player_country': raw_context[i][4],
                'player_gender': raw_context[i][5],
                'player_height': raw_context[i][6],
                'player_weight': raw_context[i][7]
                })
    raw_user_context = get_current_user_email(request.user.id)
    user ={}
    for i in range(len(raw_user_context)):
        user['id'] = raw_user_context[i][0]
        user['email'] = raw_user_context[i][1]
    raw_user_context = get_current_user_predictions_amount(request.user.id)
    user['predictions'] = raw_user_context[0][0]
    context = { 'players' : players,
                'user' : user }
    return render(request, 'players.html', context)



def matches_view(request):
    raw_context = get_matches(request.user.id)
    matches = []
    for i in range(len(raw_context)):
        matches.append({ 'match_id': raw_context[i][0],
                'match_name': raw_context[i][1],
                'match_desc': raw_context[i][2],
                'match_date': raw_context[i][3],
                'first_player_full_name': raw_context[i][4],
                'second_player_full_name': raw_context[i][5],
                'is_predicted': raw_context[i][6]
                })
    raw_user_context = get_current_user_email(request.user.id)
    user ={}
    for i in range(len(raw_user_context)):
        user['id'] = raw_user_context[i][0]
        user['email'] = raw_user_context[i][1]
    raw_user_context = get_current_user_predictions_amount(request.user.id)
    user['predictions'] = raw_user_context[0][0]
    context = { 'matches' : matches,
                'user' : user }
    return render(request, 'matches.html', context)

@login_required(login_url='/')
def predictions_view(request): 
    raw_context = get_predictions(request.user.id)
    predictions = []
    for i in range(len(raw_context)):
        predictions.append({ 'prediction_id': raw_context[i][0],
                'user_id': raw_context[i][1],
                'user_prediction_id': raw_context[i][2],
                'match_name': raw_context[i][3],
                'prediction_status_code': raw_context[i][4],
                'prediction_result': raw_context[i][5],
                'prediction_date': raw_context[i][6]
                })
    raw_user_context = get_current_user_email(request.user.id)
    user ={}
    for i in range(len(raw_user_context)):
        user['id'] = raw_user_context[i][0]
        user['email'] = raw_user_context[i][1]
    raw_user_context = get_current_user_predictions_amount(request.user.id)
    user['predictions'] = raw_user_context[0][0]
    isDisplay = 0
    if len(predictions) > 0:
        isDisplay = 1
    context = { 'predictions' : predictions,
                'user' : user,
                'isDisplay': isDisplay}
    return render(request, 'predictions.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')



def login_operation_view(request):
    print(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')

    


def login_view(request):
    return render(request, 'login.html', {})

def register_view(request):
    return render(request, 'register.html', {})


def register_operation_view(request):
    print(request.POST)
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    if password == confirm_password:
        user = User.objects.create_user(username, email, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')

@login_required(login_url='/login')
def subscriptions_view(request, id):
    subscription_ids, subscription_types, subscription_prices = get_subscription_types_by_id(id)
    subscriptions = []
    for i in range(len(subscription_ids)):
        subscriptions.append({ 'subscription_id': subscription_ids[i],
                'subscription_type': subscription_types[i],
                'subscription_price': subscription_prices[i]})
    raw_user_context = get_current_user_email(request.user.id)
    user ={}
    for i in range(len(raw_user_context)):
        user['id'] = raw_user_context[i][0]
        user['email'] = raw_user_context[i][1]
    raw_user_context = get_current_user_predictions_amount(request.user.id)
    user['predictions'] = raw_user_context[0][0]
    context = { 'subscriptions' : subscriptions,
                'user' : user }
    return render(request, 'subscriptions.html', context)


def confirm_sub_view(request, id):
    result = insert_new_user_sub(id, request.user.id)
    return HttpResponseRedirect('/')



def prediction_confirm_view(request, name):
    raw_context = get_matches_by_name(name)
    matches = []
    for i in range(len(raw_context)):
        matches.append({ 'match_id': raw_context[i][0],
                'match_name': raw_context[i][1],
                'match_desc': raw_context[i][2],
                'match_date': raw_context[i][3],
                'first_player_full_name': raw_context[i][4],
                'second_player_full_name': raw_context[i][5]
                })
    raw_user_context = get_current_user_email(request.user.id)
    user ={}
    for i in range(len(raw_user_context)):
        user['id'] = raw_user_context[i][0]
        user['email'] = raw_user_context[i][1]
    raw_user_context = get_current_user_predictions_amount(request.user.id)
    user['predictions'] = raw_user_context[0][0]
    context = { 'matches' : matches,
                'user' : user }
    return render(request, 'prediction_confirm.html', context)


def prediction_confirm_operation_view(request, name):
    result = insert_new_user_prediction(name, request.user.id)
    return HttpResponseRedirect('/')



def analysis_view(request):
    raw_context = get_subs_analysis()
    print(raw_context)
    return render(request, 'analysis.html', {'values': raw_context})


def matches_by_player_view(request, id):
    raw_context = get_matches_by_player_id(id)
    matches = []
    for i in range(len(raw_context)):
        matches.append({ 'match_id': raw_context[i][0],
                'match_name': raw_context[i][1],
                'match_desc': raw_context[i][2],
                'match_date': raw_context[i][3],
                'first_player_full_name': raw_context[i][4],
                'second_player_full_name': raw_context[i][5],
                'player_full_name': raw_context[i][6]
                })
    raw_user_context = get_current_user_email(request.user.id)
    user ={}
    for i in range(len(raw_user_context)):
        user['id'] = raw_user_context[i][0]
        user['email'] = raw_user_context[i][1]
    raw_user_context = get_current_user_predictions_amount(request.user.id)
    user['predictions'] = raw_user_context[0][0]

    raw_player_context = get_players_by_id(id)
    player ={}
    player['full_name'] = raw_player_context[0][0]
    isDisplay = 0
    if len(matches) > 0:
        isDisplay = 1
    context = { 'matches' : matches,
                'user' : user,
                'player': player,
                'isDisplay': isDisplay}
    return render(request, 'players_by_id.html', context)


def subscription_download_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(200, 800, "Hello world")
    p.drawString(200, 780, "Hello world")
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')



def analysis_operation_view(request):
    print(request.POST)
    date_from = request.POST['datefrom']
    date_to = request.POST['dateto']
    raw_context = get_subs_analysis_by_date(date_from, date_to)
    print(raw_context)
    return render(request, 'analysis.html', {'values': raw_context})