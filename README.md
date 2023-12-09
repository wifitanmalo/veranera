![logo](logo_1650x211.png)

Veranera
-------------
_Veranera_ es una aplicación hecha con **Python** para administrar una cafetería, esta permite registrar un usuario para iniciar sesión y al hacerlo genera tres menús en los cuales se pueden crear platos, reservar mesas y realizar pedidos respectivamente, además de un botón para cerrar sesión cuando el empleado haya terminado su trabajo dentro de la aplicación.

### Hecha por:
> - Andrés Felipe Castrillón (2380664)
> - Johan Alexander Castro (2380818)
> - Nicolás Chaparro (2380530)

# Inicio de programa
-------------

#### Página principal
	if __name__ == '__main__':
		reserved_tables = []
		available_plates = []
		available_options = ["Yes", "No"]
		try:
			window = tk.Tk()
			back_frame = tk.Frame(window)
			back = tk.Button(back_frame, text="Back",
					command=home)
			back.pack()
			icon = tk.PhotoImage(file="icon.png")
			logo = tk.PhotoImage(file="logo.png")
			window.iconphoto(True, icon)
			veranera = ttk.Label(window, image=logo)
			veranera.pack()
		except:
			print("- Error loading images")
		finally:
			window.title("Coffee shop: veranera")
			window.geometry("300x550")
			window.resizable(False, False)
			home()
			menu()
			window.mainloop()

> El código comienza generando una ventana de Tkinter para luego importar tanto el logo como el ícono y así añadirlos en esta, además de llamar a la función **home()** que se encargará de generar la página principal y la función **menu()** que se explicará más adelante. Como puede presentarse el caso de que las imágenes no se acarguen correctamente se maneja una excepción para que la aplicación siga funcionando con normalidad.

    def home():
		global text, home_frame
		home_frame = tk.Frame(window)
		home_frame.pack()
		try:
			back_frame.pack_forget()
			account_frame.pack_forget()
			tab.pack_forget()
		except:
			print("- Start error")
		finally:
			message = tk.Label(home_frame,
						   font=("Verdana", 9),
						   justify="center",
						   text="""
		In Veranera we pride ourselves on offering
		a unique experience that combines delicious
		flavors, a cozy atmosphere and a variety of 
		services to satisfy your tastes and needs.
		Come and discover the charm of Veranera
		where every sip tells a story and every bite
		is a delicious adventure!
		""")
			message.pack()
			sign_in = tk.Button(home_frame, text="Sign in", command=signin)
			sign_in.pack()
			sign_up = tk.Button(home_frame, text="Sign up", command=signup)
			sign_up.pack()
			text = tk.Label(home_frame, text="", font=("Verdana", 10))
			text.pack()

> Esta función se encarga de generar la **página principal**, en ella se empaquetarán la descripción de la cafetería junto con los botones de inicio de sesión y registro de usuario, se maneja una excepción debido a que la función al estar pensada para ser utilizada cada que se quiera cerrar sesión o devolverse durante un inicio/registro, contiene algunos comandos para olvidar objetos que pueden lanzar error por presentarse casos en los que no han sido llamados aún **(como cuando recíen se abre la aplicación).**

#### Registro de sesión
Al pulsar el botón de registro se llama una función con el nombre **singup()**, la cual se encarga de llamar a la función **enter_email():**

	def enter_email():
		global the_email, email_error, email_text, account_frame
		home_frame.pack_forget()
		account_frame = tk.Frame(window)
		account_frame.pack()
		email_text = tk.Label(account_frame, text="Email:")
		email_text.pack()
		the_email = tk.Entry(account_frame, width=22)
		the_email.pack()
		email_error = tk.Label(account_frame, text="")
		email_error.pack()

> Esta función se encarga de crear un Frame en el que se empaquetará el cuadro de entrada para el correo junto con un mensaje vacío, el cual será usado posteriormente para indicar si hubo algún error.

