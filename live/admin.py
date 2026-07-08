from django.contrib import admin
from .models import LiveStream, LiveChatMessage, LivePoll, LivePollVote


@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ao_vivo', 'data_agendamento', 'modulo']
    list_filter = ['ao_vivo']
    search_fields = ['titulo', 'descricao']


@admin.register(LiveChatMessage)
class LiveChatMessageAdmin(admin.ModelAdmin):
    list_display = ['stream', 'usuario', 'mensagem', 'created_at']
    list_filter = ['stream']


class LivePollVoteInline(admin.TabularInline):
    model = LivePollVote
    extra = 0
    readonly_fields = ['usuario', 'opcao_index']


@admin.register(LivePoll)
class LivePollAdmin(admin.ModelAdmin):
    list_display = ['pergunta', 'stream', 'ativa', 'created_at']
    list_filter = ['ativa', 'stream']
    inlines = [LivePollVoteInline]


@admin.register(LivePollVote)
class LivePollVoteAdmin(admin.ModelAdmin):
    list_display = ['poll', 'usuario', 'opcao_index']
    list_filter = ['poll']
