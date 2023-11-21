import tkinter as tk
from tkinter import messagebox
import requests


authenticated = False
user_id = None
reserve_button = None


def open_login_page():
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    # Labels e Entries para o login
    tk.Label(login_window, text="Username:").pack()
    login_username_entry = tk.Entry(login_window)
    login_username_entry.pack()
    tk.Label(login_window, text="Password:").pack()
    login_password_entry = tk.Entry(login_window, show="*")
    login_password_entry.pack()

    def login():
        username = login_username_entry.get()
        password = login_password_entry.get()
        response = requests.post(
            "http://localhost:8001/login",
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            messagebox.showinfo("Success", response.json()["message"])
            login_window.destroy()
            global authenticated
            authenticated = True
            global user_id
            user_id = response.json()["id"]
            update_username(username)
            toggle_reserve_button(True)

            add_logout_button()
        else:
            messagebox.showinfo("Error", response.json()["message"])

    def open_create_user_page():
        create_user_window = tk.Toplevel(login_window)
        create_user_window.title("Criar utilizado")

        # Labels e Entries para criar usuário
        tk.Label(create_user_window, text="Novo Username:").pack()
        new_username_entry = tk.Entry(create_user_window)
        new_username_entry.pack()
        tk.Label(create_user_window, text="Nova Password:").pack()
        new_password_entry = tk.Entry(create_user_window, show="*")
        new_password_entry.pack()

        def create_user():
            new_username = new_username_entry.get()
            new_password = new_password_entry.get()
            response = requests.post(
                "http://localhost:8001/users",
                json={"username": new_username, "password": new_password},
            )
            if response.status_code == 201:
                messagebox.showinfo("Success", response.json()["message"])
                create_user_window.destroy()
            else:
                messagebox.showinfo("Error", response.json()["message"])

        create_user_button = tk.Button(
            create_user_window,
            text="Criar utilizador",
            command=create_user,
            font=("Arial", 14),
            fg="black",
            padx=10,
            pady=5,
        )
        create_user_button.pack()

    login_button = tk.Button(
        login_window,
        text="Login",
        command=login,
        font=("Arial", 14),
        fg="black",
        padx=10,
        pady=5,
    )
    login_button.pack()

    create_user_button = tk.Button(
        login_window,
        text="Criar utilizador",
        command=open_create_user_page,
        font=("Arial", 14),
        fg="black",
        padx=10,
        pady=5,
    )
    create_user_button.pack()


def get_movies():
    response = requests.get("http://localhost:8001/movies")
    movies = response.json()
    movies_listbox.delete(0, tk.END)
    movie_info = []
    for movie in movies:
        movie_details = f"{movie['Titulo']} - Lugares disponíveis: {movie['Lugares']}"
        movies_listbox.insert(tk.END, movie_details)
        movie_info.append(
            {
                "id": movie["id"],
                "title": movie["Titulo"],
                "seats": movie["Lugares"],
                "description": movie["Descrição"],
            }
        )
    return movie_info


def add_movie():
    add_movie_window = tk.Toplevel(root)
    add_movie_window.title("Adicionar Filme")

    # Labels e Entries para adicionar um filme
    tk.Label(add_movie_window, text="Título:").pack()
    title_entry = tk.Entry(add_movie_window)
    title_entry.pack()

    tk.Label(add_movie_window, text="Descrição:").pack()
    description_entry = tk.Entry(add_movie_window)
    description_entry.pack()

    tk.Label(add_movie_window, text="Sala:").pack()
    room_entry = tk.Entry(add_movie_window)
    room_entry.pack()

    tk.Label(add_movie_window, text="Lugares Disponíveis:").pack()
    seats_entry = tk.Entry(add_movie_window)
    seats_entry.pack()

    def create_movie():
        title = title_entry.get()
        description = description_entry.get()
        room = room_entry.get()
        seats = seats_entry.get()

        response = requests.post(
            "http://localhost:8001/showing_movies",
            json={
                "title": title,
                "description": description,
                "room": room,
                "seats": seats,
            },
        )

        if response.status_code == 201:
            messagebox.showinfo("Success", response.json()["message"])
            add_movie_window.destroy()
            get_movies()
        else:
            messagebox.showinfo("Error", response.json()["message"])

    create_movie_button = tk.Button(
        add_movie_window,
        text="Adicionar Filme",
        command=create_movie,
        font=("Arial", 14),
        fg="black",
        padx=10,
        pady=5,
    )
    create_movie_button.pack()


def delete_movie():
    selected_movie_index = movies_listbox.curselection()
    if selected_movie_index:
        selected_movie = movies_listbox.get(selected_movie_index)
        confirmation = messagebox.askyesno(
            "Confirmação", f"Tem certeza que deseja apagar o filme: {selected_movie}?"
        )

        if confirmation:
            movie_info = get_movies()
            movie_id = movie_info[selected_movie_index[0]]["id"]
            response = requests.delete(f"http://localhost:8001/movies/{movie_id}")

            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Filme apagado com sucesso.")
                get_movies()
            else:
                messagebox.showerror("Erro", "Falha ao apagar o filme.")
    else:
        messagebox.showinfo("Erro", "Selecione um filme para apagar.")


def reserve_movie():
    selected_movie_index = movies_listbox.curselection()
    global authenticated
    global user_id
    if selected_movie_index:
        if not authenticated:
            messagebox.showinfo(
                "Login obrigatório", "Por favor faça login para realizar uma reserva."
            )
            open_login_page()
            return

        movie_ids = get_movies()
        if selected_movie_index[0] < len(movie_ids):
            movie_id = movie_ids[selected_movie_index[0]]["id"]
            response = requests.post(
                "http://localhost:8001/reservations",
                json={"movie_id": movie_id, "user_id": user_id},
            )

            if response.text:
                data = response.json()
                if response.status_code == 200:
                    messagebox.showinfo(
                        "Success", data.get("message", "Reserca realiazda com sucesso.")
                    )
                    get_movies()
                elif response.status_code == 401:
                    messagebox.showinfo(
                        "Login obrigatório",
                        "Por favor faça login para realizar uma reserva.",
                    )
                    open_login_page()
                else:
                    messagebox.showinfo(
                        "Error", data.get("message", "Falha ao criar a reserva.")
                    )
            else:
                messagebox.showinfo("Error", "Sem resposta do servidor.")
        else:
            messagebox.showinfo("Error", "Seleccione o filme para reservar")


def get_movie_description():
    selected_movie_index = movies_listbox.curselection()

    if selected_movie_index:
        movie_ids = get_movies()
        
        if selected_movie_index[0] < len(movie_ids):
            movie = movie_ids[selected_movie_index[0]]

        if "title" in movie and "description" in movie:
            messagebox.showinfo(
                "Descrição do filme",
                f"Titulo: {movie['title']}\nDescrição: {movie['description']}",
            )
        else:
            messagebox.showinfo("Erro", "Informações do filme indisponíveis.")
    else:
        messagebox.showinfo("Erro", "Selecione um filme para ver a descrição.")


def add_logout_button():
    logout_button = tk.Button(
        root,
        text="Logout",
        command=logout,
        font=("Arial", 14),
        fg="black",
        padx=10,
        pady=5,
    )
    logout_button.pack()


def logout():
    global authenticated
    authenticated = False
    username_label.config(text="")
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button) and widget["text"] == "Logout":
            widget.pack_forget()


