# base_empregos

Código para extrair dados da web bne.com.br para diversos fins. Por enquanto extrai dados do BNE. 

Utiliza o pacote Scrapy (https://scrapy.org/). É recomendável instalar num env dedicado em conda.

### Instalação

Instalar os pacotes listados em *requirements.txt*

    conda install -r requirements.txt
    
    
### Execução

A spider (ver documentação do Scrapy) pode ser usada diretamente no terminal. Para isso, vá ao diretório do projeto scrapy (empregos) e executa o seguinte comando.

    scrapy crawl bne -O output.csv
    
Esse comando vai executar a spider e escrever a saída no arquivo output.csv

Outra forma de executar o scraper é atraves do módulo *main.py*. Essa forma é mais robusta porque além do scraper já faz o tratamento dos dados de saída. Para executar ir ao diretório empregos/ e executar o seguinte comando.

    python -m main
    
Vai ser criado um arquivo de saída na pasta empregos chamado *bne.csv* com os dados já processados.

### Onde está o que?

 - O codigo do scraper está no diretório *spiders*.
 - A pipeline (para mudar o nome do arquivo de saída, por exemplo) está no diretório raiz *pipelines.py*
 - Todas as funções de tratamento do arquivo de saída estao em *postproc.py*.