Al final del cuadro se añadirá tanto un botón para enviar el correo como uno para devolverse a la página principal. Al enviar el correo se llama a la función **create_email()**:

	def create_email():
    global email, confirm_text, pass_error, confirm_pass
    email_digits = "abcdefghijklmnopqrstuvwxyz0123456789._"
    valid_domains = ["@gmail.com", "@hotmail.com", "@yahoo.com",
                    "@outlook.es", "@correounivalle.edu.co"]
    try:
        email = the_email.get().lower()
        user = email[0:email.index("@")]
        domain = email[email.index("@"):len(email)]
        if (len(user) == 0) or (len(user) < 6) or (len(user) > 30):
            raise ValueError
        elif domain not in valid_domains:
            raise Exception
        for word in user:
            if word not in email_digits:
                raise ValueError
        with open('registered_accounts.txt',
                  'r',
                  encoding="utf-8") as email_file:
            accounts_list = email_file.readlines()
            for line in range(0, len(accounts_list)):
                account = accounts_list[line].split()
                if account[0] == email:
                    raise KeyboardInterrupt
        email_error.config(text=email, fg="#808080")
        enter_password()
        confirm_text = tk.Label(account_frame,
                                text="Confirm password:")
        confirm_text.pack()
        confirm_pass = tk.Entry(account_frame, width = 22,
                                show="*")
        confirm_pass.pack()
        pass_error = tk.Label(account_frame, text="")
        pass_error.pack()
        register = tk.Button(account_frame, text="Register",
                            command=create_password)
        register.pack() 
    except ValueError:
        email_error.config(text="- Invalid username",
                            fg="#FF0000")
        clean_email()
    except FileNotFoundError:
        email_error.config(text="- Unknown error",
                            fg="#FF0000")
        clean_email()
    except KeyboardInterrupt:
        email_error.config(text="- Email already exists",
                            fg="#FF0000")
        clean_email()
    except:
        email_error.config(text = "- Invalid email",
                           fg = "#FF0000")
        clean_email()

> Esta función se encarga de obtener el correo ingresado para verificar varios detalles:
> - **Nombre de usuario mayor a 7 dígitos y menor a 30 y dominio de correo válido:**  para verificar el nombre de usuario se recorta el correo desde la primera letra hasta el @ y se asigna a la variable __user__, lo mismo se aplica para el dominio en la variable __domain__, pero desde el @ hasta la última letra del correo. Luego se aplica una condición comprobando que la longitud del nombre cumpla con la permitida y que el dominio se encuentre en la lista __valid_domains.__
> - **Dígitos permitidos:** se utiliza un ciclo for que recorre cada letra de la variable **user** para comprobar que el caracter se encuentre en la lista __email_digits.__
> - **Correo no existente:** abre el archivo de correos registrados y al igual que con el anterior punto se utiliza un ciclo for para revisar cada línea del archivo de texto y comprobar que el correo no haya sido registrado anteriormente.

En caso de que alguna de estas condiciones no se cumpla se activará un error que mostrará un mensaje de error, además de vaciar el respectivo cuadro. Si el correo cumple con los requisitos, el cuadro se reemplazará por el email en color gris para luego aparecer los cuadros de contraseña/confirmar contraseña junto con el botón de terminar registro el cual llamará a la función **create_password():**

	def create_password():
		global password
		password = the_pass.get()
		confirm = confirm_pass.get()
		if password == confirm:
			if password_strength():
				hash = hashlib.sha256(password.encode("utf-8"))
				with open('registered_accounts.txt', 'a', encoding="utf-8") as file:
					file.write(f"{email} {password} {hash.hexdigest()}\n")
				account_frame.pack_forget()
				back_frame.pack_forget()
				home()
				text.config(text="- Account created succesfully!",
							fg="#008000")
			else:
				pass_error.config(text="""Must contain:
	- a lowercase letter (a-z)
	- a upper letter (A-Z)
	- a number (0-9)
	- a symbol (@*$!?\&/.-_)
	- 10 characters long""", font=("Verdana", 8), fg = "#FF0000",
								  justify="left")
				clean_pass()
		else:
			pass_error.config(text="- Passwords don't match",
							  fg="#FF0000")
			clean_pass()

