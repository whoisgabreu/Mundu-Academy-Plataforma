from django.db.models import Count
from django.http import Http404
from core.utils import render
from guild.models import Community, Thread, Comment


def _time_ago(dt):
    from django.utils import timezone
    now = timezone.now()
    diff = now - dt
    if diff.days == 0:
        mins = diff.seconds // 60
        if mins < 1:
            return 'agora'
        if mins < 60:
            return f'há {mins}min'
        hours = mins // 60
        return f'há {hours}h' if hours < 24 else 'ontem'
    if diff.days == 1:
        return 'ontem'
    return f'há {diff.days} dias'


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
    ).order_by('-upvotes')[:20]
    enriched = [enrich_thread(t, t.reply_count) for t in threads]
    return render(request, 'guild.html', {
        'communities': communities,
        'threads': enriched,
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

    return render(request, 'community.html', {
        'community': community,
        'posts': posts,
        'sort': sort,
        'related_communities': related,
        'moderators': moderators,
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

    return render(request, 'thread.html', {
        'community': community,
        'post': post,
        'comments': comment_tree,
        'total_comments': total_comments,
        'related_communities': related,
        'moderators': moderators,
    })