def update_username(username):
    username_label.config(text=f"Utilizador - {username}")


def toggle_reserve_button(show):
    global reserve_button
    global authenticated
    if show and authenticated:
        if not reserve_button:
            reserve_button = tk.Button(
                root,
                text="Reservar lugar",
                command=reserve_movie,
                font=("Arial", 14),
                fg="black",
                padx=10,
                pady=5,
            )
            reserve_button.pack()
    else:
        if reserve_button:
            reserve_button.pack_forget()


def on_window_open():
    get_movies()


def show_initial_message():
    welcome_message = (
        "Bem-vindo à sua plataforma de reservas. Precisa de ajuda? Digite 'Ajuda'."
    )
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, welcome_message + "\n")
    chat_log.config(state=tk.DISABLED)
    user_input.focus_set() 

    def handle_user_input(event):
        user_input.config(state=tk.DISABLED)
        user_response = user_input.get()
        if user_response.lower() == "ajuda":
            show_help_message()
        else:
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(
                tk.END,
                "Comando não reconhecido. Digite 'Ajuda' para obter assistência.\n",
            )
            chat_log.config(state=tk.DISABLED)
        user_input.unbind("<Return>")

    user_input.bind("<Return>", handle_user_input)


def choose_movie_with_most_seats(movies_info):
    max_seats = 0
    movie_with_most_seats = None

    for movie in movies_info:
        if movie["seats"] > max_seats:
            max_seats = movie["seats"]
            movie_with_most_seats = movie

    return movie_with_most_seats["title"] if movie_with_most_seats else None