> Esta función obtiene los datos de los cuadros de contraseña para verificar que sean iguales, si lo son llama a la función **password_strength()** la cual de manera similar a la función **create_email()** utiliza un ciclo for para comprobar cada dígito encargándose de verificar que contenga una letra minúscula, una letra mayúscula, un número, un caracter especial y que su longitud sea mayor a 10. En caso de que solo una no se cumpla, el retorno de la función pasará a ser False, vaciando los cuadros de contraseña e indicando por mediode un texto los requisitos que esta debe cumplir. Si se cumplen todas las condiciones la contraseña pasará a ser encriptada con el método **SHA-256** para luego abrir el archivo de texto en el que se registran las cuentas y escribir en este el correo, la contraseña y su encriptación. Ya finalmente llamará a la función **home()** para regresar a la página principal y se mostrará un mensaje indicando que el correo ha sido registrado con éxito.

#### Inicio de sesión
Al pulsar el botón de registro se llama una función con el nombre **singin()**, la cual hace exactamente lo mismo que la función **signup()** con la diferencia de que el botón ahora llamará a la función **verify_email():**

	def verify_email():
    global pin, pass_error
    email = the_email.get().lower()
    try:
        with open('registered_accounts.txt', 'r', encoding="utf-8") as email_file:
            accounts_list = email_file.readlines()
            for line in range(0, len(accounts_list)):
                account = accounts_list[line].split()
                user = account[0]
                pin = account[2]
                if user == email:
                    email_error.config(text=email, fg="#808080")
                    enter_password()
                    pass_error = tk.Label(account_frame, text="")
                    pass_error.pack()
                    log_in = tk.Button(account_frame, text="Log in",
                                        command=verify_password)
                    log_in.pack()
                    break
            if user != email:
                email_error.config(text="- Email not found",
                            fg="#FF0000")
                clean_email()
    except FileNotFoundError:
        email_error.config(text="- Unknown error",
                            fg="#FF0000")
        clean_email()

> Esta función, al igual que la función **create_email()** se encarga de obtener el email enviado para luego leer cada línea del archivo de cuentas registradas almacenándolas en la variable **user** junto con su encriptación en la variable **pin** y verificar por medio de un ciclo for que el correo se encuentre registrado, en caso de no encontrar el correo o se produzca un error con el manejo del archivo se vacía la entrada para mostrar un mensaje de error, pero si el correo se encuentra correctamente se detiene el ciclo para que aparezca el cuadro de contraseña con el botón de inciar sesión que llamará a la función **verify_password():**

	def verify_password():
    password = the_pass.get()
    hash = hashlib.sha256(password.encode("utf-8"))
    print(hash.hexdigest(), pin)
    if hash.hexdigest() == pin:
        account_frame.pack_forget()
        back_frame.pack_forget()
        tab.pack(expand=True, fil="both")
    else:
        pass_error.config(text="- Incorrect password",
                          fg="#FF0000")
        the_pass.delete(0, "end")

> Esta función se encarga de encriptar la contraseña registrada para compararla con la que quede asignada a la variable **pin,** si ambos datos coinciden se actualizará la ventana con las tablas que fueron llamadas con la función **menu()** al inicio del programa, pero que no habían sido empaquetadas. En caso contrario se vacía el cuadro de contraseña y se muestra un mensaje de error.

- **Nota:** sin el archivo de cuentas registradas **"registered_accounts.txt"** la aplicación no puede funcionar.

