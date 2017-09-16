from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Results
from . import game


class Index(View):
    """ index view """
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        """
        Return room list
        """
        return render(request, self.template_name, {"room_list": game.listRoom(),})


class RankView(generic.ListView):
    model = Results
    template_name = "ranking.html"
    def get_context_data(self, **kwargs):
        """
        Return top 10 rank
        """
        context = super(RankView, self).get_context_data(**kwargs)
        context["ranking_list"] = Results.objects.filter(result__lte=1).order_by('-result')
        return context


@login_required
def createRoom(request):
    room_id = game.create(request.user.id)
    status = game.startGame(room_id)
    if not status:
        return render(request, 'error_message.html', {'error_message': '開局失敗'})
    return HttpResponseRedirect(reverse('gnumber:game', args=(room_id,)))


@login_required
def gameRoom(request, room_id):
    if game.roomExist(room_id) != 1:
        return render(request, 'error_message.html', {'error_message': '遊戲不存在'})
    if game.roomMemberCounter(room_id) is False:
        return render(request, 'error_message.html', {'error_message': '房間已滿'})
    if game.userExistInRoom(room_id, request.user.id) == 0:
        result, message = game.userJoin(room_id, request.user.id)
        if not result:
            return render(request, 'error_message.html', {'error_message': message})

    gameOver = False
    result = None

    if request.method == "POST":
        game.userIncre(room_id, request.user.id)
        inputNumber = request.POST['InputNumber']
        status, response = game.checkMatch(room_id, inputNumber)
        if not status:
            print(status, response)
            gameOver = True
            game.endGame(room_id)
        else:
            if int(response[0]) == 4:
                gameOver = True
                game.endGame(room_id)
                thisResult = int(game.getUserResult(room_id, request.user.id))
                if Results.objects.filter(user=request.user).exists() > 0:
                    lastRecord = get_object_or_404(Results, user=request.user)
                    if lastRecord is not None:
                        if lastRecord.result == 0 or lastRecord.result > thisResult:
                            lastRecord.result = thisResult
                            lastRecord.save()
                else:
                    createRecord = Results.objects.create(user=request.user, result=thisResult)
                    createRecord.save()
            result = "{A}A{B}B".format(A=response[0], B=response[1])
            
    
    status = game.getUsersInRoom(room_id)
    if not isinstance(status, dict):
        return render(request, 'error_message.html', {'error_message': '請輸入合法路徑'})
    outputResult = {}
    for key in status:
        outputResult[User.objects.get(id=key).username] = status.get(key)

    return render(request, 'game_room.html', {'game_status': outputResult,
                                              'guess_result': result,
                                              'game_over': gameOver})
