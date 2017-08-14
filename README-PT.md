
# INPE IONEX TEC MAPS

## A proposta

Sabe-se que o sistema de previsão ionosférica do CRS-INPE e de muitos institutos de pesquisa tem como resultado 2 tipos de arquivos, sendo um deles um arquivo de texto (‘descriptor.txt’) contendo os dados a cerca da simulação feita, como latitute, longitude e altura utilizados na previsão, e um arquivo binário (‘data.dat’), contendo todos os dados de simulação estimados e organizados conforme o arquivo texto. 

Dessa forma, foi desenvolvido um algoritmo para interpretar esses arquivos e poder buscar os dados de acordo com a localização desejada, gerando mapas de TEC e arquivos IONEX das simulações.

## Criando mapas de TEC

Utilizando um sistema de busca que faz a varredura de todos os valores de NE e TEC correspondentes no arquivo, coordenada a coordenada, e reunir todos os valores de conteúdo eletrônico total em todos os pontos geográficos simulados, foi capaz de criar uma imagem com o resultado obtido, de acordo com a Figura XXX.

![Imgur](http://i.imgur.com/0gluZxS.png)

O algoritmo desenvolvido pode criar inúmeros mapas de TEC, desde que todos os arquivos de texto e dados, resultados da simulação do SUPIM, estejam na pasta desejada, inserida pelo usuário na execução do script. O mapa desenvolvido é geo-referenciado, e suas coordenadas correspondem fielmente aos pontos observáveis reais, aumentando a credibilidade da imagem gerada. 

Além do mapa limitado às coordenadas presentes na Figura 2, foi desenvolvida uma visualização global para os mapas de TEC, conforme Figura 2.

![Imgur](http://i.imgur.com/mTxrARE.png)

Para executar o script, basta rodá-lo no terminal, ou com alguma IDE capaz de interpretar Python. </br>
Na chamada da execução do arquivo deve ser passado por parâmetro o diretório correspondente contendo os arquivos 'descriptor' e 'data'. </br>
Abaixo fica uma imagem do script sendo executado via terminal. 

![Imgur](http://i.imgur.com/XYrkZhe.png)

## Criando arquivos IONEX

Da mesma forma que o sistema de geração de mapas TEC utiliza os arquivos ‘descriptor’ e ‘data’, esse sistema também faz a leitura desses arquivos, calcula o TEC referente aos pontos necessários, e organiza tudo em um arquivo no formato IONEX.

Baseado em um primeiro formato proposto por [Schaer, 1996], que segue o formato Receiver Independent Exchange (RINEX) [Gurtner e Madner, 1990], o formato conhecido como Ionosphere map Exchange (IONEX), que suporta a troca de informações em duas e três dimensões, foi desenvolvido a fim de ser referência quanto a mapas codificados de TEC. 

O algoritmo desenvolvido lê e interpreta os arquivos ‘descriptor’ usados durante as simulações do SUPIM, calcula o TEC referente aquelas coordenadas, busca esse valor no arquivo ‘data’ e preenche um novo arquivo, resultado do script, com os valores de TEC, seguindo o formato especificado pelo padrão IONEX. Antes do algoritmo ser executado é necessário informar o número de dimensões desejadas (2D ou 3D) e o diretório contendo os arquivos de texto e dados usados no sistema de simulação ionosférica.

Ao final, tem-se um mapa de TEC referente a data e hora da simulação, no formato IONEX, que pode ser lido em qualquer sistema capaz de interpretar esse formato. A Figura 3 mostra o trecho de um arquivo referente a um mapa IONEX 2D, enquanto a Figura 4 é o resultado para um mapa IONEX 3D.

![Imgur](http://i.imgur.com/t85NLg6.png)

![Imgur](http://i.imgur.com/lrax5Ye.png)

Na chamada da execução do arquivo deve ser passado por parâmetro o diretório correspondente contendo os arquivos 'descriptor' e 'data', bem como o número de dimensões desejados para a criação de mapas (2D ou 3D). </br>
Abaixo fica uma imagem do script sendo executado via terminal. 

![Imgur](http://i.imgur.com/6HZ1dT1.png)

## Direitos Autorais

**O projeto pode ser reproduzido sem problema algum.** </br>
Entretanto, caso isso seja feito, apenas peço para manterem/referenciarem **créditos ao autor**.


Enjoy!

**Hollweg**