Menú de opciones
-------------
Al entrar a la aplicación se generarán tres menús: uno para platos, otro para mesas y el último para pedidos, cada uno contiene una tabla junto con tres botones para agregar, actualizar y eliminar respectivamente. Aquí se muestra cómo se genera la tabla usando de ejemplo el menú de pedidos **(por ser el menos extenso):**

	def orders_table():
    global orders, plate_entry, table_entry, error_text3
    columns = ("Plate's name:", "Table's number:")
    orders = ttk.Treeview(order, columns=columns, show="headings")
    orders.column("Plate's name:", width=140, anchor=tk.CENTER)
    orders.column("Table's number:", width=140, anchor=tk.CENTER)
    orders.heading("Plate's name:", text="Plate's name:")
    orders.heading("Table's number:", text="Table's number:")
    orders.pack()
    add_frame = tk.Frame(order)
    add_frame.pack()
    plate_text = tk.Label(add_frame, text="Plate's name:")
    plate_text.pack()
    plate_entry = tk.Entry(add_frame)
    plate_entry.pack()
    table_text = tk.Label(add_frame, text="Table's number:")
    table_text.pack()
    table_entry = tk.Entry(add_frame)
    table_entry.pack()
    error_text3 = tk.Label(add_frame, text="")
    error_text3.pack()
    add = tk.Button(add_frame, text="Add", command=add_order)
    add.pack()
    update = tk.Button(add_frame, text="Update", command=update_order)
    update.pack()
    delete = tk.Button(add_frame, text="Delete", command=delete_order)
    delete.pack()

> Esta función se encarga de generar las columnas junto con los encabezados de la tabla para luego crear un Frame en el que se empaquetarán los cuadros con los que se rellenarán dichas tablas y sus respectivos botones.

#### Platos
-------------
La sección de platos contendrá cuatro entradas: __nombre, valor, descripción y disponibilidad,__ las cuales pueden ser rellenadas por medio de la función **add_plate()** llamada por el botón agregar:

	def add_plate():
    try:
        plate_data()
        for item in plates.get_children():
            if plates.item(item, "values")[0] == name:
                raise KeyboardInterrupt
        if (len(name) == 0) or (len(description) == 0):
            error_text1.config(text="- There can't be empty spaces",
                                fg="#FF0000")
            clean_plate_entrys()
        elif value < 1:
            error_text1.config(text="- Negative numbers not allowed",
                                fg="#FF0000")
            clean_plate_entrys()
        elif available not in available_options:
            error_text1.config(text="- Available only gets (Yes/No)",
                                fg="#FF0000")
            clean_plate_entrys()
        else:
            if available == "Yes":
                available_plates.append(name)
            plates.insert('', 'end', values=(name,
                                             f"${value}",
                                             description,
                                             available))
            error_text1.config(text="- Plate added succesfully",
                               fg="#008000")
            clean_plate_entrys()
    except KeyboardInterrupt:
        error_text1.config(text="- Plate's name already exists",
                            fg="#FF0000")
        clean_plate_entrys()
    except:
        error_text1.config(text="- Error, try again",
                            fg="#FF0000")
        clean_plate_entrys()

> Esta función se encarga de llamar a la función **plate_data()** la cual obtiene los datos ingresados en los cuadros para luego revisar si cumplen con las siguientes condiciones:
> - **Nombre no existente:** haciendo uso del comando **get_children()** se revisa el primer item de cada fila de la tabla para comprobar por medio de un ciclo for que el nombre no exista, en caso de existir suelta un error.
> - **Espacios rellenados:** verifica por medio del metodo len si tanto el nombre como la descripción han sido rellenados, los otros dos no los tiene en cuenta ya que estos sueltan un error por uno recibir valores enteros y el otro los valores de una lista.
> - **Valores positivos:** se verifica que el número ingresado en el cuadro de valor sea un número mayor a cero.
> - **Disponibilidad:** como se mencionó anteriormente el cuadro de disponibilidad solo recibe los valores de la lista **available_options** la cual contiene las cadenas **["Yes", "No"].**

> En caso de que todos los datos sean correctos se modificará la respectiva fila de la tabla con los valores ingresados mostrando un mensaje de que el plato se añadió correctamente, en caso de que el plato tenga la disponiblidad **Yes** se añadirá su nombre a una lista que se encuentra en el inicio del programa llamada **available_plates.** 

Al haber creado un plato satisfactoriamente, puedes seleccionarlo para actualizarlo ingresando nuevos valores o simplemente eliminarlo.