def show_help_message():
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "Bot: Quer ajuda para escolher um filme? (Sim/Não)\n")
    chat_log.config(state=tk.DISABLED)


def send_message(event=None):
    message = user_input.get()
    if message.strip() != "":
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"Eu: {message}\n")
        movie_info = get_movies()

        if "ajuda" in message.lower():
            show_help_message()
        elif "sim" in message.lower():
            selected_movie = choose_movie_with_most_seats(movie_info)
            if selected_movie:
                chat_log.insert(
                    tk.END,
                    f"Bot: Recomendo '{selected_movie}' que possui mais lugares disponíveis.\n",
                )
            else:
                chat_log.insert(tk.END, "Bot: Não há filmes disponíveis no momento.\n")
        elif "não" in message.lower():
            chat_log.insert(
                tk.END,
                "Bot: Obrigado, aconselho a realizar a sua reserva antes que esgote.\n",
            )
        else:
            chat_log.insert(
                tk.END, "Bot: Não entendi. Pode reformular a sua resposta?\n"
            )

        chat_log.config(state=tk.DISABLED)
        user_input.delete(0, tk.END)


root = tk.Tk()
root.minsize(600, 500)
root.title("Reservas de Cinema")

header_label = tk.Label(
    root, text="Reservas de Cinema", font=("Helvetica", 24), pady=20
)
header_label.pack()

root.bind("<Map>", lambda event: on_window_open())

username_label = tk.Label(root, text="", font=("Arial", 12), fg="Red")
username_label.pack()

movies_listbox = tk.Listbox(root, width=60, font=("Arial", 12))
movies_listbox.pack()

buttons_frame = tk.Frame(root)
buttons_frame.pack()
add_movie_button = tk.Button(
    buttons_frame,
    text="Adicionar Filme",
    command=add_movie,
    font=("Arial", 14),
    fg="black",
    padx=10,
    pady=5,
)
add_movie_button.pack(side=tk.LEFT, padx=5)

delete_movie_button = tk.Button(
    buttons_frame,
    text="Apagar Filme",
    command=delete_movie,
    font=("Arial", 14),
    fg="black",
    padx=10,
    pady=5,
)
delete_movie_button.pack(side=tk.LEFT, padx=5)

button_frame = tk.Frame(root)
button_frame.pack()

login_button = tk.Button(
    button_frame,
    text="Login",
    command=open_login_page,
    font=("Arial", 14),
    fg="black",
    padx=10,
    pady=5,
)
login_button.pack(side=tk.LEFT)

description_button = tk.Button(
    button_frame,
    text="Descrição do filme",
    command=get_movie_description,
    font=("Arial", 14),
    fg="black",
    padx=10,
    pady=5,
)
description_button.pack(side=tk.LEFT, padx=10)

chat_frame = tk.Frame(root, relief=tk.SUNKEN, bd=1)
chat_frame.pack(side=tk.BOTTOM)

chat_log = tk.Text(chat_frame, wrap=tk.WORD, height=15, width=50)
chat_log.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
chat_log.config(state=tk.DISABLED)

user_input = tk.Entry(chat_frame)
user_input.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.BOTH, expand=True)
user_input.bind("<Return>", send_message)

send_button = tk.Button(chat_frame, text="Enviar", command=send_message)
send_button.pack(side=tk.BOTTOM, padx=5, pady=5)

show_initial_message()

root.mainloop()
