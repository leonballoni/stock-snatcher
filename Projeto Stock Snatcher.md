# Projeto Stock Snatcher

DDL: 13/11/2024
Enviar: fabiola.rozendo@cialdnb.com, silvia.tomaz@cialdnb.com, alexsandro.valencio@cialdnb.com

## Objetivos
* Criar um Stocks REST API com PYTHON e um web framework popular (FastAPI ou outrem) 

## Requerimentos

1. README.md
* Como iniciar a app
* Revisão técnica

2. Definir e criar entidade de Stocks

3. Criar Duas rotas de operação
* **GET /stock/{stock_symbol}** 
-> Deve ser populado com dados provenientes de APIs ou Scrapping especificadosa baixo (seção de DADOS EXTERNOS)
-> Adicionar caching por GET (TLS)[https://cachetools.readthedocs.io/en/latest/] ou (Redis)[https://redis.io/] 

* **POST /stock/{stock_symbol}** -> Atualiza o montante (Amount) de tipo inteiro  (arredondar) e retornar código 201 de criação bem sucedida. Response body: “{amount} units of stock {stock_symbol} were added to your stock record”


4. Criar sistema de caching com cachetools (se não tiver tempo) ou redis (compose + classe para gerir caching)

5. API polygon
contém 
{
  "afterHours": 322.1,
  "close": 325.12,
  "from": "2023-01-09",
  "high": 326.2,
  "low": 322.3,
  "open": 324.66,
  "preMarket": 324.5,
  "status": "OK",
  "symbol": "AAPL",
  "volume": 26122646
}

* https://www.marketwatch.com/tools/markets/stocks/country/united-states
> class=table table-condensed (estrutura da tabela presente nesta class)
> <thead> contém name, exchange, sector
> <tbody> lista ordenada de value do name, exchange e sector
> class="pagination" (contém o catálogo de itens) [1-102]

* https://www.marketwatch.com/investing/stock/aapl
> class="table table--primary no-heading c2" -> conteúdo de performance
> class="element element--table overflow--table Competitors" -> Conteúdo de competidores



avaliar:
https://api.wsj.net/api/dylan/quotes/v2/comp/quoteByDialect?dialect=official&needed=CompositeTrading|BluegrassChannels&MaxInstrumentMatches=1&accept=application/json&EntitlementToken=cecc4267a0194af89ca343805a3e57af&ckey=cecc4267a0&dialects=Charting&id=UnitInvestmentTrust-BR-SANB11


## 