#### Actualizar
	def update_plate():
    try:
        selection = plates.selection()
        selected_name = plates.item(selection, "values")[0]
        selection = plates.selection()
        if selection:
            plate_data()
            for item in plates.get_children():
                if(item != selection[0]
                   and plates.item(item, "values")[0] == name):
                    raise KeyboardInterrupt
            if (len(name) == 0) or (len(description) == 0):
                error_text1.config(text="- Can't leave empty spaces",
                                    fg="#FF0000")
                clean_plate_entrys()
            elif value < 1:
                error_text1.config(text="- Negative numbers not allowed",
                                    fg="#FF0000")
                clean_plate_entrys()
            elif available not in available_options:
                error_text1.config(text="- Available only gets (Yes/No)",
                                    fg="#FF0000")
                clean_plate_entrys()
            else:
                if selected_name != name:
                    if ((selected_name not in available_plates)
                        and (available == "Yes")):
                        available_plates.append(name)
                    elif ((selected_name in available_plates)
                          and (available == "No")):
                        available_plates.append(name)
                        available_plates.remove(selected_name)
                    elif ((selected_name in available_plates)
                          and (available == "Yes")):
                        available_plates.append(name)
                        available_plates.remove(selected_name)
                elif selected_name == name:
                    if ((name not in available_plates)
                        and (available == "Yes")):
                        available_plates.append(name)
                    elif ((name in available_plates)
                          and (available == "No")):
                        available_plates.remove(name)
                plates.item(selection, values=(name,
                                               f"${value}",
                                               description,
                                               available))
                error_text1.config(text="- Plate updated succesfully",
                                    fg="#008000")
                clean_plate_entrys()
    except KeyboardInterrupt:
        error_text1.config(text="- Plate's name already exists",
                            fg="#FF0000")
        clean_plate_entrys()
    except:
        error_text1.config(text="- Error, try again",
                            fg="#FF0000")
        clean_plate_entrys()

> Esta función trabaja de la misma forma que la función **add_plate()** con la diferencia que al cumplir con los requisitos se tienen en cuenta distintos condiciones como:
> - **Si el nombre a actualizar es diferente al ingresado:** en caso de no encontrarse el antiguo nombre en la lista de **available_plates()** y la disponibilidad es actualizada a **"Yes"**, el nuevo nombre debe ser agregado a la lista. Si el antiguo nombre estaba en dicha lista, pero la disponibilidad se actualiza a **"No"** el antiguo nombre deber eliminado para añadir el nuevo a la lista y si el antiguo nombre estaba en la lista y su disponibilidad se mantiene en **"Yes** se hace exactamente lo mismo que con la anterior condición.
> - **Si el nombre a actualizar es igual al ingresado:** si el nombre no se encontraba en la lista de **available_plates()** y su disponibilidad se actualiza a **Yes** el nombre es agregado a esta y si el nombre ya estaba en la lista, pero su disponibilidad se actualiza a **"No"** este debe eliminarse

#### Eliminar
	def delete_plate():
    try:
        selection = plates.selection()
        delete_name = plates.item(selection, "values")[0]
        if delete_name in available_plates:
            available_plates.remove(delete_name)
        if selection:
            plates.delete(selection)
            error_text1.config(text="- Plate deleted succesfully",
                                       fg="#008000")
        clean_plate_entrys()
    except:
        error_text1.config(text="- Error, try again",
                            fg="#FF0000")
        clean_plate_entrys()
> Esta función se encarga de eliminar la fila seleccionado y en caso de que el nombre eliminado se encontrara almacenado en la lista **available_plates()** se elimina de esta.

#### Mesas
-------------
Las mesas al igual que los platos poseen 4 casillas en la tabla: **Número de mesa, fecha, hora y número de personas,** pero ahora solo se piden tres datos a rellenar ya que el número de la mesa se hace de manera aleatoria eligiendo un número del 1 al 8. El código de añadir mesas es casi idéntico al de añadir platos:

	def book_table():
    try:
        table_data()
        the_table = random_table
        for item in tables.get_children():
            if ((int(tables.item(item, "values")[0]) == the_table)
                and (tables.item(item, "values")[1] == date)
                and (tables.item(item, "values")[2] == hour)):
                raise KeyboardInterrupt
        if people < 1:
            error_text2.config(text="- Negative numbers not allowed",
                            fg="#FF0000")
            clean_table_entrys()
        elif people > 10:
            error_text2.config(text="- People can't be more than 10",
                            fg="#FF0000")
            clean_table_entrys()
        else:
            tables.insert('', 'end', values=(the_table,
                                             date,
                                             hour,
                                             people))
            reserved_tables.append(the_table)
            error_text2.config(text="- Table reserved succesfully",
                               fg="#008000")
            clean_table_entrys()
    except ValueError:
        error_text2.config(text="- Invalid date or hour",
                            fg="#FF0000")
        clean_table_entrys()
    except KeyboardInterrupt:
        error_text2.config(text="- Table not available for that date",
                            fg="#FF0000")
        clean_table_entrys()

