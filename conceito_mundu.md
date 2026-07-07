# Arquitetura da Plataforma Mundu

## Visão Geral

A Mundu é uma plataforma de aprendizagem contínua focada em desenvolvimento profissional e pessoal.

O objetivo não é apenas hospedar cursos, mas criar um ecossistema completo onde os membros possam:

* Aprender
* Praticar
* Compartilhar conhecimento
* Evoluir continuamente

A plataforma combina conceitos de:

* Udemy (cursos estruturados)
* Duolingo (gamificação e engajamento)
* Reddit (comunidade e fóruns)
* Tutor IA (acompanhamento individual)

---

# Missão

Transformar o aprendizado em uma jornada contínua, social e motivadora.

---

# Pilares da Plataforma

## Aprender

Responsável pelo consumo de conteúdo educacional.

### Recursos

* Cursos
* Módulos
* Aulas
* Certificados
* Trilhas de aprendizagem
* Histórico de progresso

---

## Evoluir

Responsável pela gamificação.

### Recursos

* XP
* Níveis
* Conquistas
* Streaks
* Metas de estudo
* Ranking
* Marcos de progresso

---

## Compartilhar

Responsável pela construção da comunidade.

### Recursos

* Fóruns
* Discussões
* Perguntas e respostas
* Compartilhamento de projetos
* Networking
* Grupos temáticos

---

## Ser Orientado

Responsável pelo acompanhamento inteligente do aprendizado.

### Recursos

* Tutor IA Salomão
* Feedback personalizado
* Correção de atividades
* Recomendações de estudo
* Acompanhamento de progresso

---

# Arquitetura Conceitual

```text
Mundu
│
├── Cursos
│
├── Gamificação
│
├── Comunidade
│
├── Salomão
│
└── Multi-Tenant
```

---

# Stack Tecnológica

## Backend

* Django
* Django REST Framework
* django-tenants

## Banco de Dados

* PostgreSQL

## Frontend

* React
* Next.js

## Infraestrutura

* Docker

## Cache e Filas

* Redis

---

# Estratégia de Vídeos

## MVP

Utilizar vídeos hospedados no YouTube.

### Formato

Vídeos Não Listados.

### Benefícios

* Sem custo de armazenamento
* Sem custo de CDN
* Escalabilidade global
* Qualidade adaptativa automática
* Upload simplificado

---

# Fluxo dos Vídeos

```text
Instrutor
↓
YouTube
↓
Vídeo Não Listado
↓
Mundu
↓
Aluno
```

---

# Evolução dos Vídeos

## Fase 2

Migração gradual para Vimeo.

### Benefícios

* Restrição por domínio
* Maior privacidade
* Player customizado
* Melhor experiência white-label

---

## Fase 3

Infraestrutura própria somente se houver necessidade financeira ou operacional.

Possíveis tecnologias:

* Bunny Stream
* Backblaze B2
* FFmpeg

---

# Estrutura Multi-Tenant

Cada cliente possui:

* Usuários próprios
* Cursos próprios
* Comunidade própria
* Certificados próprios
* Branding próprio

Exemplo:

```text
empresa1.mundu.com
empresa2.mundu.com
empresa3.mundu.com
```

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
Atividade
↓
Certificado
```

---

# Sistema de Gamificação

## XP

Toda ação relevante gera experiência.

Exemplos:

```text
Assistir aula = +20 XP

Concluir módulo = +100 XP

Responder quiz = +15 XP

Criar tópico = +10 XP

Receber curtida = +2 XP
```

---

## Níveis

Representam a evolução do membro.

```text
Nível 1
Nível 2
Nível 3
...
```

---

## Streak

Dias consecutivos de aprendizado.

Exemplos:

```text
7 dias

15 dias

30 dias

100 dias
```

---

## Conquistas

Exemplos:

```text
Primeira Aula

Primeiro Curso

Primeira Discussão

30 Dias de Streak

1000 XP

10 Certificados
```

---

# Comunidade

A comunidade é um dos pilares centrais da plataforma.

---

## Estrutura

```text
Comunidade
↓
Categorias
↓
Tópicos
↓
Comentários
```

---

## Exemplos

```text
Programação
├── Python
├── Django
└── IA

Marketing
├── Tráfego Pago
├── SEO
└── Copywriting

Negócios
├── Vendas
├── Gestão
└── Liderança
```

---

# Recursos da Comunidade

## MVP

* Criar tópicos
* Responder tópicos
* Curtir respostas
* Categorias

---

## Futuro

* Melhor resposta
* Menções
* Tags
* Moderação avançada
* IA resumindo discussões

---

# Salomão — Tutor Inteligente

## Propósito

O Salomão existe para ajudar o aluno a aprender, não para aprender por ele.

---

## Princípios

### O Salomão não deve

* Fazer trabalhos completos
* Resolver atividades integralmente
* Produzir respostas prontas para avaliações

---

## O Salomão deve

* Orientar
* Explicar
* Corrigir
* Incentivar
* Sugerir caminhos de estudo

---

# Funcionalidades do Salomão

## Correção de Textos

O aluno envia um texto.

O Salomão:

* identifica problemas
* sugere melhorias
* explica correções
* fornece feedback

Sem reescrever completamente a atividade.

---

## Feedback em Atividades

O Salomão avalia:

* clareza
* coerência
* domínio do tema
* pontos de melhoria

---

## Tutor Socrático

Ao invés de entregar respostas prontas, o Salomão estimula reflexão através de perguntas.

Exemplo:

```text
Você considerou este cenário?

Como sua solução impacta esse resultado?

Existe outra abordagem possível?
```

---

## Mentor de Estudos

O Salomão acompanha:

* progresso
* desempenho
* frequência
* interesses

E recomenda:

* cursos
* módulos
* conteúdos complementares

---

## Tutor da Comunidade

Dentro dos fóruns o Salomão pode:

* resumir discussões
* destacar conteúdos relevantes
* sugerir leituras
* conectar tópicos relacionados

---

# Roadmap

## Fase 1

MVP

* Cursos
* Módulos
* Aulas
* YouTube
* Certificados
* Multi-Tenant

---

## Fase 2

Gamificação

* XP
* Níveis
* Streak
* Conquistas

---

## Fase 3

Comunidade

* Fóruns
* Categorias
* Comentários
* Curtidas

---

## Fase 4

Salomão

* Correção de textos
* Feedback
* Recomendações
* Tutor da comunidade

---

## Fase 5

Vídeos Premium

* Vimeo
* White-label avançado
* Maior proteção de conteúdo

---

# Conclusão

A Mundu não é apenas uma plataforma de cursos.

Ela é um ecossistema de aprendizagem composto por:

* Conteúdo estruturado
* Comunidade ativa
* Gamificação
* Inteligência artificial orientadora

O objetivo é criar um ambiente onde o aprendizado seja contínuo, social e motivador.
