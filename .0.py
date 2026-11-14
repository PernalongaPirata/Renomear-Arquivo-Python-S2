import os

def deletar_imagens_defeituosas():
    opcoes = {
        '1': 'Retrato',
        '2': 'Paisagem',
        '3': 'Quadrada',
        '4': 'ControlNet',
        '5': 'Semi-realista'
    }
    
    print("Qual formato de imagem apresenta defeito?")
    for chave, valor in opcoes.items():
        print(f"{chave} - {valor}")
        
    escolha = input("\nDigite o número da opção: ").strip()
    
    if escolha not in opcoes:
        print("Opção inválida. Operação cancelada.")
        return
        
    categoria_escolhida = opcoes[escolha].lower()
    numeros_alvo = []
    
    while True:
        numero = input(f"Digite o final (ex: 001, 004) para a categoria {opcoes[escolha]}: ").strip()
        if numero:
            numeros_alvo.append(numero)
            
        continuar = input("Deseja adicionar mais algum número para deletar? (s/n): ").strip().lower()
        if continuar != 's':
            break

    arquivos_deletados = 0
    print("\nExecutando limpeza...")
    
    extensoes = ('.png', '.jpg', '.jpeg', '.webp')
    
    for arquivo in os.listdir('.'):
        arquivo_min = arquivo.lower()
        
        # 1. Verifica se é uma imagem válida
        if not arquivo_min.endswith(extensoes):
            continue
            
        # 2. Separa o nome da extensão (para não confundir o final do lote com o formato .png)
        nome_sem_extensao, _ = os.path.splitext(arquivo_min)
        
        # 3. Lida com variações do Semi-realista (com hífen, sem hífen, tudo junto)
        categoria_presente = False
        if categoria_escolhida == 'semi-realista':
            if 'semi-realista' in nome_sem_extensao or 'semirealista' in nome_sem_extensao or 'semi realista' in nome_sem_extensao:
                categoria_presente = True
        else:
            if categoria_escolhida in nome_sem_extensao:
                categoria_presente = True

        # 4. Verifica se a categoria está no nome e se o número do lote bate
        if categoria_presente:
            for num in numeros_alvo:
                # Checa se o nome termina com o número (ex: s2_001 termina com 001)
                if nome_sem_extensao.endswith(num):
                    # Confirmação final: garante que são os estágios 1, 2 ou 3
                    if arquivo[0] in ['1', '2', '3']:
                        try:
                            os.remove(arquivo)
                            print(f"🗑️ Apagado: {arquivo}")
                            arquivos_deletados += 1
                        except Exception as e:
                            print(f"❌ Erro ao apagar {arquivo}: {e}")
                        break # Interrompe o loop para não tentar apagar o mesmo arquivo duas vezes

    if arquivos_deletados > 0:
        print(f"\n✅ Concluído! {arquivos_deletados} arquivo(s) relacionado(s) a {opcoes[escolha]} foram apagados.")
    else:
        print("\nNenhum arquivo correspondente foi encontrado para deletar. Verifique se os números digitados estão corretos.")

if __name__ == '__main__':
    deletar_imagens_defeituosas()