import cv2
import numpy as np


def contar_objetos(image_path, save_path, min_area=100, use_chocolates_logic=False, dist_thresh=0.7):
    """
    Detecta e conta objetos em uma imagem usando o algoritmo Watershed.

    Args:
        image_path (str): Caminho para a imagem de entrada.
        save_path (str): Caminho para salvar a imagem com os resultados.
        min_area (int): Área mínima para considerar um contorno como objeto.
        use_chocolates_logic (bool): Se True, usa a lógica de binarização para
                                     imagens com objetos escuros em fundo claro
                                     (como chocolates.jpg).
        dist_thresh (float): Limiar para a transformada de distância (entre 0 e 1).
    """
    # --- 1. Carregar a Imagem ---
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro ao carregar a imagem: {image_path}")
        return

    img_copy = img.copy()  # Cópia para desenhar os resultados
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur para reduzir ruído antes da binarização
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # --- 2. Binarização ---
    # A lógica de binarização é ajustada com base no tipo de imagem.
    if use_chocolates_logic:
        # Para chocolates.jpg (objetos escuros, fundo claro)
        _, thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    else:
        # Para seeds.png (objetos claros, fundo escuro)
        _, thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # --- 3. Limpeza da Máscara (Morfologia) ---
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    # Fechamento para preencher pequenos buracos
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    # --- 4. Encontrar Fundo e Frente (para Watershed) ---
    # Usar máscara pós-fechamento para dist transform e dilatação
    sure_bg = cv2.dilate(closing, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 5)
    # Ajustar limiar com base no parâmetro da função
    _, sure_fg = cv2.threshold(dist_transform, dist_thresh * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # Encontrar região desconhecida (a "borda" dos objetos)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # --- 5. Criar Marcadores para o Watershed ---
    # Rotular os componentes conectados na área de frente
    _, markers = cv2.connectedComponents(sure_fg)

    # Adicionar 1 a todos os rótulos para que o fundo seja 1 (e não 0, que é 'desconhecido')
    markers = markers + 1

    # Marcar a região desconhecida com 0
    markers[unknown == 255] = 0
    # --- 6. Aplicar o Algoritmo Watershed ---
    # O algoritmo preencherá as regiões desconhecidas
    markers = cv2.watershed(img, markers)

    # --- 7. Contar Objetos e Desenhar Contornos (Lógica Aperfeiçoada) ---
    contagem = 0
    labels = np.unique(markers)

    for label in labels:
        if label < 2:
            continue

        # Máscara do objeto atual
        mask = np.zeros(gray.shape, dtype="uint8")
        mask[markers == label] = 255

        # Encontrar contornos no objeto
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area:
                continue
            # O filtro de circularidade foi removido para melhorar a detecção
            contagem += 1
            # Desenhar contorno do objeto
            cv2.drawContours(img_copy, [cnt], -1, (255, 255, 0), 2)

    # --- 8. Exibir e Salvar o Resultado ---
    # Atualiza texto com a contagem final na imagem
    texto = f"Objetos detectados: {contagem}"
    cv2.putText(img_copy, texto, (10, img_copy.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

    # Salvar a imagem final
    cv2.imwrite(save_path, img_copy)
    print(f"Imagem resultante salva em: {save_path}")
    print(f"Total de objetos contados: {contagem}")

    # Exibir imagens do processo para depuração
    cv2.imshow("Mascara Binarizada", thresh)
    cv2.imshow("Resultado Final", img_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # --- Processar a imagem 'seeds.png' ---
    print("Processando 'seeds.png'...")
    contar_objetos(
        image_path='images/seeds.png',
        save_path='images/seeds_resultado.png',
        min_area=100,
        use_chocolates_logic=False,
        dist_thresh=0.4  # Limiar ajustado para sementes
    )

    print("\n" + "="*50 + "\n")

    # --- Processar a imagem 'chocolates.jpg' ---
    print("Processando 'chocolates.jpg'...")
    contar_objetos(
        image_path='images/chocolates.jpg',
        save_path='images/chocolates_resultado.png',
        min_area=500,  # Chocolates são maiores, ajustar área mínima
        use_chocolates_logic=True,
        dist_thresh=0.5  # Limiar mantido para chocolates
    )
