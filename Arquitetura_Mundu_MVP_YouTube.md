# Arquitetura da Plataforma Mundu (MVP + Evolução)

## Objetivo

Criar uma plataforma de ensino white-label (multi-tenant) focada em cursos, treinamentos e capacitações online.

A plataforma deverá:

- suportar múltiplos clientes (tenants)
- permitir publicação rápida de cursos
- manter baixo custo operacional
- validar o produto antes de investir em infraestrutura de vídeo
- evoluir gradualmente para soluções mais robustas

---

# Filosofia do MVP

O objetivo da primeira versão não é construir uma infraestrutura de streaming.

O objetivo é validar:

- venda de cursos
- experiência do aluno
- retenção
- progresso das aulas
- certificação
- multi-tenant
- gestão de conteúdo

O YouTube absorve toda a complexidade de vídeo enquanto a equipe foca no produto.

---

# Stack Escolhida

## Backend

- Django
- Django REST Framework
- django-tenants

## Banco

- PostgreSQL

## Frontend

- React / Next.js

## Infra

- Docker

## Vídeos (MVP)

- YouTube (Não Listado)

---

# Arquitetura Geral

```text
Frontend
↓
Django API
↓
PostgreSQL
↓
YouTube (Não Listado)
↓
Aluno
```

---

# Estrutura Multi-Tenant

## Modelo recomendado

Schema por tenant utilizando:

- django-tenants

## Exemplo

```text
empresa1.mundu.com
empresa2.mundu.com
empresa3.mundu.com
```

## Benefícios

- isolamento dos dados
- branding individual
- escalabilidade
- white-label simplificado

---

# Estrutura Acadêmica

```text
Tenant
↓
Curso
↓
Módulo
↓
Aula
↓
Progresso
↓
Certificado
```

---

# Organização dos Cursos

## Curso

```python
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.URLField()
``

## Módulo

```python
class Module(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=255)
    order = models.IntegerField()
``

## Aula

```python
class Lesson(models.Model):
    module = models.ForeignKey(Module)

    title = models.CharField(max_length=255)

    youtube_video_id = models.CharField(max_length=50)

    duration = models.IntegerField()

    order = models.IntegerField()

    is_preview = models.BooleanField(default=False)
``

---

# Integração com YouTube

## Fluxo

```text
Instrutor
↓
Upload no YouTube
↓
Vídeo Não Listado
↓
Cadastro na Plataforma
↓
Aluno
```

## Como funciona

O instrutor publica o vídeo como:

```text
Não Listado
```

O vídeo não aparece em pesquisas públicas, mas pode ser exibido dentro da plataforma utilizando embed.

---

# Player de Vídeo

## Arquitetura

```text
Frontend
↓
YouTube Iframe API
↓
Vídeo Não Listado
```

## Benefícios

- custo zero de armazenamento
- custo zero de CDN
- escalabilidade global
- múltiplas resoluções automáticas
- transcodificação automática

---

# Controle de Progresso

Mesmo utilizando vídeos do YouTube, a plataforma continua responsável por:

- progresso do aluno
- conclusão da aula
- bloqueio de módulos
- emissão de certificados
- métricas de aprendizado

Através da YouTube Player API é possível obter:

```javascript
player.getCurrentTime()
player.getDuration()
```

---

# Área Administrativa

Cada tenant poderá gerenciar:

- cursos
- módulos
- aulas
- certificados
- usuários
- branding

---

# White-Label

Cada cliente poderá possuir:

- logo própria
- cores próprias
- domínio próprio
- certificados personalizados

---

# Estrutura Recomendada de Apps Django

```text
/apps
    /accounts
    /tenants
    /courses
    /lessons
    /certificates
    /analytics
    /billing
```

---

# Roadmap

# Fase 1 — MVP

## Objetivo

Validar o produto rapidamente.

## Implementar

- Login
- Multi-tenant básico
- Cursos
- Módulos
- Aulas
- Player YouTube
- Controle de progresso
- Certificados

---

# Fase 2 — Crescimento

## Adicionar

- Analytics
- Quizzes
- Gamificação
- Comentários
- Comunidade
- Trilhas de aprendizagem

---

# Fase 3 — Vimeo

## Objetivo

Aumentar privacidade e profissionalização da plataforma.

### Benefícios

- Restrição por domínio
- Vídeos privados
- Player customizado
- White-label avançado
- Menor risco de compartilhamento externo

## Arquitetura

```text
Frontend
↓
Django API
↓
PostgreSQL
↓
Vimeo
↓
Aluno
```

---

# Fase 4 — Infraestrutura Própria

Executar apenas quando houver necessidade comprovada.

## Possíveis tecnologias

- Bunny Stream
- Backblaze B2
- FFmpeg
- CDN própria

## Objetivos

- controle total do conteúdo
- redução de dependência externa
- personalização avançada
- otimização de custos em larga escala

---

# Dicas Importantes

## Não investir cedo em infraestrutura de vídeo

A infraestrutura de vídeo não é o diferencial da plataforma.

O diferencial está em:

- experiência do aluno
- conteúdo
- certificação
- gestão de cursos
- experiência white-label

---

# Conclusão

A estratégia recomendada é:

Fase 1:
- YouTube Não Listado

Fase 2:
- Crescimento do produto

Fase 3:
- Vimeo

Fase 4:
- Infraestrutura própria (somente se necessário)

Essa abordagem reduz custos, acelera o lançamento do MVP e permite que a equipe concentre esforços no que realmente gera valor para os clientes.
