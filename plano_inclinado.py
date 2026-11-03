import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms

def analisar_plano_inclinado(m, theta_deg, mu_e, mu_c, g=9.81):
    """
    Analisa as forças e o movimento de um bloco em um plano inclinado
    e gera um diagrama vetorial.
    """
    
    # 1. CONVERSÃO E CÁLCULOS FÍSICOS
    # O math/numpy usa radianos, então converti para ângulo
    theta = np.radians(theta_deg)
    
    # Força Peso total (P = m * g)
    P = m * g                 
    
    # Decomposição do Peso
    # Px puxa o bloco para baixo na rampa (paralelo ao plano)
    Px = P * np.sin(theta)    
    # Py empurra o bloco contra a rampa (perpendicular ao plano)
    Py = P * np.cos(theta)    
    
    # Força Normal
    # A superfície reage à componente Py. N e Py se anulam (equilíbrio no eixo y)
    N = Py                    
    
    # Força de Atrito Estático Máxima
    # É o limite máximo antes do bloco começar a escorregar
    Fat_est_max = mu_e * N    
    
    # 2. LÓGICA DE MOVIMENTO
    # Comparamos a força que tenta mover o bloco (Px) com o limite de atrito (Fat_est_max)
    if Px <= Fat_est_max:
        # Se Px não supera o limite, o bloco não se move
        estado = "Repouso"
        Fat = Px              # O atrito atua apenas com a força necessária para segurar o bloco
        a = 0.0               # Sem aceleração
    else:
        # Se Px supera o limite, o bloco escorrega!
        estado = "Deslizando"
        Fat = mu_c * N        # Agora o atrito que atua é o cinético (dinâmico)
        a = (Px - Fat) / m    # 2ª Lei de Newton: Força Resultante = m * a -> a = F_res / m
        
    # --- EXIBIÇÃO DOS RESULTADOS NO CONSOLE ---
    print("="*40)
    print("--- RESULTADOS DA ANÁLISE ---")
    print(f"Estado do bloco: {estado}")
    print(f"Aceleração (a): {a:.2f} m/s²")
    print(f"Força Peso (P): {P:.2f} N")
    print(f"  ↳ Componente Px: {Px:.2f} N")
    print(f"  ↳ Componente Py: {Py:.2f} N")
    print(f"Força Normal (N): {N:.2f} N")
    print(f"Atrito Estático Máx: {Fat_est_max:.2f} N")
    print(f"Atrito Atuante (Fat): {Fat:.2f} N")
    print("="*40)
    
    # 3. VISUALIZAÇÃO GRÁFICA (MATPLOTLIB)
    # Criamos a figura (janela) e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Geometria da rampa
    L = 10  # Comprimento da base da rampa
    H = L * np.tan(theta) # Altura baseada no ângulo (trigonometria básica)
    
    # Desenhar o triângulo (rampa) usando polígono
    # Vértices: (0,0) onde fica o ângulo, (L,0) canto inferior direito, (L,H) topo
    rampa = patches.Polygon([[0, 0], [L, 0], [L, H]], closed=True, color='#E0E0E0', ec='black', zorder=1)
    ax.add_patch(rampa)
    
    # Posição do bloco na rampa
    # Calculamos para ele ficar no meio da hipotenusa
    dist_bloco = L / (2 * np.cos(theta)) 
    x_c = dist_bloco * np.cos(theta)
    y_c = dist_bloco * np.sin(theta)
    
    # Desenhar o bloco
    lado = 1.5
    # Criamos o bloco na origem e depois rotacionamos e transladamos
    bloco = patches.Rectangle((-lado/2, 0), lado, lado, color='#3498DB', zorder=2)
    # Aplicando a transformação (rotação pelo ângulo theta, depois move para x_c, y_c)
    trans = transforms.Affine2D().rotate(theta).translate(x_c, y_c) + ax.transData
    bloco.set_transform(trans)
    ax.add_patch(bloco)
    
    # Desenhar o arco mostrando o ângulo theta
    arco = patches.Arc((0, 0), 3, 3, angle=0, theta1=0, theta2=theta_deg, color='#2980B9', linewidth=2)
    ax.add_patch(arco)
    ax.text(1.8, 0.5 * np.sin(theta/2), rf'$\theta={theta_deg}^\circ$', color='#2980B9', fontsize=12, fontweight='bold')
    
    # --- DESENHAR VETORES (FORÇAS) ---
    # Encontrar o centro geométrico do bloco para ser a origem das setas
    x_centro = x_c - (lado/2) * np.sin(theta)
    y_centro = y_c + (lado/2) * np.cos(theta)
    
    # Um fator de escala visual para as setas não ficarem gigantes na tela
    escala = 3.0 / P
    
    # 1. Força Peso (P) - Sempre vertical para baixo (0, -y)
    ax.annotate('', xy=(x_centro, y_centro - P * escala), xytext=(x_centro, y_centro),
                arrowprops=dict(arrowstyle="->", color='#E74C3C', lw=2), zorder=3)
    ax.text(x_centro + 0.2, y_centro - P * escala, 'P', color='#E74C3C', fontsize=12, fontweight='bold')
    
    # 2. Força Normal (N) - Perpendicular à rampa (90 graus)
    nx = -N * escala * np.sin(theta)
    ny = N * escala * np.cos(theta)
    ax.annotate('', xy=(x_centro + nx, y_centro + ny), xytext=(x_centro, y_centro),
                arrowprops=dict(arrowstyle="->", color='#27AE60', lw=2), zorder=3)
    ax.text(x_centro + nx, y_centro + ny + 0.2, 'N', color='#27AE60', fontsize=12, fontweight='bold')
    
    # 3. Força de Atrito (Fat) - Paralela à rampa, contra o movimento (para cima)
    fat_x = Fat * escala * np.cos(theta)
    fat_y = Fat * escala * np.sin(theta)
    ax.annotate('', xy=(x_centro + fat_x, y_centro + fat_y), xytext=(x_centro, y_centro),
                arrowprops=dict(arrowstyle="->", color='#F39C12', lw=2), zorder=3)
    ax.text(x_centro + fat_x + 0.2, y_centro + fat_y + 0.2, 'Fat', color='#F39C12', fontsize=12, fontweight='bold')
    
    # 4. Componente Px - Paralela à rampa, a favor do movimento (para baixo)
    px_x = -Px * escala * np.cos(theta)
    px_y = -Px * escala * np.sin(theta)
    ax.annotate('', xy=(x_centro + px_x, y_centro + px_y), xytext=(x_centro, y_centro),
                arrowprops=dict(arrowstyle="->", color='#8E44AD', lw=1.5, ls='dashed'), zorder=3)
    ax.text(x_centro + px_x - 0.5, y_centro + px_y - 0.5, 'Px', color='#8E44AD', fontsize=12, fontweight='bold')
    
    # Configurações finais de exibição
    ax.set_aspect('equal') # Mantém proporção de X e Y reais
    ax.set_xlim(-1, L + 2)
    ax.set_ylim(-1, H + 3)
    ax.axis('off') # Remove o grid numérico, deixando apenas o desenho
    
    # Título do gráfico
    plt.title(f"Diagrama de Forças - Plano Inclinado\nEstado: {estado} | $a = {a:.2f} \, m/s^2$", fontsize=14, pad=20)
    
    # Exibir a janela interativa!
    plt.tight_layout()
    plt.show()

