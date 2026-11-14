import os
import re
import uuid


def chave_natural(texto):
    """Ordenação 'natural', igual à do Explorer do Windows: 2 vem antes de 10.

    Quebra o texto em pedaços de letras e de números e compara os números
    como números (e não letra por letra, onde "10" ficaria antes de "2").
    """
    partes = re.split(r'(\d+)', texto)
    return [int(p) if i % 2 else p.lower() for i, p in enumerate(partes)]


def renomear_imagens():
    extensoes_imagens = ('.png', '.jpg', '.jpeg', '.webp')

    padrao = re.compile(
        r"^([123]).*?(ControlNet|Paisagem|Quadrada|Retrato|Semi-realista).*?((?:[A-Za-z0-9]+_)?\d+)\.(png|jpg|jpeg|webp)$",
        re.IGNORECASE
    )

    ordem_categoria = {
        "Retrato": 1,
        "Paisagem": 2,
        "Quadrada": 3,
        "Controlnet": 4,
        "Semi-realista": 5
    }

    arquivos_validos = []

    for arquivo in os.listdir('.'):
        if os.path.isfile(arquivo):
            match = padrao.match(arquivo)
            if match:
                estagio = int(match.group(1))
                categoria = match.group(2).capitalize()
                contador_lote = match.group(3)
                extensao = match.group(4).lower()

                arquivos_validos.append({
                    'nome_original': arquivo,
                    'estagio': estagio,
                    'categoria': categoria,
                    'contador_lote': contador_lote,
                    'extensao': extensao
                })

    if not arquivos_validos:
        print("Nenhuma imagem correspondente ao padrão foi encontrada nesta pasta.")
        return

    # Ordem final:
    # 1º categoria (todas as Retrato, depois Paisagem, etc.)
    # 2º número do lote em ordem NUMÉRICA (1, 2, 3 ... 10, 11 — e não 1, 10, 11, 2, 3)
    # 3º estágio (1 = Geração, 2 = Upscale, 3 = Olhos)
    # 4º nome do arquivo, só para desempatar (o resultado fica sempre igual,
    #    sem depender da ordem em que a pasta é lida)
    arquivos_validos.sort(key=lambda x: (
        ordem_categoria.get(x['categoria'], 99),
        chave_natural(x['contador_lote']),
        x['estagio'],
        x['nome_original'].lower()
    ))

    # PASSO 1: Renomear para nomes temporários
    for item in arquivos_validos:
        nome_antigo = item['nome_original']
        nome_temp = f"temp_seguranca_{uuid.uuid4().hex}.{item['extensao']}"
        os.rename(nome_antigo, nome_temp)
        item['nome_temp'] = nome_temp

    # PASSO 2: Renomear para a sequência final
    novo_indice = 1
    print("Resultado da renomeação:\n")

    for item in arquivos_validos:
        nome_temp = item['nome_temp']
        novo_nome_arquivo = f"{novo_indice:03d}.{item['extensao']}"

        os.rename(nome_temp, novo_nome_arquivo)

        nome_sem_extensao = item['nome_original'].rsplit('.', 1)[0]
        print(f"{nome_sem_extensao} = {novo_indice:03d}")

        novo_indice += 1

    print("\n✅ Renomeação concluída com sucesso!")


if __name__ == '__main__':
    renomear_imagens()
