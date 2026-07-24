import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Avg, Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from core.utils import render
from cursos.models import (
    Alternativa,
    Aula,
    Certificate,
    CertificateTemplate,
    Modulo,
    Questao,
    Quiz,
    TentativaQuiz,
)
from cursos.services import certificate_context, certificate_pdf_bytes, issue_certificate
from professor.forms import (
    AlternativaFormSet,
    AulaForm,
    CertificateIssueForm,
    CertificateTemplateForm,
    ModuloForm,
    QuestaoForm,
    QuizForm,
)
from professor.permissions import is_professor, professor_required


PAGE_SIZE = 10


def _page(request, queryset, per_page=PAGE_SIZE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get('page') or 1)


def _messages(request):
    return list(messages.get_messages(request))


def _ctx(request, **context):
    context.setdefault('prof_nav', 'dashboard')
    context.setdefault('messages_list', _messages(request))
    return context


def _query(request):
    return (request.GET.get('q') or '').strip()


def _default_quiz_questions():
    return [
        {
            'enunciado': '',
            'tipo': 'multipla_escolha',
            'alternativas': [
                {'texto': '', 'correta': True},
                {'texto': '', 'correta': False},
            ],
        }
    ]


def _questions_payload_from_quiz(quiz):
    questions = quiz.questoes.prefetch_related('alternativas').order_by('ordem')
    return [
        {
            'enunciado': question.enunciado,
            'tipo': question.tipo,
            'alternativas': [
                {'texto': answer.texto, 'correta': answer.correta}
                for answer in question.alternativas.all()
            ],
        }
        for question in questions
    ] or _default_quiz_questions()


def _questions_payload_from_request(request):
    raw_payload = request.POST.get('questions_payload') or ''
    if not raw_payload:
        return _default_quiz_questions(), []
    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError:
        return _default_quiz_questions(), ['Não foi possível ler as perguntas. Recarregue a página e tente novamente.']
    if not isinstance(payload, list):
        return _default_quiz_questions(), ['O formato das perguntas é inválido.']
    return payload, []


def _validate_quiz_questions(payload):
    errors = []
    normalized = []
    allowed_types = {choice[0] for choice in Questao.TIPOS}

    for index, question in enumerate(payload, start=1):
        if not isinstance(question, dict):
            errors.append(f'Pergunta {index}: dados inválidos.')
            continue
        enunciado = (question.get('enunciado') or '').strip()
        tipo = question.get('tipo') or 'multipla_escolha'
        alternatives_raw = question.get('alternativas') or []
        has_any_answer = any((alt.get('texto') or '').strip() for alt in alternatives_raw if isinstance(alt, dict))
        if not enunciado and not has_any_answer:
            continue
        if not enunciado:
            errors.append(f'Pergunta {index}: informe o enunciado.')
        if tipo not in allowed_types:
            errors.append(f'Pergunta {index}: tipo inválido.')
            tipo = 'multipla_escolha'

        alternatives = []
        for alt in alternatives_raw:
            if not isinstance(alt, dict):
                continue
            texto = (alt.get('texto') or '').strip()
            if not texto:
                continue
            alternatives.append({
                'texto': texto,
                'correta': bool(alt.get('correta')),
            })

        if tipo == 'verdadeiro_falso' and len(alternatives) != 2:
            errors.append(f'Pergunta {index}: verdadeiro/falso precisa ter exatamente 2 respostas.')
        elif tipo == 'multipla_escolha' and len(alternatives) < 2:
            errors.append(f'Pergunta {index}: adicione pelo menos 2 respostas.')

        correct_count = sum(1 for alt in alternatives if alt['correta'])
        if alternatives and correct_count != 1:
            errors.append(f'Pergunta {index}: marque exatamente 1 resposta correta.')

        normalized.append({
            'enunciado': enunciado,
            'tipo': tipo,
            'alternativas': alternatives,
        })

    normalized = [item for item in normalized if item['enunciado'] or item['alternativas']]
    if not normalized:
        errors.append('Adicione pelo menos uma pergunta ao quiz.')
    return normalized, errors


def _questions_payload_json(payload):
    return json.dumps(payload, ensure_ascii=False).replace('</', '<\\/')


