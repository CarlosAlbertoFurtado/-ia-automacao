# Agente Assistente com Function Calling

Agente de IA que **decide sozinho** quais ferramentas usar para responder suas perguntas. Ele consulta APIs em tempo real para buscar cotações e clima.

## 🎯 O que este projeto demonstra
- **Agents**: LLM no controle, decidindo quais ferramentas usar e em qual ordem.
- **Function Calling (Tool Use)**: O LLM retorna argumentos JSON para que o código execute funções locais.
- **APIs REST**: Consumo de APIs públicas gratuitas (AwesomeAPI, wttr.in).
- **LangChain Agents**: Framework que gerencia o loop de raciocínio do agente.
- **Orquestração**: O agente encadeia múltiplas chamadas de ferramentas e unifica a resposta.

## 🧠 Como o Agente funciona

```
Pergunta do Usuário
       │
       ▼
┌──────────────────┐
│   Gemini (LLM)   │  ← Analisa a pergunta e decide quais tools chamar
│   "Preciso do    │
│    dólar E clima"│
└──────┬───────────┘
       │
       ├──► Tool 1: buscar_cotacao_dolar()  → R$ 5.42
       │
       ├──► Tool 2: buscar_clima("Campinas") → 24°C, ensolarado
       │
       ▼
┌──────────────────┐
│   Gemini (LLM)   │  ← Processa os resultados e gera resposta unificada
│   "O dólar está  │
│    R$ 5.42 e em  │
│    Campinas...   │
└──────────────────┘
       │
       ▼
   Resposta Final
```

## 🛠️ Ferramentas disponíveis

| Ferramenta | API | O que faz |
|---|---|---|
| `buscar_cotacao_dolar` | AwesomeAPI | Cotação USD→BRL em tempo real |
| `buscar_clima` | wttr.in | Clima atual de qualquer cidade |
| `buscar_cotacao_moeda` | AwesomeAPI | Cotação de EUR, GBP, BTC, etc. |

**Todas as APIs são 100% gratuitas e não precisam de cadastro!**

## 🚀 Como rodar

### 1. Instale as dependências
```bash
pip install langchain langchain-google-genai httpx python-dotenv
```

### 2. Configure a chave (gratuita)
```bash
copy .env.example .env
# Edite .env com sua chave do Google AI Studio
```

### 3. Rode o agente
```bash
python agente.py
```

### 4. Teste perguntas compostas!
```
Você: Qual é o dólar hoje e como está o tempo em Campinas?

> Entering new AgentExecutor chain...
> Calling tool: buscar_cotacao_dolar
> Calling tool: buscar_clima with args: {"cidade": "Campinas"}

🤖 Resposta: Atualmente, o dólar está cotado a R$ 5,42 para compra...
   Em Campinas o clima está ensolarado com temperatura de 24°C...
```

## 📚 Conceitos-chave

### O que é um Agente?
É um LLM que tem acesso a **ferramentas** e **decide sozinho** quando e como usá-las. Diferente de um chatbot normal, o agente pode:
- Chamar APIs
- Executar código
- Encadear múltiplas ações
- Raciocinar sobre os resultados

### Function Calling
A capacidade do LLM de retornar uma "intenção de chamada de função" em formato JSON estruturado. O código então executa a função real e devolve o resultado ao LLM.

### Verbose Mode
Com `verbose=True`, você vê o "pensamento" do agente: quais tools ele decide chamar e por quê. Isso é ótimo para debug e para mostrar em entrevistas!
