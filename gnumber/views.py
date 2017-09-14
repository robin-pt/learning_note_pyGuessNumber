from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Results
from . import game, rules


class Index(generic.TemplateView):
    """ index view """
    template_name = "index.html"


class RankView(generic.ListView):
    template_name = "ranking.html"
    contex_object_name = "ranking_list"

    def get_queryset(self):
        """
        Return top 10 rank
        """
        return Results.objects.filter(result__lte=1).order_by('-result')[10:]

@login_required
def createRoom(request):
    room_id = game.create(request.user.id)
    return HttpResponseRedirect(reverse('gnumber:game', args=(room_id,)))

def gameRoom(request, room_id):
    if game.roomExist(room_id) != 1:
        return render(request, 'error_message.html', {'error_message': '遊戲不存在'})
    if game.roomMemberCounter(room_id) is False:
        return render(request, 'error_message.html', {'error_message': '房間已滿'})
    if game.userExistInRoom(room_id, request.user.id) == 0:
        result, message = game.userJoin(room_id, request.user.id)
        if not result:
            return render(request, 'error_message.html', {'error_message': message})
    return render(request, 'game_room.html')