def _create_quiz_questions(quiz, questions):
    for question_index, question in enumerate(questions, start=1):
        questao = Questao.objects.create(
            quiz=quiz,
            enunciado=question['enunciado'],
            tipo=question['tipo'],
            ordem=question_index,
        )
        for answer_index, answer in enumerate(question['alternativas'], start=1):
            Alternativa.objects.create(
                questao=questao,
                texto=answer['texto'],
                correta=answer['correta'],
                ordem=answer_index,
            )


@professor_required
def dashboard(request):
    modules = Modulo.objects.annotate(aulas_count=Count('aulas'), alunos_count=Count('progressos__usuario', distinct=True))
    context = {
        'prof_nav': 'dashboard',
        'cards': [
            {'label': 'Módulos', 'value': modules.count(), 'icon': 'layout-dashboard'},
            {'label': 'Aulas', 'value': Aula.objects.count(), 'icon': 'play-circle'},
            {'label': 'Quizzes', 'value': Quiz.objects.count(), 'icon': 'list-checks'},
            {'label': 'Certificados', 'value': Certificate.objects.count(), 'icon': 'award'},
        ],
        'draft_modules': Modulo.objects.filter(status='draft').count(),
        'published_modules': Modulo.objects.filter(status='published').count(),
        'students_count': modules.aggregate(total=Count('progressos__usuario', distinct=True))['total'] or 0,
        'recent_modules': modules.order_by('-created_at')[:5],
        'recent_attempts': TentativaQuiz.objects.select_related('usuario', 'quiz').order_by('-concluido_em')[:5],
    }
    return render(request, 'professor/dashboard.html', _ctx(request, **context))


@professor_required
def module_list(request):
    q = _query(request)
    queryset = Modulo.objects.annotate(
        aulas_count=Count('aulas', distinct=True),
        alunos_count=Count('progressos__usuario', distinct=True),
    )
    if q:
        queryset = queryset.filter(Q(titulo__icontains=q) | Q(descricao__icontains=q))
    page_obj = _page(request, queryset.order_by('ordem', 'titulo'))
    return render(request, 'professor/module_list.html', _ctx(request, prof_nav='modules', page_obj=page_obj, q=q))


@professor_required
def module_create(request):
    form = ModuloForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            modulo = form.save()
            messages.success(request, 'Módulo criado com sucesso.')
            return redirect('professor:module_detail', pk=modulo.pk)
        messages.error(request, 'Revise os campos destacados.')
    return render(request, 'professor/form.html', _ctx(
        request,
        prof_nav='modules',
        title='Novo módulo',
        form=form,
        cancel_url='/professor/modulos/',
        enctype=False,
    ))


@professor_required
def module_detail(request, pk):
    modulo = get_object_or_404(
        Modulo.objects.annotate(
            aulas_count=Count('aulas', distinct=True),
            alunos_count=Count('progressos__usuario', distinct=True),
        ),
        pk=pk,
    )
    aulas = modulo.aulas.order_by('ordem')
    quizzes = Quiz.objects.filter(modulo=modulo).select_related('aula').order_by('ordem')
    return render(request, 'professor/module_detail.html', _ctx(
        request,
        prof_nav='modules',
        modulo=modulo,
        aulas=aulas,
        quizzes=quizzes,
    ))


@professor_required
def module_edit(request, pk):
    modulo = get_object_or_404(Modulo, pk=pk)
    form = ModuloForm(request.POST or None, instance=modulo)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Módulo atualizado com sucesso.')
            return redirect('professor:module_detail', pk=modulo.pk)
        messages.error(request, 'Revise os campos destacados.')
    return render(request, 'professor/form.html', _ctx(
        request,
        prof_nav='modules',
        title='Editar módulo',
        form=form,
        cancel_url=f'/professor/modulos/{modulo.pk}/',
        enctype=False,
    ))


@professor_required
@require_POST
def module_delete(request, pk):
    modulo = get_object_or_404(Modulo, pk=pk)
    modulo.delete()
    messages.success(request, 'Módulo excluído com sucesso.')
    return redirect('professor:module_list')


@professor_required
@require_POST
def module_reorder(request):
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'erro': 'JSON inválido.'}, status=400)
    ordered_ids = payload.get('ordered_ids') or []
    if not isinstance(ordered_ids, list):
        return JsonResponse({'ok': False, 'erro': 'ordered_ids deve ser uma lista.'}, status=400)
    with transaction.atomic():
        for index, module_id in enumerate(ordered_ids):
            Modulo.objects.filter(id=module_id).update(ordem=index)
    return JsonResponse({'ok': True})