> Esta función se encarga de revisar por medio de un ciclo for que el número de mesa, la fecha y la hora no se repetan con una ya existente, para luego revisar que el número de personas no sea menor a 1 ni mayor a 10 para finalmente agregar los valores en la tabla y el número de mesa en una lista encontrada en el punto de inicio de la aplicación llamada **reserved_tables** en la que se registran las tablas ya reservadas.
> - **Nota:** no se encontró la manera de pedir la hora en la que inicia y termina una reserva para calcular un periodo en el que dicha mesa no pueda ser reservada, por lo que por ejemplo una misma mesa puede ser reservada por una persona a las 22:09 y por otra a las 22:10 del mismo día, cosa que claramente no es posible en la vida real.

La diferencia radica en que como ahora se pide tanto fecha como hora, la función **table_data** que se encarga de recoger los datos ingresados en los campos debe hacer uso de la librería **datetime** para comprobar que no se ingresa una fecha u hora inválidas y lanzar un error en caso de que esto sea así.

	def table_data():
    global random_table, date, hour, people, date_format, hour_format
    random_table = random.randint(1, 9)
    date = date_entry.get()
    hour = hour_entry.get()
    people = int(people_entry.get())
    date_format = datetime.strptime(date, "%d/%m/%Y")
    hour_format = datetime.strptime(hour, "%H:%M")

La función tanto de actualizar como de eliminar mesas son exactamente iguales a las de los platos **(con sus respectivas condiciones claro está),** la diferencia radica en que si el número de mesa a eliminar se encuentra en la lista **reserved_tables** se elimina también de esta.

#### Pedidos
---
Y llegamos a la parte final y más sencilla del código, los pedidos solo poseen dos casillas: **nombre del plato y nùmero de mesa,** esta como se puede apreciar depende de las dos anteriores tablas para poder ser utilizada.

	def add_order():
    try:
        order_data()
        if len(plate_name) == 0:
            error_text3.config(text="- There can't be empty spaces",
                                fg="#FF0000")
            clean_order_entrys()
        elif plate_name not in available_plates:
            error_text3.config(text="- Plate isn't available",
                                fg="#FF0000")
            clean_order_entrys()
        elif table_number < 1:
            error_text3.config(text="- Negative numbers not allowed",
                                fg="#FF0000")
            clean_order_entrys()
        elif table_number not in reserved_tables:
            error_text3.config(text="- Table not reserved yet",
                                fg="#FF0000")
            clean_order_entrys()
        else:
            orders.insert('', 'end', values=(plate_name, table_number))
            error_text3.config(text="- Order added succesfully",
                               fg="#008000")
            clean_order_entrys()
    except:
        error_text3.config(text="- Error, try again",
                            fg="#FF0000")
        clean_order_entrys()

> Esta funciòn se encarga de llamar a la función **order_data()** que se encarga de recoger los datos de ambos cuadros para asì comprobar que el nombre del plato no esté vacío, que este se encuentre en la lista **available_plates,** que el número de mesa no sea negativo y que este a su vez se encuentre en la lista **reserved_tables.** Es por esta razón que si no hay platos disponibles ni mesas reservadas no se puede realizar ni un solo pedido.

Al momento de tanto actualizar como eliminar las cosas funcionan de manera más sencilla que con las anteriores tablas, porque para actualizar simplemente se revisa que los datos cumplan con las mismas condiciones mostradas en la anterior función y para eliminar la orden se elimina sin más.

###### *- uwu*
