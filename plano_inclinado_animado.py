import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import matplotlib.animation as animation

def animar_plano_inclinado(m, theta_deg, mu_e, mu_c, g=9.81, salvar_gif=False):
    """
    Analisa as forças e simula visualmente (com animação) o movimento
    de um bloco em um plano inclinado.
    """
    
    # ---------------------------------------------------------
    # 1. CÁLCULOS FÍSICOS DA DINÂMICA
    # ---------------------------------------------------------
    theta = np.radians(theta_deg)
    
    P = m * g                 
    Px = P * np.sin(theta)    
    Py = P * np.cos(theta)    
    N = Py                    
    Fat_est_max = mu_e * N    
    
    if Px <= Fat_est_max:
        estado = "Repouso"
        Fat = Px              
        a = 0.0               
    else:
        estado = "Deslizando"
        Fat = mu_c * N        
        a = (Px - Fat) / m    
        
    print(f"\n--- INICIANDO SIMULAÇÃO ---")
    print(f"Estado: {estado} | Aceleração (a): {a:.2f} m/s²")
    
    # ---------------------------------------------------------
    # 2. CONFIGURAÇÃO DA FIGURA E GEOMETRIA
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    
    L = 10
    H = L * np.tan(theta)
    
    # Desenhar Rampa
    rampa = patches.Polygon([[0, 0], [L, 0], [L, H]], closed=True, color='#E0E0E0', ec='black', zorder=1)
    ax.add_patch(rampa)
    
    # Calcular posição inicial
    dist_max = L / np.cos(theta)
    dist_inicial = dist_max - 2.0  # Começa um pouco abaixo do topo
    if dist_inicial < 2.0:
        dist_inicial = dist_max / 2.0
        
    lado = 1.5
    bloco = patches.Rectangle((-lado/2, 0), lado, lado, color='#3498DB', zorder=2)
    ax.add_patch(bloco)
    
    # Arco do ângulo
    arco = patches.Arc((0, 0), 3, 3, angle=0, theta1=0, theta2=theta_deg, color='#2980B9', linewidth=2)
    ax.add_patch(arco)
    ax.text(1.8, 0.5 * np.sin(theta/2), rf'$\theta={theta_deg}^\circ$', color='#2980B9', fontsize=12, fontweight='bold')
    
    # Texto (HUD) que vai se atualizar na animação
    texto_info = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
                         
    # ---------------------------------------------------------
    # 3. PREPARAÇÃO DOS VETORES ANIMADOS
    # ---------------------------------------------------------
    # Para animar vetores de forma eficiente, usamos FancyArrowPatch e Text
    escala = 3.0 / P
    
    text_P = ax.text(0, 0, 'P', color='#E74C3C', fontweight='bold')
    text_N = ax.text(0, 0, 'N', color='#27AE60', fontweight='bold')
    text_Fat = ax.text(0, 0, 'Fat', color='#F39C12', fontweight='bold')
    text_Px = ax.text(0, 0, 'Px', color='#8E44AD', fontweight='bold')
    
    arrow_P = patches.FancyArrowPatch((0,0), (1,1), color='#E74C3C', mutation_scale=15, lw=2, zorder=3)
    arrow_N = patches.FancyArrowPatch((0,0), (1,1), color='#27AE60', mutation_scale=15, lw=2, zorder=3)
    arrow_Fat = patches.FancyArrowPatch((0,0), (1,1), color='#F39C12', mutation_scale=15, lw=2, zorder=3)
    arrow_Px = patches.FancyArrowPatch((0,0), (1,1), color='#8E44AD', mutation_scale=15, lw=1.5, linestyle='dashed', zorder=3)
    
    ax.add_patch(arrow_P)
    ax.add_patch(arrow_N)
    ax.add_patch(arrow_Fat)
    ax.add_patch(arrow_Px)
    
    ax.set_aspect('equal')
    ax.set_xlim(-1, L + 2)
    ax.set_ylim(-1, H + 3)
    ax.axis('off')
    
    plt.title(f"Simulação Dinâmica - Plano Inclinado\nEstado: {estado} | $a = {a:.2f} \, m/s^2$", fontsize=14)
    
    # ---------------------------------------------------------
    # 4. LÓGICA DE ANIMAÇÃO (A MÁGICA ACONTECE AQUI)
    # ---------------------------------------------------------
    dt = 0.05 # O tempo avança 0.05 segundos por frame (20 frames por segundo)
    
    def init():
        """Função chamada no início para limpar os objetos que serão animados"""
        texto_info.set_text('')
        return bloco, texto_info, arrow_P, arrow_N, arrow_Fat, arrow_Px, text_P, text_N, text_Fat, text_Px

    def animate(i):
        """Função chamada automaticamente a cada frame para calcular a nova posição"""
        tempo_total = i * dt
        
        # Equação horária da posição (MRUV): s(t) = s_0 + v_0*t + (1/2)*a*t^2
        if estado == "Deslizando":
            s_atual = 0.5 * a * (tempo_total ** 2)
            vel = a * tempo_total
            
            # Se chegou na base da rampa, travamos ele no final
            if s_atual >= dist_inicial:
                s_atual = dist_inicial
                vel = a * np.sqrt(2 * dist_inicial / a) # Velocidade final máxima alcançada
        else:
            s_atual = 0.0
            vel = 0.0
            
        # Transformar a distância percorrida na rampa (s_atual) em coordenadas X, Y
        # Subtraímos de dist_inicial porque ele está indo EM DIREÇÃO à origem (0,0)
        dist_neste_frame = dist_inicial - s_atual
        x_c = dist_neste_frame * np.cos(theta)
        y_c = dist_neste_frame * np.sin(theta)
        
        # 4.1 Atualizar Posição do Bloco (Translação)
        trans = transforms.Affine2D().rotate(theta).translate(x_c, y_c) + ax.transData
        bloco.set_transform(trans)
        
        # Encontrar o centro para prender a origem das setas
        x_centro = x_c - (lado/2) * np.sin(theta)
        y_centro = y_c + (lado/2) * np.cos(theta)
        
        # 4.2 Atualizar Setas (Vetores de Força)
        arrow_P.set_positions((x_centro, y_centro), (x_centro, y_centro - P * escala))
        text_P.set_position((x_centro + 0.2, y_centro - P * escala))
        
        nx = -N * escala * np.sin(theta)
        ny = N * escala * np.cos(theta)
        arrow_N.set_positions((x_centro, y_centro), (x_centro + nx, y_centro + ny))
        text_N.set_position((x_centro + nx, y_centro + ny + 0.2))
        
        fat_x = Fat * escala * np.cos(theta)
        fat_y = Fat * escala * np.sin(theta)
        arrow_Fat.set_positions((x_centro, y_centro), (x_centro + fat_x, y_centro + fat_y))
        text_Fat.set_position((x_centro + fat_x + 0.2, y_centro + fat_y + 0.2))
        
        px_x = -Px * escala * np.cos(theta)
        px_y = -Px * escala * np.sin(theta)
        arrow_Px.set_positions((x_centro, y_centro), (x_centro + px_x, y_centro + px_y))
        text_Px.set_position((x_centro + px_x - 0.5, y_centro + px_y - 0.5))
        
        # 4.3 Atualizar Painel de Informações (HUD)
        if estado == "Repouso":
            texto_info.set_text(f"ESTADO: {estado}\nTempo: {tempo_total:.1f} s\nVelocidade: 0.00 m/s")
        else:
            texto_info.set_text(f"ESTADO: {estado}\nTempo: {tempo_total:.1f} s\nDescida: {s_atual:.1f} m\nVelocidade: {vel:.1f} m/s")
            
        return bloco, texto_info, arrow_P, arrow_N, arrow_Fat, arrow_Px, text_P, text_N, text_Fat, text_Px

    # Calcular quantos frames precisamos rodar
    frames = 60 # Padrão (3 segundos) para Repouso
    if estado == "Deslizando":
        t_final = np.sqrt(2 * dist_inicial / a) # Tempo até o chão
        frames = int(t_final / dt) + 20         # Frames até o chão + 1 segundo extra parando
        
    # Inicia a animação!
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, 
                                   interval=int(dt*1000), blit=True)
    
    # ---------------------------------------------------------
    # 5. EXPORTAR GIF (OPCIONAL) OU MOSTRAR NA TELA
    # ---------------------------------------------------------
    if salvar_gif:
        print("\nGerando arquivo GIF. Por favor aguarde (isso pode levar uns segundos)...")
        # writer='pillow' é nativo e excelente para GIFs simples se a biblioteca Pillow estiver instalada
        anim.save('simulacao_rampa.gif', writer='pillow', fps=int(1/dt))
        print("✅ Arquivo 'simulacao_rampa.gif' salvo com sucesso na sua pasta do projeto!")
        
    plt.tight_layout()
    plt.show()

# ==========================================
# INTERFACE DE ENTRADA
# ==========================================
if __name__ == "__main__":
    print("="*45)
    print(" 🎬 SIMULADOR ANIMADO DE PLANO INCLINADO ")
    print("="*45)
    
    try:
        massa = 10.0 # float(input("Massa do bloco em kg (ex: 10): "))
        angulo = 10.0 # float(input("Ângulo da rampa em graus (ex: 30): "))
        mu_e = 0.4 # float(input("Coeficiente de atrito ESTÁTICO (ex: 0.4): "))
        mu_c = 0.3 # float(input("Coeficiente de atrito CINÉTICO (ex: 0.3): "))
        
        salvar_gif = 'n' # input("Deseja salvar a animação como GIF? (s/n): ").strip().lower() == 's'
        
        animar_plano_inclinado(m=massa, theta_deg=angulo, mu_e=mu_e, mu_c=mu_c, salvar_gif=salvar_gif)
    except ValueError:
        print("\n❌ ERRO: Digite apenas números com '.' para os decimais.")
