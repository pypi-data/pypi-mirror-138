from datetime import date, datetime

import pytz
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import localdate

from ..models.journals import Journal
from ..rocketchat import RocketChat, get_rc_id
from ..views import leader_or_staff_required


@leader_or_staff_required
def participants(request, journal_id):
    qs = Journal.objects.all()
    if not request.user.is_staff:
        qs = qs.filter(leaders=request.leader)
    journal = get_object_or_404(qs, id=journal_id)

    try:
        d = localdate(datetime.utcfromtimestamp(int(request.GET["date"])).replace(tzinfo=pytz.utc))
    except (KeyError, ValueError):
        d = date.today()

    return JsonResponse(
        {
            "participants": list({"value": p.id, "label": str(p)} for p in journal.get_valid_participants(d)),
        }
    )


def rocketchat(request):
    """
    Implements API for Rocket.Chat IFrame authentication
    """
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    rc = RocketChat()
    rc.sync_user(request.user)

    return JsonResponse({"loginToken": rc.create_login_token(get_rc_id(request.user))})