# ==========================================
# ENTRADA DE DADOS INTERATIVA
# ==========================================
if __name__ == "__main__":
    print("="*45)
    print(" 🎢 SIMULADOR DE PLANO INCLINADO COM ATRITO ")
    print("="*45)
    
    try:
        # Solicitando dados ao usuário pelo terminal
        massa = float(input("Digite a massa do bloco em kg (ex: 10): "))
        angulo = float(input("Digite o ângulo de inclinação em graus (ex: 30): "))
        mu_e = float(input("Digite o coeficiente de atrito ESTÁTICO (ex: 0.4): "))
        mu_c = float(input("Digite o coeficiente de atrito CINÉTICO (ex: 0.3): "))
        
        # Adicionando a gravidade como opcional
        g_str = input("Digite a gravidade (ou aperte Enter para usar 9.81 m/s²): ")
        gravidade = float(g_str) if g_str.strip() else 9.81
        
        print("\nProcessando cálculos e gerando o diagrama gráfico...\n")
        
        # Chamar a função principal com as respostas do usuário
        analisar_plano_inclinado(m=massa, 
                                 theta_deg=angulo, 
                                 mu_e=mu_e, 
                                 mu_c=mu_c,
                                 g=gravidade)
                                 
    except ValueError:
        # Caso o usuário digite texto ou vírgula no lugar de ponto
        print("\n❌ ERRO: Por favor, digite apenas números! Lembre-se de usar ponto '.' para decimais (ex: 0.5 ao invés de 0,5).")

