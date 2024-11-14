
# Stock Snatcher

Stock Snatcher é um projeto voltado para a captura de dados de APIs de mercado, combinando-os com scraping de dados para fornecer um serviço que recupera informações de ações, incluindo registros de compras e vendas.

## Objetivos

O projeto tem como principais objetivos:
- Capturar informações do mercado e simular cenários de compra e venda de ativos.
- Explorar técnicas eficientes de scraping e construir uma pipeline robusta para coleta de dados, com otimizações como caching e logging.

## Análise do Desafio

1. Superar sistemas de segurança que limitam a ação de bots em sites é um desafio novo, mas motivador.
2. Identificamos que o Market Watch é protegido pela Datadome, uma empresa que usa algoritmos avançados, inclusive de machine learning, para bloquear bots.
3. A combinação de diversas ferramentas e o conhecimento compartilhado pela comunidade são essenciais para o desenvolvimento contínuo deste projeto.
4. Estamos explorando ferramentas como **Selenium**, **Scrapy**, e **BeautifulSoup**, além de técnicas de proxying, para reduzir a chance de detecção.
5. Este projeto tem como objetivo aprimorar o conhecimento em ferramentas de scraping e técnicas de contorno de bloqueios.

## Estrutura do Projeto

O desenvolvimento do projeto segue a estrutura abaixo:

1. **Serviços na pasta `src/`** – núcleo das operações:
   - `snatcher`: backend da API.
   - `airflow`: batching diário para atualização dos dados de ações. (Versão futura)

2. **Serviços na pasta `infra/`** – infraestrutura do projeto:
   - `snatcher`
   - `redis`
   - `postgresql`

3. **Desenvolvimentos Futuros**:
   - Automatizar a coleta de dados com Airflow.
   - Adicionar mais funcionalidades ao serviço de recuperação de dados.
   - Implementar relatórios visuais (Grafana ou Metabase).
   - Aprimorar algoritmos para contornar o sistema DataDome.

## Guia Rápido de Início

### Requisitos

#### Ferramentas Necessárias:
- [Python 3.10+](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

### Passo a Passo

1. **Inicializar via Makefile**  
   Use o Makefile para simplificar a inicialização dos serviços.

#### Para rodar localmente no código

1. Configure o ambiente:
   ```shell
   make setup
   ```

#### Para rodar via Docker

2. Inicie o Dockerfile (adicione `-logs` para exibir logs no terminal):
   ```shell
   make docker-run-logs 
   ```

#### Para rodar via Docker Compose (inclui todos os serviços)

3. Inicie o Compose (adicione `-logs` para exibir logs no terminal):
   ```shell
   make compose-run-logs
   ```

#### Testes

4. Execute os testes de cobertura (TO BE FINISHED - TBF):
   ```shell
   make test-coverage
   ```

> **Atenção**: Certifique-se de configurar o arquivo `.env` com base no `.env_example`.

O serviço estará disponível na porta **8000** para containers e na porta **8001** para o setup local.

## TODO

Futuras melhorias e implementações para explorar a escalabilidade do projeto:

- Implementar paginação e filtragem dinâmica.
- Desenvolver uma pipeline de extração automatizada com Airflow e definir periodicidade ideal.
- Migrar serviços para um cluster Kubernetes (K8S).
- Adicionar logs de monitoramento (e de auditoria) – PaperTrail.



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
