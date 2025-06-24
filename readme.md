# Aula: Contagem de Objetos em Imagens com OpenCV

| Máscara                | Moedas                 |
|------------------------|------------------------|
| ![Máscara](images/mask.png) | ![Moedas](images/moedas.png) |


## Descrição
Esta aula apresenta uma atividade prática de Processamento Digital de Imagens utilizando a biblioteca OpenCV em Python para contagem de objetos (moedas) em uma imagem.

O código realiza os seguintes passos principais:
1. Carregamento da imagem colorida.
2. Conversão para escala de cinza.
3. Binarização automática usando o método de Otsu.
4. Remoção de ruídos com operações morfológicas (abertura).
5. Inversão da máscara binarizada para destacar os objetos (moedas).
6. Detecção dos contornos dos objetos.
7. Filtragem dos contornos por área mínima para eliminar ruídos.
8. Desenho dos contornos na imagem original.
9. Exibição da máscara e da imagem resultante com contornos desenhados.
10. Impressão do número total de objetos detectados.

---

## Objetivos
- Entender o fluxo básico de segmentação e análise de imagens.
- Praticar técnicas de pré-processamento como binarização e operações morfológicas.
- Utilizar a função `findContours` para identificar objetos em imagens binárias.
- Aplicar filtros para considerar apenas objetos com área significativa.
- Visualizar resultados com `imshow` e manipular janelas OpenCV.

---

## Requisitos
- Python 3.x
- OpenCV (`opencv-python`)

Instalação:
```bash
pip install opencv-python
```

# Contador de Objetos com OpenCV

Este projeto utiliza Python e a biblioteca OpenCV para detectar e contar objetos em imagens. O script implementa o algoritmo Watershed para segmentar objetos, mesmo que estejam próximos ou sobrepostos.

## Funcionalidades

- **Carregamento de Imagem**: Carrega uma imagem de um caminho especificado.
- **Pré-processamento**:
    - Converte a imagem para escala de cinza.
    - Aplica desfoque gaussiano para reduzir ruído.
- **Binarização**:
    - Utiliza um método de binarização adaptativo (`THRESH_BINARY` ou `THRESH_BINARY_INV`) com `THRESH_OTSU` para encontrar o limiar ideal.
    - A lógica é ajustada para objetos claros em fundo escuro e vice-versa.
- **Limpeza da Máscara**:
    - Aplica operações morfológicas de abertura e fechamento para remover ruídos e preencher buracos na máscara binária.
- **Segmentação com Watershed**:
    - Calcula a transformada de distância para encontrar o centro dos objetos.
    - Identifica regiões de primeiro plano (`sure_fg`), plano de fundo (`sure_bg`) e desconhecidas.
    - Aplica o algoritmo Watershed para segmentar os objetos.
- **Contagem e Visualização**:
    - Itera sobre os marcadores do Watershed para identificar cada objeto.
    - Filtra os objetos por uma área mínima para ignorar ruídos.
    - Desenha contornos verdes ao redor dos objetos detectados.
    - Exibe a contagem total de objetos na imagem.
- **Salvamento**:
    - Salva a imagem resultante com os contornos e a contagem em um novo arquivo.

## Como Usar

1.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Execute o script**:
    ```bash
    python main.py
    ```
O script processará as imagens `seeds.png` e `chocolates.jpg` da pasta `images/` e salvará os resultados na mesma pasta.

## Estrutura do Código

A função principal é `contar_objetos()`, que recebe os seguintes parâmetros:

- `image_path`: Caminho da imagem de entrada.
- `save_path`: Caminho para salvar a imagem resultante.
- `min_area`: Área mínima para que um contorno seja considerado um objeto.
- `use_chocolates_logic`: Booleano que ajusta a binarização para imagens com objetos escuros em fundo claro.
- `dist_thresh`: Limiar da transformada de distância para separar objetos (valor entre 0 e 1).
