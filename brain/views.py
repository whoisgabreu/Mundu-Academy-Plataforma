from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.utils import render
from .models import BrainNote, BrainSavedItem, BrainStreak, BrainFork, BrainFollower

VALID_TABS = ['private', 'public', 'saved', 'forks', 'followers']


def _user_to_dict(user):
    perfil = getattr(user, 'perfil', None)
    return {
        'handle': user.username,
        'nome_completo': user.get_full_name() or user.username,
        'iniciais': perfil.iniciais if perfil else user.username[:2].upper(),
        'role': perfil.role if perfil else 'Membro Mundu',
    }


@login_required(login_url='/login')
def my_brain(request):
    tab = request.GET.get('tab', 'private')
    if tab not in VALID_TABS:
        tab = 'private'

    notes = BrainNote.objects.filter(user=request.user).order_by('-id')
    public_notes_count = notes.filter(is_public=True).count()

    my_brain_karma = 0
    perfil = getattr(request.user, 'perfil', None)
    if perfil:
        my_brain_karma = perfil.xp_total

    public_brain_notes = BrainNote.objects.filter(
        is_public=True
    ).exclude(user=request.user).order_by('-likes')[:10]
    public_notes_data = []
    for pn in public_brain_notes:
        author = _user_to_dict(pn.user)
        public_notes_data.append({
            'id': pn.id,
            'author_handle': author['handle'],
            'author_user': author,
            'title': pn.title,
            'body': pn.content,
            'source_label': pn.source,
            'source_handle': '',
            'tags': pn.tags,
            'likes': pn.likes,
            'comments': pn.comments_count,
            'saves': 0,
            'time_ago': pn.date,
        })

    saved_items = BrainSavedItem.objects.filter(user=request.user)
    saved_data = [{
        'id': item.item_id,
        'title': item.title,
        'type': item.item_type,
    } for item in saved_items]

    streak = BrainStreak.objects.filter(user=request.user).order_by('id')

    forks = BrainFork.objects.filter(user=request.user)

    followers = BrainFollower.objects.filter(user=request.user)
    followers_data = []
    for f in followers:
        try:
            user_obj = User.objects.get(username=f.follower_handle)
            follower_info = _user_to_dict(user_obj)
        except User.DoesNotExist:
            follower_info = {
                'handle': f.follower_handle,
                'nome_completo': f.follower_handle.replace('-', ' ').title(),
                'iniciais': (f.follower_handle[:2] if f.follower_handle else '?').upper(),
                'role': 'Membro Mundu',
            }
        followers_data.append({
            **follower_info,
            'since': f.since,
        })

    context = {
        'tab': tab,
        'notes': notes,
        'saved_items': saved_data,
        'streak': streak,
        'forks': forks,
        'followers': followers_data,
        'public_notes': public_notes_data,
        'public_notes_count': public_notes_count,
        'brain_karma': my_brain_karma,
    }

    return render(request, 'my_brain.html', context)
