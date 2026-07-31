from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from core.utils import human_time_ago, render
from guild.forms import CommunityForm
from guild.models import Community, Thread, Comment, GuildMembership, GuildMission


def _can_manage_guild(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def _time_ago(dt):
    return human_time_ago(dt)


def resolve_user(handle):
    from django.contrib.auth.models import User
    try:
        u = User.objects.get(username=handle)
        p = u.perfil
        return {
            'handle': u.username,
            'nome_completo': u.get_full_name() or u.username,
            'iniciais': p.iniciais,
            'role': p.role,
            'karma': p.karma,
            'bio': p.bio,
        }
    except User.DoesNotExist:
        return {
            'handle': handle,
            'nome_completo': handle.replace('-', ' ').title(),
            'iniciais': handle[:2].upper(),
            'role': 'Membro Mundu',
            'karma': 0,
            'bio': '',
        }


def enrich_thread(t, reply_count=0):
    return {
        'id': t.id,
        'slug': t.slug,
        'title': t.title,
        'author': t.author_handle,
        'author_handle': t.author_handle,
        'author_user': resolve_user(t.author_handle),
        'community_slug': t.community.slug,
        'post_community_slug': t.community.slug,
        'community': t.community.name,
        'community_id': t.community_id,
        'time_ago': _time_ago(t.created_at),
        'tag': t.tag,
        'post_type': t.post_type,
        'preview': t.preview,
        'body': t.body,
        'url': t.url,
        'upvotes': t.upvotes,
        'replies': reply_count,
        'reply_count': reply_count,
    }


def build_comment_tree(comments_qs):
    comment_map = {}
    roots = []
    for c in comments_qs:
        d = enrich_comment(c)
        d['children'] = []
        comment_map[c.id] = d
    for c in comments_qs:
        d = comment_map[c.id]
        if c.parent_id and c.parent_id in comment_map:
            comment_map[c.parent_id]['children'].append(d)
        else:
            roots.append(d)
    return roots


def enrich_comment(c):
    return {
        'id': c.id,
        'author': c.author_handle,
        'author_handle': c.author_handle,
        'author_user': resolve_user(c.author_handle),
        'body': c.body,
        'upvotes': c.upvotes,
        'time_ago': _time_ago(c.created_at),
    }


def guild_home(request):
    communities = Community.objects.all()
    threads = Thread.objects.select_related('community').annotate(
        reply_count=Count('comments')
    )
    sort = request.GET.get('sort', 'hot')
    if sort == 'new':
        threads = threads.order_by('-created_at')
    elif sort == 'unanswered':
        threads = threads.filter(reply_count=0).order_by('-created_at')
    else:
        threads = threads.order_by('-upvotes')
    threads = threads[:20]
    enriched = [enrich_thread(t, t.reply_count) for t in threads]
    ranking = GuildMembership.objects.select_related('usuario', 'usuario__perfil', 'community').order_by('-xp')[:10]
    return render(request, 'guild.html', {
        'communities': communities,
        'threads': enriched,
        'sort': sort,
        'ranking': ranking,
        'can_manage_guild': _can_manage_guild(request.user),
    })


def community_detail(request, slug):
    from django.db.models import Count
    try:
        community = Community.objects.get(slug=slug)
    except Community.DoesNotExist:
        raise Http404('Comunidade não encontrada')

    sort = request.GET.get('sort', 'hot')
    qs = Thread.objects.filter(community=community).select_related('community').annotate(
        reply_count=Count('comments')
    )
    if sort == 'new':
        qs = qs.order_by('-created_at')
    elif sort == 'top':
        qs = qs.order_by('-upvotes')
    else:
        qs = qs.order_by('-upvotes')

    posts = [enrich_thread(t, t.reply_count) for t in qs]

    related = Community.objects.filter(slug__in=community.related)
    moderators = [resolve_user(h) for h in community.moderators]
    membership = None
    if request.user.is_authenticated:
        membership = GuildMembership.objects.filter(usuario=request.user, community=community).first()
    members = GuildMembership.objects.filter(community=community).select_related('usuario', 'usuario__perfil').order_by('-xp')[:30]
    missions = GuildMission.objects.filter(community=community, ativo=True)

    return render(request, 'community.html', {
        'community': community,
        'posts': posts,
        'sort': sort,
        'related_communities': related,
        'moderators': moderators,
        'membership': membership,
        'members': members,
        'missions': missions,
        'can_manage_guild': _can_manage_guild(request.user),
    })


def thread_detail(request, community_slug, post_slug):
    from django.db.models import Count
    try:
        community = Community.objects.get(slug=community_slug)
    except Community.DoesNotExist:
        raise Http404('Comunidade não encontrada')

    try:
        thread = Thread.objects.select_related('community').annotate(
            reply_count=Count('comments')
        ).get(slug=post_slug, community=community)
    except Thread.DoesNotExist:
        raise Http404('Post não encontrado')

    comments_qs = Comment.objects.filter(thread=thread).select_related('parent')
    comment_tree = build_comment_tree(comments_qs)
    total_comments = comments_qs.count()

    post = enrich_thread(thread, thread.reply_count)
    related = Community.objects.filter(slug__in=community.related)
    moderators = [resolve_user(h) for h in community.moderators]
    is_following_author = False
    if (
        request.user.is_authenticated
        and request.user.username != post['author_user']['handle']
    ):
        from django.contrib.auth.models import User
        from social.models import Follow

        author = User.objects.filter(username=post['author_user']['handle']).first()
        if author:
            is_following_author = Follow.objects.filter(
                seguidor=request.user,
                seguido=author,
            ).exists()

    return render(request, 'thread.html', {
        'community': community,
        'post': post,
        'comments': comment_tree,
        'total_comments': total_comments,
        'related_communities': related,
        'moderators': moderators,
        'is_following_author': is_following_author,
    })


@login_required(login_url='/login')
def guild_create(request):
    if not _can_manage_guild(request.user):
        messages.error(request, 'Apenas administradores podem criar comunidades.')
        return redirect('/guild')
    form = CommunityForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            community = form.save(commit=False)
            community.created_at = timezone.now().strftime('%b %Y')
            community.save()
            messages.success(request, 'Comunidade criada com sucesso.')
            return redirect('community', slug=community.slug)
        messages.error(request, 'Revise os campos destacados.')
    return render(request, 'guild_form.html', {
        'form': form,
        'title': 'Nova comunidade',
        'cancel_url': '/guild',
        'messages_list': list(messages.get_messages(request)),
    })


@login_required(login_url='/login')
def guild_edit(request, slug):
    if not _can_manage_guild(request.user):
        messages.error(request, 'Apenas administradores podem editar comunidades.')
        return redirect('/guild')
    community = get_object_or_404(Community, slug=slug)
    form = CommunityForm(request.POST or None, instance=community)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Comunidade atualizada com sucesso.')
            return redirect('community', slug=community.slug)
        messages.error(request, 'Revise os campos destacados.')
    return render(request, 'guild_form.html', {
        'form': form,
        'title': 'Editar comunidade',
        'cancel_url': f'/g/{community.slug}',
        'messages_list': list(messages.get_messages(request)),
    })


@login_required(login_url='/login')
@require_POST
def guild_delete(request, slug):
    if not _can_manage_guild(request.user):
        messages.error(request, 'Apenas administradores podem excluir comunidades.')
        return redirect('/guild')
    community = get_object_or_404(Community, slug=slug)
    community.delete()
    messages.success(request, 'Comunidade excluída com sucesso.')
    return redirect('/guild')