@professor_required
def lesson_list(request):
    q = _query(request)
    queryset = Aula.objects.select_related('modulo').order_by('modulo__ordem', 'ordem')
    if q:
        queryset = queryset.filter(Q(titulo__icontains=q) | Q(descricao__icontains=q) | Q(modulo__titulo__icontains=q))
    page_obj = _page(request, queryset)
    return render(request, 'professor/lesson_list.html', _ctx(request, prof_nav='lessons', page_obj=page_obj, q=q))


@professor_required
def lesson_create(request):
    form = AulaForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            aula = form.save()
            messages.success(request, 'Aula criada com sucesso.')
            return redirect('professor:lesson_detail', pk=aula.pk)
        messages.error(request, 'Revise os campos destacados.')
    return render(request, 'professor/form.html', _ctx(
        request,
        prof_nav='lessons',
        title='Nova aula',
        form=form,
        cancel_url='/professor/aulas/',
        enctype=True,
    ))


@professor_required
def lesson_detail(request, pk):
    aula = get_object_or_404(Aula.objects.select_related('modulo'), pk=pk)
    quizzes = aula.quizzes.order_by('ordem')
    return render(request, 'professor/lesson_detail.html', _ctx(request, prof_nav='lessons', aula=aula, quizzes=quizzes))


