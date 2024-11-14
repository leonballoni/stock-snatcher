
# Stock Snatcher

Stock Snatcher é um projeto voltado para a captura de dados de APIs de mercado, combinando-os com scraping de dados para fornecer um serviço que recupera informações de ações, incluindo registros de compras e vendas.

## Objetivos

O projeto tem como principais objetivos:
- Capturar informações do mercado e simular cenários de compra e venda de ativos.
- Explorar técnicas eficientes de scraping e construir uma pipeline robusta para coleta de dados, com otimizações como caching e logging.

## Guia Rápido de Início

### Requisitos

#### Ferramentas Necessárias:
- [Python 3.10+](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

### Passo a Passo

1. **Inicializar via Makefile**  
   Use o Makefile para simplificar a inicialização dos serviços.

#### Para rodar em sua máquina diretamente

1. Configure o ambiente:
   ```shell
   make setup
   ```
* seguido de (que pode ser reproduzido executando o arquivo main.py na pasta src/snatcher)
  ```shell
  make run 
  ```

#### Para rodar via Docker

2. Inicie o Dockerfile (remova sufixo `-logs` para operar no modo detached):
   ```shell
   make docker-run-logs 
   ```

#### Para rodar via Docker Compose (inclui todos os serviços)

3. Inicie o Compose (remova sufixo `-logs` para operar no modo detached):
   ```shell
   make compose-run-logs
   ```

#### SWAGGER Docs
4. Podem ser acessados via rota:

> URL:PORT/docs ou URL:PORT/api/v1/docs

#### Testes

5. Execute os testes de cobertura (TO BE FINISHED - TBF):
   ```shell
   make test-coverage
   ```

> **Atenção**: Certifique-se de configurar o arquivo `.env` com base no `.env_example`.

O serviço estará disponível na porta **8000** para containers e na porta **8001** para o setup local.


## Análise do Desafio

1. Superar sistemas de segurança que limitam a ação de bots em sites é um desafio novo, mas motivador.
2. Identificamos que o Market Watch é protegido pela Datadome, uma empresa que usa algoritmos avançados, inclusive de machine learning, para bloquear bots.
3. A combinação de diversas ferramentas e o conhecimento compartilhado pela comunidade são essenciais para o desenvolvimento contínuo deste projeto.
4. Tenho explorado as ferramentas  **Selenium**, **Scrapy**, e **BeautifulSoup**, além de técnicas de proxying, para reduzir a chance de detecção.
5. Este projeto tem como objetivo aprimorar o conhecimento em ferramentas de scraping e técnicas de contorno de bloqueios.

## Estrutura do Projeto

O desenvolvimento do projeto segue a estrutura abaixo:

1. **Serviços na pasta `src/`** – núcleo das operações:
   - `snatcher`: backend da API.

[//]: # (   - `airflow`: batching diário para atualização dos dados de ações. &#40;Versão futura&#41;)

2. **Serviços na pasta `infra/`** – infraestrutura do projeto:
   - `snatcher`
   - `redis`
   - `postgresql` -> Agora operando por RDS da AWS

3. **Desenvolvido** :
   - Rotas de GET e POST Stocks
   - Contratos de entrada e saída do StockModel
   - Caching com Redis 
   - PostgresDB em AWS e Docker
   - Simples comando habilita todo o serviço
   - Logs de Auditoria

4. **Desenvolvimentos pendentes (por prioridade)** :
   - Finalizar processo de estudo e extração eficiente dos dados da Market Watch
   - Aprimorar algoritmos para contornar o sistema DataDome.
   - Integrar de forma coesa o extrator com MW e Polygon

5. **Desenvolvimento futuro** 
   - Logs de monitoramento (Paper trail, etc)
   - Acrescentar testes unitários e de integração para adequar cobertura (80%)
   - Automatizar a coleta de dados com Airflow.
   - Adicionar mais funcionalidades ao serviço de recuperação de dados.
   - Implementar relatórios visuais de Logs e Dados(Grafana ou Metabase).

## Referências

Aqui estão as documentações oficiais para cada tecnologia:

---

### FastAPI
- [FastAPI - Documentação Oficial](https://fastapi.tiangolo.com/)

### SQLAlchemy
- [SQLAlchemy - Documentação Oficial](https://www.sqlalchemy.org/)

### Selenium
- [Selenium - Documentação Oficial](https://www.selenium.dev/)

### Scrapy
- [Scrapy - Documentação Oficial](https://docs.scrapy.org/)

### BeautifulSoup
- [BeautifulSoup - Documentação Oficial](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### Pytest
- [Pytest - Documentação Oficial](https://docs.pytest.org/)

### Amazon RDS PostgreSQL
- [Amazon RDS for PostgreSQL - Documentação Oficial](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.html)

---

### [Design patterns](https://refactoring.guru/design-patterns) 

* Domain-Driven Design (DDD)
* [Ports and Adapters (Hexagonal Architecture)](https://web.archive.org/web/20140329201018/http://alistair.cockburn.us/Hexagonal+architecture)
