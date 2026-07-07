# Arquitetura da Plataforma de Vídeos White-Label

## Objetivo

Criar uma plataforma institucional de vídeos com arquitetura multi-tenant (white-label), usando Django e Cloudflare R2.

A plataforma deverá:
- suportar múltiplos clientes (tenants)
- fazer streaming eficiente de vídeos
- escalar sem reescrever a infraestrutura
- manter baixo custo no MVP

---

# Stack Escolhida

## Backend
- Django
- Django REST Framework
- django-tenants

## Banco
- PostgreSQL

## Filas
- Redis
- Celery

## Armazenamento
- Cloudflare R2

## Streaming
- HLS

## Processamento
- FFmpeg

## Frontend
- React / Next.js

## Player
- HLS.js

## Infra
- Docker

---

# Arquitetura Geral

```text
Frontend
↓
Django API
↓
PostgreSQL
↓
Cloudflare R2
↓
Cloudflare CDN
↓
Player HLS.js
```

---

# Estrutura Multi-Tenant

## Modelo recomendado

Usar:
- PostgreSQL schema-per-tenant

Biblioteca:
- django-tenants

## Exemplo

```text
empresa1.plataforma.com
empresa2.plataforma.com
```

---

# Por que schema-per-tenant?

## Vantagens

- melhor isolamento
- organização mais limpa
- branding separado
- escalabilidade boa
- facilita white-label

---

# Organização dos Vídeos

## Estrutura no R2

```text
/tenant-id/videos/video-id/
```

## Exemplo

```text
/acme/videos/abc123/
```

---

# Estrutura interna do vídeo

```text
master.m3u8
thumb.jpg

/720p/
/480p/
/360p/
```

---

# Importante

Nunca misturar vídeos de tenants diferentes.

Isso ajuda em:
- segurança
- auditoria
- billing
- exclusão
- exportação

---

# Model de Vídeo

```python
class Video(models.Model):
    tenant = models.ForeignKey(Tenant)

    title = models.CharField(max_length=255)

    original_file = models.URLField()

    hls_manifest = models.URLField()

    thumbnail = models.URLField()

    duration = models.IntegerField()

    status = models.CharField(max_length=20)
```

---

# Upload Correto dos Vídeos

## NÃO fazer

```text
Frontend
↓
Django recebe vídeo
↓
salva no servidor
```

Isso sobrecarrega o backend.

---

# Fluxo recomendado

```text
Frontend
↓
pede signed URL
↓
Django gera URL temporária
↓
Frontend envia direto pro R2
```

---

# Vantagens

- backend leve
- menos uso de CPU
- menos RAM
- menos banda
- melhor escalabilidade

---

# Pipeline de Processamento

## Fluxo completo

```text
Usuário envia vídeo
↓
R2 recebe
↓
Celery cria job
↓
Worker FFmpeg processa
↓
gera HLS
↓
gera thumbnail
↓
salva arquivos
↓
atualiza banco
```

---

# Processamento de Vídeo

## Ferramenta

FFmpeg

Usado para:
- converter formatos
- gerar HLS
- gerar thumbnails
- criar múltiplas qualidades

---

# Streaming com HLS

## O que é HLS?

HLS divide o vídeo em pequenos segmentos.

Exemplo:

```text
segment1.ts
segment2.ts
segment3.ts
```

O player baixa apenas pequenos pedaços.

---

# Vantagens do HLS

- carregamento rápido
- menos buffering
- adaptação automática da qualidade
- melhor experiência mobile

---

# Qualidades recomendadas no MVP

## Começar simples

- 720p
- 480p

Evitar inicialmente:
- 1080p
- AV1
- live streaming
- DRM

---

# Estrutura HLS

```text
master.m3u8
720p.m3u8
480p.m3u8
```

---

# Player Recomendado

## Stack

- HLS.js
- Plyr (opcional)

---

# Exemplo simples

```html
<video id="video" controls></video>

<script>
const video = document.getElementById('video');

if (Hls.isSupported()) {
  const hls = new Hls();

  hls.loadSource('/video/master.m3u8');

  hls.attachMedia(video);
}
</script>
```

---

# Workers e Filas

## Nunca processar FFmpeg no request web

Encoding consome:
- CPU
- memória
- tempo

---

# Arquitetura correta

```text
Django API
↓
Redis Queue
↓
Celery Worker
↓
FFmpeg
↓
R2
```

---

# Cloudflare R2

## Motivos da escolha

- excelente custo-benefício
- integração fácil
- ótimo para MVP
- sem custo de egress na CDN Cloudflare

---

# Vantagem importante

Em vídeo, o maior custo geralmente é:
- bandwidth
- download

Cloudflare reduz bastante esse problema.

---

# Organização dos IDs

## Não usar IDs sequenciais

Evitar:

```text
/videos/1/
```

---

# Usar UUID

```text
/videos/550e8400-e29b-41d4-a716-446655440000/
```

---

# Benefícios

- segurança
- evita enumeração
- melhor distribuição

---

# White-Label

Separar por tenant:

- branding
- logo
- CSS
- tema do player
- domínio

---

# Estrutura Recomendada de Apps Django

```text
/apps
    /accounts
    /tenants
    /videos
    /streaming
    /billing
    /analytics
```

---

# Fases do Projeto

# Fase 1 — MVP

## Implementar

- upload
- R2
- HLS
- player
- multi-tenant básico

---

# Fase 2 — Funcionalidades

## Adicionar

- progresso do vídeo
- histórico
- analytics
- quizzes
- certificados

---

# Fase 3 — Escala

## Evoluir

- autoscaling
- workers dedicados
- encoding distribuído
- filas separadas

---

# Dicas Importantes

## Guardar arquivo original

Sempre manter:
- vídeo original enviado

Mesmo após gerar HLS.

---

# Motivos

No futuro vocês podem:
- gerar novas qualidades
- trocar codec
- criar preview
- criar versão mobile
- migrar para AV1

---

# Conclusão

A stack escolhida já é uma arquitetura profissional.

Com ela é possível:
- lançar rápido
- validar o produto
- vender para empresas
- escalar sem reescrever tudo

A combinação:
- Django
- PostgreSQL
- Cloudflare R2
- FFmpeg
- HLS

é excelente para uma plataforma SaaS white-label de vídeos institucionais.