@professor_required
def lesson_edit(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    form = AulaForm(request.POST or None, request.FILES or None, instance=aula)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Aula atualizada com sucesso.')
            return redirect('professor:lesson_detail', pk=aula.pk)
        messages.error(request, 'Revise os campos destacados.')
    return render(request, 'professor/form.html', _ctx(
        request,
        prof_nav='lessons',
        title='Editar aula',
        form=form,
        cancel_url=f'/professor/aulas/{aula.pk}/',
        enctype=True,
    ))


@professor_required
@require_POST
def lesson_delete(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    aula.delete()
    messages.success(request, 'Aula excluída com sucesso.')
    return redirect('professor:lesson_list')


@professor_required
def quiz_list(request):
    q = _query(request)
    status = (request.GET.get('status') or '').strip()
    queryset = Quiz.objects.select_related('modulo', 'aula').annotate(questoes_count=Count('questoes')).order_by('modulo__ordem', 'ordem')
    if q:
        queryset = queryset.filter(Q(titulo__icontains=q) | Q(descricao__icontains=q) | Q(aula__titulo__icontains=q))
    if status in {'draft', 'published'}:
        queryset = queryset.filter(status=status)
    page_obj = _page(request, queryset)
    totals = Quiz.objects.aggregate(
        total=Count('id'),
        published=Count('id', filter=Q(status='published')),
        draft=Count('id', filter=Q(status='draft')),
    )
    return render(request, 'professor/quiz_list.html', _ctx(
        request,
        prof_nav='quizzes',
        page_obj=page_obj,
        q=q,
        status=status,
        total_quizzes=totals['total'] or 0,
        published_quizzes=totals['published'] or 0,
        draft_quizzes=totals['draft'] or 0,
        total_questions=Questao.objects.count(),
        total_attempts=TentativaQuiz.objects.count(),
    ))


@professor_required
def quiz_create(request):
    form = QuizForm(request.POST or None)
    questions_payload = _default_quiz_questions()
    question_errors = []
    if request.method == 'POST':
        questions_payload, payload_errors = _questions_payload_from_request(request)
        normalized_questions, question_errors = _validate_quiz_questions(questions_payload)
        question_errors = payload_errors + question_errors
        handled_error = False
        if form.is_valid() and not question_errors:
            try:
                with transaction.atomic():
                    quiz = form.save()
                    _create_quiz_questions(quiz, normalized_questions)
            except IntegrityError:
                messages.error(request, 'Já existe um quiz nessa ordem. Deixe a ordem vazia para gerar automaticamente.')
                handled_error = True
            else:
                messages.success(request, 'Quiz criado com perguntas e respostas.')
                return redirect('professor:quiz_detail', pk=quiz.pk)
        if not handled_error:
            messages.error(request, 'Revise os campos destacados.')
    return render(request, 'professor/quiz_form.html', _ctx(
        request,
        prof_nav='quizzes',
        title='Novo quiz',
        form=form,
        cancel_url='/professor/quizzes/',
        question_errors=question_errors,
        questions_payload_json=_questions_payload_json(questions_payload),
    ))


@professor_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz.objects.select_related('modulo', 'aula'), pk=pk)
    questions = quiz.questoes.prefetch_related('alternativas').order_by('ordem')
    attempts_queryset = quiz.tentativas.select_related('usuario').order_by('-concluido_em')
    attempts = attempts_queryset[:10]
    question_count = quiz.questoes.count()
    attempts_count = attempts_queryset.count()
    approved_attempts = attempts_queryset.filter(aprovado=True).count()
    average_points = attempts_queryset.aggregate(value=Avg('pontuacao'))['value'] or 0
    average_score = round((average_points / question_count) * 100) if question_count else 0
    return render(request, 'professor/quiz_detail.html', _ctx(
        request,
        prof_nav='quizzes',
        quiz=quiz,
        questions=questions,
        attempts=attempts,
        question_count=question_count,
        attempts_count=attempts_count,
        approved_attempts=approved_attempts,
        average_score=average_score,
    ))


@professor_required
def quiz_edit(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    form = QuizForm(request.POST or None, instance=quiz)
    questions_payload = _questions_payload_from_quiz(quiz)
    question_errors = []
    if request.method == 'POST':
        questions_payload, payload_errors = _questions_payload_from_request(request)
        normalized_questions, question_errors = _validate_quiz_questions(questions_payload)
        question_errors = payload_errors + question_errors
        handled_error = False
        if form.is_valid() and not question_errors:
            try:
                with transaction.atomic():
                    quiz = form.save()
                    quiz.questoes.all().delete()
                    _create_quiz_questions(quiz, normalized_questions)
            except IntegrityError:
                messages.error(request, 'Já existe um quiz nessa ordem. Deixe a ordem vazia para gerar automaticamente.')
                handled_error = True
            else:
                messages.success(request, 'Quiz atualizado com perguntas e respostas.')
                return redirect('professor:quiz_detail', pk=quiz.pk)
        if not handled_error:
            messages.error(request, 'Revise os campos destacados.')
    return render(request, 'professor/quiz_form.html', _ctx(
        request,
        prof_nav='quizzes',
        title='Editar quiz',
        form=form,
        cancel_url=f'/professor/quizzes/{quiz.pk}/',
        question_errors=question_errors,
        questions_payload_json=_questions_payload_json(questions_payload),
        editing=True,
    ))


@professor_required
@require_POST
def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    quiz.delete()
    messages.success(request, 'Quiz excluído com sucesso.')
    return redirect('professor:quiz_list')


def _formset_has_correct_answer(formset):
    for form in formset.forms:
        if not hasattr(form, 'cleaned_data') or form.cleaned_data.get('DELETE'):
            continue
        if form.cleaned_data.get('texto') and form.cleaned_data.get('correta'):
            return True
    return False


@professor_required
def question_create(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    question = Questao(quiz=quiz)
    form = QuestaoForm(request.POST or None, instance=question)
    formset = AlternativaFormSet(request.POST or None, instance=question)
    if request.method == 'POST':
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            formset = AlternativaFormSet(request.POST, instance=question)
            if formset.is_valid() and _formset_has_correct_answer(formset):
                formset.save()
                messages.success(request, 'Pergunta criada com sucesso.')
                return redirect('professor:quiz_detail', pk=quiz.pk)
            question.delete()
            if not _formset_has_correct_answer(formset):
                messages.error(request, 'Marque pelo menos uma resposta correta.')
            else:
                messages.error(request, 'Revise as respostas.')
        else:
            messages.error(request, 'Revise a pergunta.')
    return render(request, 'professor/question_form.html', _ctx(
        request,
        prof_nav='quizzes',
        title='Nova pergunta',
        quiz=quiz,
        form=form,
        formset=formset,
        cancel_url=f'/professor/quizzes/{quiz.pk}/',
    ))


@professor_required
def question_edit(request, pk):
    question = get_object_or_404(Questao.objects.select_related('quiz'), pk=pk)
    form = QuestaoForm(request.POST or None, instance=question)
    formset = AlternativaFormSet(request.POST or None, instance=question)
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid() and _formset_has_correct_answer(formset):
            form.save()
            formset.save()
            messages.success(request, 'Pergunta atualizada com sucesso.')
            return redirect('professor:quiz_detail', pk=question.quiz_id)
        if not _formset_has_correct_answer(formset):
            messages.error(request, 'Marque pelo menos uma resposta correta.')
        else:
            messages.error(request, 'Revise a pergunta e as respostas.')
    return render(request, 'professor/question_form.html', _ctx(
        request,
        prof_nav='quizzes',
        title='Editar pergunta',
        quiz=question.quiz,
        form=form,
        formset=formset,
        cancel_url=f'/professor/quizzes/{question.quiz_id}/',
    ))


@professor_required
@require_POST
def question_delete(request, pk):
    question = get_object_or_404(Questao.objects.select_related('quiz'), pk=pk)
    quiz_pk = question.quiz_id
    question.delete()
    messages.success(request, 'Pergunta excluída com sucesso.')
    return redirect('professor:quiz_detail', pk=quiz_pk)


@professor_required
def certificate_list(request):
    q = _query(request)
    templates = CertificateTemplate.objects.all()
    if q:
        templates = templates.filter(Q(nome__icontains=q) | Q(assinatura__icontains=q))
    page_obj = _page(request, templates.order_by('nome'))
    issued = Certificate.objects.select_related('usuario', 'modulo', 'trilha').order_by('-emitido_em')[:8]
    return render(request, 'professor/certificate_list.html', _ctx(
        request,
        prof_nav='certificates',
        page_obj=page_obj,
        issued=issued,
        q=q,
    ))


@professor_required
def certificate_template_create(request):
    form = CertificateTemplateForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            template = form.save()
            messages.success(request, 'Template criado com sucesso.')
            return redirect('professor:certificate_template_detail', pk=template.pk)
        messages.error(request, 'Revise os campos destacados.')
    return render(request, 'professor/form.html', _ctx(request, prof_nav='certificates', title='Novo certificado', form=form, cancel_url='/professor/certificados/'))


@professor_required
def certificate_template_detail(request, pk):
    template = get_object_or_404(CertificateTemplate, pk=pk)
    issue_form = CertificateIssueForm(request.POST or None)
    if request.method == 'POST':
        if issue_form.is_valid():
            cert, created = issue_certificate(
                issue_form.cleaned_data['usuario'],
                template=template,
                modulo=issue_form.cleaned_data.get('modulo'),
                trilha=issue_form.cleaned_data.get('trilha'),
            )
            messages.success(request, 'Certificado gerado com sucesso.' if created else 'Certificado já existia para essa combinação.')
            return redirect('professor:certificate_view', codigo=cert.codigo)
        messages.error(request, 'Revise os dados para gerar o certificado.')
    issued = template.certificados.select_related('usuario', 'modulo', 'trilha').order_by('-emitido_em')[:10]
    return render(request, 'professor/certificate_detail.html', _ctx(
        request,
        prof_nav='certificates',
        template=template,
        issue_form=issue_form,
        issued=issued,
    ))


@professor_required
def certificate_template_edit(request, pk):
    template = get_object_or_404(CertificateTemplate, pk=pk)
    form = CertificateTemplateForm(request.POST or None, instance=template)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Template atualizado com sucesso.')
            return redirect('professor:certificate_template_detail', pk=template.pk)
        messages.error(request, 'Revise os campos destacados.')
    return render(request, 'professor/form.html', _ctx(request, prof_nav='certificates', title='Editar certificado', form=form, cancel_url=f'/professor/certificados/{template.pk}/'))


@professor_required
@require_POST
def certificate_template_delete(request, pk):
    template = get_object_or_404(CertificateTemplate, pk=pk)
    template.delete()
    messages.success(request, 'Template excluído com sucesso.')
    return redirect('professor:certificate_list')


def certificate_view(request, codigo):
    certificate = get_object_or_404(Certificate.objects.select_related('usuario', 'modulo', 'trilha', 'template'), codigo=codigo)
    if not (request.user.is_authenticated and (is_professor(request.user) or certificate.usuario_id == request.user.id)):
        messages.error(request, 'Você não tem permissão para visualizar este certificado.')
        return redirect('/')
    return render(request, 'certificate_public.html', _ctx(
        request,
        prof_nav='certificates',
        **certificate_context(certificate),
    ))


def certificate_pdf(request, codigo):
    certificate = get_object_or_404(Certificate, codigo=codigo)
    if not (request.user.is_authenticated and (is_professor(request.user) or certificate.usuario_id == request.user.id)):
        messages.error(request, 'Você não tem permissão para baixar este certificado.')
        return redirect('/')
    response = HttpResponse(certificate_pdf_bytes(certificate), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{certificate.codigo}.pdf"'
    return response
