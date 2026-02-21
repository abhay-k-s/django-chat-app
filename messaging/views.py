from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import User
from .models import Message
from django.db.models import Q


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'users': users})



@login_required
def chat_view(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(Q(sender=request.user, receiver=receiver) |Q(sender=receiver, receiver=request.user)).order_by("timestamp")
    Message.objects.filter(sender=receiver,receiver=request.user,is_read=False).update(is_read=True)
    return render(request, "chat.html", {"receiver": receiver,"messages": messages})