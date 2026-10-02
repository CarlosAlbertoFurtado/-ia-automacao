"""
Semana 4 — Agente Assistente com Function Calling (Tools)

Este agente usa o Gemini para decidir SOZINHO quais ferramentas usar
para responder a pergunta do usuário. Ele possui 3 ferramentas:

1. buscar_cotacao_dolar() — Consulta a cotação do Dólar em tempo real (API gratuita)
2. buscar_clima()         — Consulta o clima atual de uma cidade (API gratuita)
3. buscar_noticias()      — Busca as notícias mais recentes sobre um tema

O LLM analisa a pergunta, decide quais tools chamar, processa os resultados
e gera uma resposta unificada.

Stack: Python, LangChain Agents, APIs públicas gratuitas, Gemini
"""
import os
import httpx
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
load_dotenv()
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

@tool
def buscar_cotacao_dolar() -> str:
    """
    Busca a cotação atual do Dólar (USD) em relação ao Real (BRL).
    Use esta ferramenta quando o usuário perguntar sobre dólar, câmbio ou cotação.
    Retorna: cotação de compra, venda e variação do dia.
    """
    try:
        response = httpx.get('https://economia.awesomeapi.com.br/json/last/USD-BRL', timeout=10)
        data = response.json()['USDBRL']
        return f'💵 Cotação do Dólar (USD → BRL):\n  • Compra: R$ {float(data['bid']):.2f}\n  • Venda: R$ {float(data['ask']):.2f}\n  • Variação: {data['pctChange']}%\n  • Máxima do dia: R$ {float(data['high']):.2f}\n  • Mínima do dia: R$ {float(data['low']):.2f}\n  • Atualizado em: {data['create_date']}'
    except Exception as e:
        return f'Erro ao buscar cotação: {e}'

@tool
def buscar_clima(cidade: str) -> str:
    """
    Busca o clima atual de uma cidade.
    Use esta ferramenta quando o usuário perguntar sobre tempo, clima ou temperatura.
    
    Args:
        cidade: Nome da cidade (ex: 'Campinas', 'São Paulo', 'Rio de Janeiro')
    
    Retorna: temperatura, condição, umidade e vento.
    """
    try:
        response = httpx.get(f'https://wttr.in/{cidade}?format=j1', timeout=10, headers={'Accept-Language': 'pt-BR'})
        data = response.json()
        current = data['current_condition'][0]
        area = data['nearest_area'][0]
        nome_cidade = area['areaName'][0]['value']
        regiao = area['region'][0]['value']
        desc = current.get('lang_pt', [{}])
        descricao = desc[0].get('value', current['weatherDesc'][0]['value']) if desc else current['weatherDesc'][0]['value']
        return f'🌤️ Clima em {nome_cidade}, {regiao}:\n  • Condição: {descricao}\n  • Temperatura: {current['temp_C']}°C (sensação: {current['FeelsLikeC']}°C)\n  • Umidade: {current['humidity']}%\n  • Vento: {current['windspeedKmph']} km/h ({current['winddir16Point']})\n  • Visibilidade: {current['visibility']} km\n  • UV: {current['uvIndex']}'
    except Exception as e:
        return f"Erro ao buscar clima para '{cidade}': {e}"

@tool
def buscar_cotacao_moeda(moeda: str) -> str:
    """
    Busca a cotação atual de uma moeda em relação ao Real (BRL).
    Use quando o usuário perguntar sobre Euro, Libra, Bitcoin ou outra moeda.
    
    Args:
        moeda: Código da moeda (ex: 'EUR' para Euro, 'GBP' para Libra, 'BTC' para Bitcoin)
    
    Retorna: cotação de compra e venda.
    """
    try:
        response = httpx.get(f'https://economia.awesomeapi.com.br/json/last/{moeda}-BRL', timeout=10)
        data = response.json()
        key = f'{moeda}BRL'
        info = data[key]
        return f'💱 Cotação {info['name']}:\n  • Compra: R$ {float(info['bid']):.2f}\n  • Venda: R$ {float(info['ask']):.2f}\n  • Variação: {info['pctChange']}%\n  • Atualizado em: {info['create_date']}'
    except Exception as e:
        return f'Erro ao buscar cotação de {moeda}: {e}'

def criar_agente():
    """Cria e configura o agente com suas ferramentas."""
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', google_api_key=GEMINI_API_KEY, temperature=0.3)
    tools = [buscar_cotacao_dolar, buscar_clima, buscar_cotacao_moeda]
    prompt = ChatPromptTemplate.from_messages([('system', 'Você é um assistente inteligente e prestativo que responde em português brasileiro. Você tem acesso a ferramentas para buscar informações em tempo real. SEMPRE use as ferramentas disponíveis quando a pergunta envolver dados atuais (cotações, clima, etc.). Não invente dados — use as ferramentas!\nAo responder, organize a informação de forma clara e amigável.'), ('human', '{input}'), MessagesPlaceholder('agent_scratchpad')])
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=5)
    return executor

def chat_com_agente():
    """Loop interativo com o agente."""
    print('=' * 60)
    print('🤖 AGENTE ASSISTENTE — Dólar, Clima & Moedas')
    print('=' * 60)
    print('\nPergunte qualquer coisa! Exemplos:')
    print("  • 'Qual é o dólar hoje e como está o tempo em Campinas?'")
    print("  • 'Quanto vale o Euro e o Bitcoin agora?'")
    print("  • 'Como está o clima em São Paulo?'")
    print("\nDigite 'sair' para encerrar.\n")
    print('-' * 60)
    agente = criar_agente()
    while True:
        pergunta = input('\nVocê: ').strip()
        if not pergunta:
            continue
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            print('\n👋 Até mais!')
            break
        print()
        try:
            resultado = agente.invoke({'input': pergunta})
            print(f'\n🤖 Resposta: {resultado['output']}')
        except Exception as e:
            print(f'\n❌ Erro: {e}')
        print('\n' + '-' * 60)
if __name__ == '__main__':
    if not GEMINI_API_KEY:
        print('❌ GEMINI_API_KEY não encontrada!')
        print('   Crie um arquivo .env com: GEMINI_API_KEY=sua_chave_aqui')
        print('   Pegue gratuitamente em: https://aistudio.google.com/apikey')
        exit(1)
    chat_com_agente()