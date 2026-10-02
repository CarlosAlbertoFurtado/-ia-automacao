# 🧠 Entendendo o Código do Agente (Linha a Linha)

Se um recrutador te perguntar: *"Como exatamente você implementou o Agente com Function Calling?"*, aqui está a resposta técnica, mastigada e pronta para você brilhar.

Vamos dissecar o arquivo `agente.py` da Semana 4!

---

### 1. Preparando o Terreno (Imports)
```python
import os
import httpx
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
```
* **O que significa:** Estamos trazendo as ferramentas de terceiros para o nosso código. 
* `httpx`: Faz as requisições na internet (vai nas APIs gratuitas buscar dados reais). Usar `httpx` é mais moderno que o antigo `requests`.
* `dotenv`: Lê senhas e chaves do arquivo `.env` para não vazá-las no GitHub.
* `langchain...`: Importa os blocos de montar do LangChain (o motor do nosso cérebro artificial, que fará a IA conversar e usar ferramentas).

---

### 2. Criando uma "Ferramenta" (A Mágica do Function Calling)
```python
@tool
def buscar_clima(cidade: str) -> str:
    """
    Busca o clima atual de uma cidade.
    Use esta ferramenta quando o usuário perguntar sobre tempo, clima ou temperatura.
    
    Args:
        cidade: Nome da cidade (ex: 'Campinas')
    """
```
* **O que significa:** O `@tool` acima da função é um decorador (um "feitiço") do LangChain. Ele pega essa função Python comum e a transforma em um Schema JSON que o Gemini entende nativamente.
* **A Docstring (texto verde/vermelho):** Isso NÃO é apenas comentário! É a **instrução direta para a IA**. O Gemini lê isso para decidir **quando** deve usar essa função. Sem isso, a IA fica "cega" e não sabe para que a ferramenta serve.

```python
    try:
        response = httpx.get(f"https://wttr.in/{cidade}?format=j1", timeout=10)
        data = response.json()
        # ... lógica de extração ...
        return f"🌤️ Clima em {nome_cidade}: {current['temp_C']}°C..."
```
* **O que significa:** Se a IA decidir usar essa ferramenta, o Python entra em ação. Ele bate na API pública do `wttr.in`, extrai a temperatura e devolve uma string formatada de volta para o "cérebro" da IA. O `try/except` evita que o Agente crashe se a API do clima sair do ar.

---

### 3. Configurando o Cérebro (O LLM)
```python
def criar_agente():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
    )
```
* **O que significa:** Aqui instanciamos o Gemini. 
* Escolhemos o modelo `flash` porque ele é absurdamente rápido, moderno e gratuito no Google AI Studio.
* Colocamos `temperature=0.3` (perto de zero) porque queremos respostas **precisas** e lógicas baseadas estritamente nas ferramentas, e não queremos que a IA fique inventando dados (alucinação).

---

### 4. Dando as Regras de Negócio (System Prompt)
```python
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente... SEMPRE use as ferramentas... Não invente dados!"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
```
* **O que significa:** Estamos moldando a mente do Agente, dando a ele seu propósito.
* `"system"`: É a diretriz máxima. Mandamos ele nunca inventar dados.
* `"human"`: É o local onde a pergunta digitada pelo usuário vai ser injetada.
* `"agent_scratchpad"`: **Isso é crucial.** É o "bloco de rascunho" da IA. É aqui que ela guarda os resultados das ferramentas temporariamente antes de te dar a resposta final. (Ex: "Fui na tool 1, o clima é 24ºC... fui na tool 2, o dólar é R$5... agora vou escrever a resposta final juntando tudo").

---

### 5. Juntando as Peças e Criando o Executor (O Loop do Agente)
```python
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5
    )
    return executor
```
* **O que significa:** Aqui a orquestração acontece.
* `create_tool_calling_agent`: "Amarra" a IA (Gemini), as Ferramentas (Dólar, Clima) e o Prompt (Instruções) em um objeto só.
* `AgentExecutor`: É o "gerente de projetos". Ele fica num loop (*"A IA pediu pra usar a tool? Sim, então eu executo a tool no Python. A API devolveu o dado? Sim. Devolvo pra IA ler"*).
* `verbose=True`: Faz imprimir no terminal aquela "tela cheia de logs" mostrando o pensamento passo-a-passo do Agente. É brilhante para impressionar em entrevistas de emprego, pois mostra o motor funcionando.
* `max_iterations=5`: Um botão de segurança. Se a IA ficar confusa (ex: tentar usar a ferramenta de dólar 100 vezes sem parar), o executor corta a energia na 5ª tentativa para não travar seu PC e nem estourar limite de API.

---

### 6. A Execução
```python
        resultado = agente.invoke({"input": pergunta})
        print(f"🤖 Resposta: {resultado['output']}")
```
* **O que significa:** Você aperta o "Play". O método `invoke` despacha sua pergunta, o Agente pensa, decide que ferramentas precisa, espera o retorno do Python, compõe o texto de forma humanizada e elegante, e o código exibe na tela o `output` final!

---

### 💡 Por que este código brilha no GitHub?
O código do `agente.py` já foi construído de forma **extremamente profissional**. 
Ele usa `httpx` (biblioteca moderna e assíncrona, muito cobrada em vagas Python modernas), possui forte tratamento de erros (`try/except`), faz a validação de segurança para as chaves no topo do arquivo com `os.environ` e a documentação interna (as docstrings) está impecável e otimizada para o LLM.

Este arquivo `COMO_FUNCIONA.md` é a cereja do bolo. Leia, entenda, suba para o GitHub e deixe lá para que a Ana da Moot (e os engenheiros técnicos dela) vejam a profundidade do seu entendimento do ecossistema de Automação com IA!
