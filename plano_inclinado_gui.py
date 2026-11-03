import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
import matplotlib.transforms as transforms

class SimuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Interativo 2D - Plano Inclinado")
        self.root.geometry("1150x700")  # Tamanho inicial da janela
        
        # Variáveis de Controle da Animação
        self.is_animating = False # Diz se a simulação está rodando (True) ou pausada (False)
        self.t_atual = 0.0        # Cronômetro da simulação (em segundos)
        self.s_atual = 0.0        # Distância percorrida pelo bloco na rampa
        self.dt = 0.04            # "Delta t": o tempo avança 0.04s por frame (~25 quadros por segundo)
        
        # O construtor chama as funções que montam a interface visual e o gráfico matemático
        self.construir_interface()
        self.setup_grafico()
        
        # Executa o cálculo inicial para a rampa e o bloco aparecerem na posição e ângulo corretos
        self.atualizar_fisica()
        
        # Inicia o motor da animação em background (fica rodando invisível desde o início do app)
        self.loop_animacao()
        
    def construir_interface(self):
        """Constrói os painéis, botões e caixas da janela do Tkinter"""
        # Frame Principal: divide a tela em duas partes (Painel de Controle e Simulador Visual)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # PAINEL LATERAL ESQUERDO (Controles)
        self.painel_esq = tk.Frame(self.main_frame, width=320, bg="#F7F9F9", padx=15, pady=10, relief=tk.RAISED, bd=2)
        self.painel_esq.pack(side=tk.LEFT, fill=tk.Y)
        
        titulo = tk.Label(self.painel_esq, text="⚙️ PARÂMETROS", font=("Segoe UI", 14, "bold"), bg="#F7F9F9")
        titulo.pack(pady=(0, 10))
        
        # --- SLIDERS (Barras Deslizantes) ---
        # O parâmetro 'command=self.ao_mudar_slider' avisa o programa toda vez que o mouse arrastar o botão
        
        tk.Label(self.painel_esq, text="Ângulo do Plano (graus):", bg="#F7F9F9", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        self.scale_angulo = tk.Scale(self.painel_esq, from_=0, to=80, orient=tk.HORIZONTAL, bg="#F7F9F9", command=self.ao_mudar_slider)
        self.scale_angulo.set(30) # Valor inicial padrão (30 graus)
        self.scale_angulo.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(self.painel_esq, text="Massa do Bloco (kg):", bg="#F7F9F9", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        self.scale_massa = tk.Scale(self.painel_esq, from_=1, to=50, orient=tk.HORIZONTAL, bg="#F7F9F9", command=self.ao_mudar_slider)
        self.scale_massa.set(10)
        self.scale_massa.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(self.painel_esq, text="Coef. Atrito Estático (μe):", bg="#F7F9F9", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        self.scale_mue = tk.Scale(self.painel_esq, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, bg="#F7F9F9", command=self.ao_mudar_slider)
        self.scale_mue.set(0.4)
        self.scale_mue.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(self.painel_esq, text="Coef. Atrito Cinético (μc):", bg="#F7F9F9", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        self.scale_muc = tk.Scale(self.painel_esq, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, bg="#F7F9F9", command=self.ao_mudar_slider)
        self.scale_muc.set(0.3)
        self.scale_muc.pack(fill=tk.X, pady=(0, 10))
        
        # --- BOTÕES DE CONTROLE DA ANIMAÇÃO ---
        frame_botoes = tk.Frame(self.painel_esq, bg="#F7F9F9")
        frame_botoes.pack(fill=tk.X, pady=5)
        
        btn_iniciar = tk.Button(frame_botoes, text="▶ Iniciar", bg="#2ECC71", fg="white", font=("Segoe UI", 10, "bold"), command=self.iniciar)
        btn_iniciar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        btn_pausar = tk.Button(frame_botoes, text="⏸ Pausar", bg="#F39C12", fg="white", font=("Segoe UI", 10, "bold"), command=self.pausar)
        btn_pausar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        btn_resetar = tk.Button(frame_botoes, text="🔄 Reset", bg="#E74C3C", fg="white", font=("Segoe UI", 10, "bold"), command=self.resetar)
        btn_resetar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        # --- PAINEL DE RESULTADOS DA FÍSICA EM TEMPO REAL ---
        tk.Label(self.painel_esq, text="📊 RESULTADOS DA FÍSICA", font=("Segoe UI", 12, "bold"), bg="#F7F9F9").pack(pady=(15, 5))
        
        self.lbl_estado = tk.Label(self.painel_esq, text="ESTADO: --", font=("Arial", 14, "bold"), bg="#F7F9F9")
        self.lbl_estado.pack(pady=0)
        
        # Caixa afundada (relief=tk.SUNKEN) onde as forças numéricas aparecerão calculadas instantaneamente
        self.lbl_info = tk.Label(self.painel_esq, text="", justify=tk.LEFT, bg="#FFFFFF", font=("Consolas", 11), relief=tk.SUNKEN, bd=1, padx=10, pady=10)
        self.lbl_info.pack(fill=tk.X, pady=5)
        
        # PAINEL DIREITO (A tela em branco gigante onde a animação e geometria acontecem)
        self.painel_dir = tk.Frame(self.main_frame, bg="white")
        self.painel_dir.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
    def setup_grafico(self):
        """Cria o Canvas do Matplotlib e instancía os desenhos iniciais (como o retângulo e as setas)"""
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        
        # FigureCanvasTkAgg é o conversor mágico: pega um gráfico complexo e injeta na nossa GUI do Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.painel_dir)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.D = 10.0 # Define que a "prancha" da rampa terá hipotenusa fixa de tamanho 10
        
        # Cria o polígono cinza da rampa. O 'zorder=1' garante que a rampa fique atrás de tudo
        self.rampa = patches.Polygon([[0, 0], [1, 0], [1, 1]], closed=True, color='#E0E0E0', ec='black', zorder=1)
        self.ax.add_patch(self.rampa)
        
        # Cria o retângulo azul do bloco (tamanho de 1.5 por 1.5) no 'zorder=2' para ficar acima da rampa
        self.lado = 1.5
        self.bloco = patches.Rectangle((-self.lado/2, 0), self.lado, self.lado, color='#3498DB', zorder=2)
        self.ax.add_patch(self.bloco)
        
        # Inicializa as Setas dos vetores usando FancyArrowPatch (ótimas porque têm cauda, cabeça customizável e cores vivas)
        self.setas = {
            'P': patches.FancyArrowPatch((0,0), (1,1), color='#E74C3C', mutation_scale=15, lw=2, zorder=3),
            'N': patches.FancyArrowPatch((0,0), (1,1), color='#27AE60', mutation_scale=15, lw=2, zorder=3),
            'Fat': patches.FancyArrowPatch((0,0), (1,1), color='#F39C12', mutation_scale=15, lw=2, zorder=3),
            'Px': patches.FancyArrowPatch((0,0), (1,1), color='#8E44AD', mutation_scale=15, lw=1.5, linestyle='dashed', zorder=3)
        }
        for s in self.setas.values():
            self.ax.add_patch(s)
            
        # Textos das legendas das setas
        self.textos_forca = {
            'P': self.ax.text(0,0, 'P', color='#E74C3C', fontweight='bold'),
            'N': self.ax.text(0,0, 'N', color='#27AE60', fontweight='bold'),
            'Fat': self.ax.text(0,0, 'Fat', color='#F39C12', fontweight='bold'),
            'Px': self.ax.text(0,0, 'Px', color='#8E44AD', fontweight='bold')
        }
        
        # Trava as proporções (aspect='equal' impede a rampa de esmagar) e desliga os eixos numéricos
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-1, 12)
        self.ax.set_ylim(-1, 11)
        self.ax.axis('off')
        
    def ao_mudar_slider(self, val):
        """Gatilho: sempre que o usuário mover um slider, a simulação pausa e se reinicia para atualizar a imagem."""
        self.resetar()
        
    def atualizar_fisica(self):
        """Coleta os dados, resolve as Leis de Newton, atualiza os textos de resposta e solicita redesenhar o quadro."""
        
        # 1. Coleta os valores numéricos dos Sliders
        m = self.scale_massa.get()
        theta_deg = self.scale_angulo.get()
        mu_e = self.scale_mue.get()
        mu_c = self.scale_muc.get()
        g = 9.81
        
        self.theta = np.radians(theta_deg) # Conversão para radianos exigida para cálculos de Sin e Cos
        
        # 2. Cálculos Trigonométricos
        self.P = m * g                          # Peso Total (vai do bloco ao chão)
        self.Px = self.P * np.sin(self.theta)   # Px: Componente paralela à rampa (tenta mover o bloco para baixo)
        self.Py = self.P * np.cos(self.theta)   # Py: Componente perpendicular (pressiona o bloco contra a superfície)
        self.N = self.Py                        # Normal: Reação da superfície para sustentar o bloco (mesmo módulo de Py)
        self.Fat_est_max = mu_e * self.N        # O limite final de resistência antes de escorregar (Força de Atrito Estático Máxima)
        
        # 3. Análise de Movimento
        if self.Px <= self.Fat_est_max:
            # Px (que empurra) não foi forte o suficiente para romper o Fat Máx (aderência)
            self.estado = "EM REPOUSO"
            self.Fat = self.Px       # Inteligência do Atrito Estático: ele atua apenas o suficiente para equilibrar Px. Não atua com o seu limite máximo.
            self.a = 0.0             # Sem movimento = sem aceleração
        else:
            # Px venceu a aderência!
            self.estado = "DESLIZANDO"
            self.Fat = mu_c * self.N # Agora, usamos o coeficiente de escorregamento (dinâmico/cinético)
            self.a = (self.Px - self.Fat) / m # Pela 2ª Lei de Newton: Aceleração = Força Resultante / Massa
            
        vel_atual = self.a * self.t_atual
            
        # 4. Atualiza os Títulos e Cores na Interface
        if self.estado == "EM REPOUSO":
            self.lbl_estado.config(text=f"{self.estado}", fg="#27AE60") # Verde
        else:
            self.lbl_estado.config(text=f"{self.estado}!", fg="#E74C3C") # Vermelho
            
        # Formata o texto para ser exibido em nossa caixa branca. Os comandos ':.1f' forçam apenas 1 casa decimal.
        info = (
            f"Tempo: {self.t_atual:.2f} s | Vel: {vel_atual:.2f} m/s\n"
            f"--------------------------------\n"
            f"Peso (P) : {self.P:.1f} N\n"
            f" ↳ Px: {self.Px:.1f} N | Py: {self.Py:.1f} N\n"
            f"Normal(N): {self.N:.1f} N\n"
            f"Fat Máx  : {self.Fat_est_max:.1f} N\n"
            f"Fat Real : {self.Fat:.1f} N\n"
            f"--------------------------------\n"
            f"Aceleração: {self.a:.2f} m/s²"
        )
        self.lbl_info.config(text=info)
        
        # 5. Após recalcular as componentes Físicas, chamamos a função que vai redesenhar as geometrias
        self.desenhar_frame_2d()
        
    def desenhar_frame_2d(self):
        """Posiciona blocos, inclina a rampa e desenha as setas visualmente no Canvas."""
        # --- ATUALIZAR RAMPA ---
        # Como D (Hipotenusa) vale 10. O Cateto Adjacente (Base L) = D * Cos, e o Cateto Oposto (Altura H) = D * Sen.
        L = self.D * np.cos(self.theta)
        H = self.D * np.sin(self.theta)
        self.rampa.set_xy([[0,0], [L,0], [L,H]]) # Aplica os novos vértices
        
        # --- POSICIONAR BLOCO ---
        # O topo da rampa é a origem (posição 0). 'dist_from_top' é o quanto ele desceu
        dist_from_top = 1.0 + self.s_atual # A margem 1.0 evita que ele nasça pendurado no precipício da rampa
        dist_from_origin = self.D - dist_from_top # Distância inversa da base para desenhar as coordenadas XY
        
        # Coordenadas do bloco convertidas para o eixo cartesiano normal da tela X e Y
        x_c = dist_from_origin * np.cos(self.theta)
        y_c = dist_from_origin * np.sin(self.theta)
        
        # Para desenhar o bloco INCLINADO, ele precisa sofrer uma transformação de Rotação seguida de Translação
        trans = transforms.Affine2D().rotate(self.theta).translate(x_c, y_c) + self.ax.transData
        self.bloco.set_transform(trans)
        
        # --- POSICIONAR VETORES ---
        # Acha exatamente o miolo do retângulo para plugar a cauda das setas
        x_centro = x_c - (self.lado/2) * np.sin(self.theta)
        y_centro = y_c + (self.lado/2) * np.cos(self.theta)
        
        # Essa escala serve para o Vetor não sair desenhado para fora da tela caso o bloco seja muito pesado (ex: P=500N)
        escala = 2.5 / self.P if self.P > 0 else 1
        
        # Atualiza a ponta da seta PESO (Sempre aponta perfeitamente para baixo = -y)
        self.setas['P'].set_positions((x_centro, y_centro), (x_centro, y_centro - self.P * escala))
        self.textos_forca['P'].set_position((x_centro + 0.2, y_centro - self.P * escala))
        
        # Atualiza NORMAL (Aponta para cima e perpendicular à rampa)
        nx = -self.N * escala * np.sin(self.theta)
        ny = self.N * escala * np.cos(self.theta)
        self.setas['N'].set_positions((x_centro, y_centro), (x_centro + nx, y_centro + ny))
        self.textos_forca['N'].set_position((x_centro + nx, y_centro + ny + 0.2))
        
        # Atualiza ATRITO (Paralelo à rampa, sempre contrário ao deslizamento = apontando pro topo)
        fat_x = self.Fat * escala * np.cos(self.theta)
        fat_y = self.Fat * escala * np.sin(self.theta)
        self.setas['Fat'].set_positions((x_centro, y_centro), (x_centro + fat_x, y_centro + fat_y))
        self.textos_forca['Fat'].set_position((x_centro + fat_x + 0.2, y_centro + fat_y + 0.2))
        
        # Atualiza Px (Paralelo à rampa, puxando pra base)
        px_x = -self.Px * escala * np.cos(self.theta)
        px_y = -self.Px * escala * np.sin(self.theta)
        self.setas['Px'].set_positions((x_centro, y_centro), (x_centro + px_x, y_centro + px_y))
        self.textos_forca['Px'].set_position((x_centro + px_x - 0.5, y_centro + px_y - 0.5))
        
        # Informa ao Canvas do Tkinter que os desenhos foram deslocados e ele precisa "se pintar de novo"
        self.canvas.draw_idle()
        
    def loop_animacao(self):
        """
        O CORAÇÃO DA ANIMAÇÃO (GAME LOOP). 
        Esta função roda incessantemente nos bastidores para gerar o movimento visual contínuo.
        """
        # Checa se o usuário clicou em Play e se o bloco de fato tem condições físicas de descer
        if self.is_animating and self.estado == "DESLIZANDO":
            # 1. O relógio avança em DT (Delta t = 0.04s)
            self.t_atual += self.dt
            
            # 2. Equação do Movimento MRUV: Posicao (S) = PosInicial (S0) + (Aceleração * Tempo_Quad) / 2
            # Nosso S0 no referencial é 0, portanto cortamos da equação.
            self.s_atual = 0.5 * self.a * (self.t_atual ** 2)
            
            # 3. Trava de Colisão (Checa se ele caiu da rampa)
            limite_descida = self.D - 2.5 # 'D' é 10. Subtraímos o tamanho do bloco para ele não varar o chão
            if self.s_atual >= limite_descida:
                self.s_atual = limite_descida
                self.is_animating = False # Freia a animação forçadamente porque chegou no chão!
                
            # 4. Agora que S_atual e T_atual mudaram, repassa para os desenhos se mexerem na tela
            self.atualizar_fisica()
            
        # MAGIA DO LOOP: O comando 'after(30, func)' diz ao Tkinter para disparar 'loop_animacao' novamente
        # depois de esperar 30 milissegundos. Isso cria a ilusão fluida de ~30 frames por segundo.
        self.root.after(30, self.loop_animacao)
        
    def iniciar(self):
        """Acionado pelo botão verde 'Iniciar'"""
        if self.estado == "DESLIZANDO":
            self.is_animating = True # Solta a trava do Game Loop
            
    def pausar(self):
        """Acionado pelo botão 'Pausar'"""
        self.is_animating = False # Pausa temporariamente o Game Loop sem zerar o relógio
        
    def resetar(self):
        """Acionado pelo botão 'Reset' e pelos Sliders para reiniciar a simulação do começo"""
        self.is_animating = False # Desativa animação
        self.t_atual = 0.0        # Zera o cronômetro
        self.s_atual = 0.0        # Reposiciona a distância virtual para 0 (início da rampa)
        self.atualizar_fisica()   # Aplica o posicionamento zerado de volta para a tela

if __name__ == "__main__":
    # 1. Inicializa o motor invisível da janela principal do Tkinter
    root = tk.Tk()
    
    # 2. Transfere o controle da janela para a nossa classe SimuladorGUI criada acima
    app = SimuladorGUI(root)
    
    # 3. Mantém a aplicação em loop infinito até que o usuário clique no "X" para fechar a tela.
    root.mainloop()
