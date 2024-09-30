import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont


# Função para configurar a palavra secreta
def configurar_palavra_secreta(event=None):
    global palavra_secreta
    palavra_secreta = entry_palavra_secreta.get().upper()  # Maiúsculas

    if not palavra_secreta.isalpha():
        messagebox.showwarning("Erro", "A palavra deve conter apenas letras.")
        return

    entry_palavra_secreta.delete(0, tk.END)
    esconder_tela_configurar_palavra()
    iniciar_jogo()


# Função para iniciar o jogo
def iniciar_jogo():
    global letras_adivinhadas, tentativas_restantes, letras_erradas
    letras_adivinhadas = ["_" for _ in palavra_secreta]
    tentativas_restantes = 6
    letras_erradas = []

    # Limpar e atualizar o Canvas
    canvas.delete("all")
    desenhar_forca_estrutura()  # Desenhar a estrutura da forca inicialmente
    desenhar_forca(0)
    atualizar_palavra_mostrada()
    atualizar_interface()

    mostrar_tela_jogo()


# Função para adivinhar uma letra
def adivinhar(event=None):
    global tentativas_restantes
    letra = entry_letra.get().upper()  # Maiúsculas
    entry_letra.delete(0, tk.END)

    if len(letra) != 1 or not letra.isalpha():
        messagebox.showwarning("Erro", "Digite uma única letra.")
        return

    if letra in letras_adivinhadas or letra in letras_erradas:
        messagebox.showinfo("Erro", "Você já tentou essa letra!")
        return

    if letra in palavra_secreta:
        for i, char in enumerate(palavra_secreta):
            if char == letra:
                letras_adivinhadas[i] = letra
    else:
        tentativas_restantes -= 1
        letras_erradas.append(letra)
        desenhar_forca(6 - tentativas_restantes)

    atualizar_palavra_mostrada()
    atualizar_interface()

    if tentativas_restantes == 0:
        messagebox.showinfo("Fim de Jogo", f"Você perdeu! A palavra era: {palavra_secreta}")
        mostrar_tela_configurar_palavra()
    elif "_" not in letras_adivinhadas:
        messagebox.showinfo("Fim de Jogo", "Parabéns! Você ganhou!")
        mostrar_tela_configurar_palavra()


# Função para desenhar a forca e o boneco (começando pela cabeça)
def desenhar_forca(estagio):
    if estagio >= 1:  # Cabeça
        canvas.create_oval(180, 100, 220, 140, width=4)
    if estagio >= 2:  # Corpo
        canvas.create_line(200, 140, 200, 200, width=4)
    if estagio >= 3:  # Braço esquerdo
        canvas.create_line(200, 160, 170, 180, width=4)
    if estagio >= 4:  # Braço direito
        canvas.create_line(200, 160, 230, 180, width=4)
    if estagio >= 5:  # Perna esquerda
        canvas.create_line(200, 200, 180, 230, width=4)
    if estagio >= 6:  # Perna direita
        canvas.create_line(200, 200, 220, 230, width=4)


# Função para desenhar a estrutura da forca
def desenhar_forca_estrutura():
    # Base e estrutura da forca
    canvas.create_line(100, 250, 250, 250, width=4)  # Base
    canvas.create_line(150, 250, 150, 50, width=4)  # Poste
    canvas.create_line(150, 50, 200, 50, width=4)  # Viga superior
    canvas.create_line(200, 50, 200, 80, width=4)  # Corda


# Função para atualizar a palavra mostrada
def atualizar_palavra_mostrada():
    label_palavra.config(text=" ".join(letras_adivinhadas))


# Função para atualizar os textos da interface
def atualizar_interface():
    label_tentativas.config(text=f"Tentativas restantes: {tentativas_restantes}")
    label_letras_erradas.config(text=f"Letras erradas: {' '.join(letras_erradas)}")


# Função para mostrar a tela de configuração da palavra secreta
def mostrar_tela_configurar_palavra():
    frame_jogo.pack_forget()
    frame_configurar_palavra.pack()

    # Alterar o bind do Enter para configurar a palavra
    root.unbind('<Return>')
    root.bind('<Return>', configurar_palavra_secreta)


# Função para esconder a tela de configuração e mostrar a tela do jogo
def esconder_tela_configurar_palavra():
    frame_configurar_palavra.pack_forget()
    frame_jogo.pack()

    # Alterar o bind do Enter para adivinhar letras
    root.unbind('<Return>')
    root.bind('<Return>', adivinhar)


# Função para mostrar a tela do jogo
def mostrar_tela_jogo():
    frame_jogo.pack()


# Configuração da janela principal
root = tk.Tk()
root.geometry("600x650")
root.title("Jogo de Forca")
root.configure(bg='#F0F8FF')

# Tela para o usuário 1 escolher a palavra secreta
frame_configurar_palavra = tk.Frame(root, padx=20, pady=20, bg='#F0F8FF')
frame_configurar_palavra.pack(expand=True)

label_titulo_config = tk.Label(frame_configurar_palavra, text="Jogo de Forca", font=("Helvetica", 24, "bold"),
                               fg="blue", bg='#F0F8FF')
label_titulo_config.pack()

label_instrucoes_palavra = tk.Label(frame_configurar_palavra, text="Usuário 1, digite a palavra secreta:",
                                    font=("Helvetica", 14), bg='#F0F8FF')
label_instrucoes_palavra.pack(pady=10)

entry_palavra_secreta = tk.Entry(frame_configurar_palavra, show="*", font=("Helvetica", 14))
entry_palavra_secreta.pack(pady=10)

button_confirmar_palavra = tk.Button(frame_configurar_palavra, text="Confirmar", font=("Helvetica", 14),
                                     command=configurar_palavra_secreta)
button_confirmar_palavra.pack(pady=10)

# Tela para o usuário 2 jogar
frame_jogo = tk.Frame(root, padx=20, pady=20, bg='#FFF5EE')

label_titulo_jogo = tk.Label(frame_jogo, text="Jogo de Forca", font=("Helvetica", 24, "bold"), fg="green", bg='#FFF5EE')
label_titulo_jogo.pack()

label_instrucoes = tk.Label(frame_jogo, text="Usuário 2, digite uma letra e pressione 'Enter':", font=("Helvetica", 14),
                            bg='#FFF5EE')
label_instrucoes.pack(pady=10)

label_palavra = tk.Label(frame_jogo, text="", font=("Courier", 20, "bold"), bg='#FFF5EE')
label_palavra.pack(pady=20)

label_tentativas = tk.Label(frame_jogo, text="Tentativas restantes: 6", font=("Helvetica", 14), bg='#FFF5EE')
label_tentativas.pack(pady=10)

label_letras_erradas = tk.Label(frame_jogo, text="Letras erradas: ", font=("Helvetica", 14), bg='#FFF5EE')
label_letras_erradas.pack(pady=10)

entry_letra = tk.Entry(frame_jogo, font=("Helvetica", 14), justify='center')
entry_letra.pack(pady=10)
entry_letra.focus_set()  # Foco automático na entrada

# Canvas para desenhar a forca e o boneco
canvas = tk.Canvas(frame_jogo, width=300, height=300, bg='#FFF5EE')
canvas.pack()

# Iniciar o loop principal da interface
root.mainloop()
