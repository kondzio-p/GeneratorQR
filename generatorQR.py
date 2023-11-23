'''
Zadanie zaliczeniowe z języka Python
Imię i nazwisko ucznia: Konrad Pepliński
Data wykonania zadania: 23.11
Treść zadania: Aplikacja do tworzenia kodów QR.
Opis funkcjonalności aplikacji: Aplikacja do tworzenia własnych kodów QR z dodatkową funkcjonalnością zapisywania historii wygenerowanych kodów qr. 
'''
import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import qrcode
from fpdf import FPDF
import tempfile
import os
import sys
import datetime
import webbrowser  # Dodany import

class QRCodeGenerator:
    '''Klasa do generowania kodów QR.'''

    def __init__(self):
        '''Inicjalizacja okna głównego aplikacji'''
        self.root = tk.Tk()
        self.root.title("Generator kodów QR")
        self.root.geometry("350x350")

        self.label = tk.Label(self.root, text="Wprowadź dane do wygenerowania kodu QR:")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=5)  

        self.creator_label = tk.Label(self.root, text="Twórca kodu:")
        self.creator_label.pack()

        self.creator_entry = tk.Entry(self.root)
        self.creator_entry.pack(pady=5)  

        self.size_var = tk.StringVar()
        self.size_var.set("Mały")
        self.size_label = tk.Label(self.root, text="Rozmiar kodu QR:")
        self.size_label.pack()

        self.size_combobox = ttk.Combobox(self.root, textvariable=self.size_var, values=["Mały", "Średni", "Duży", "Bardzo duży"])
        self.size_combobox.pack(pady=5)  

        self.qr_color_button = tk.Button(self.root, text="Wybierz kolor kodu QR", command=self.choose_qr_color)
        self.qr_color_button.pack(pady=5)

        self.bg_color_button = tk.Button(self.root, text="Wybierz kolor tła kodu QR", command=self.choose_bg_color)
        self.bg_color_button.pack(pady=5)

        self.generate_button = tk.Button(self.root, text="Generuj kod QR", command=self.generate_qr)
        self.generate_button.pack(pady=5)  

        self.open_html_button = tk.Button(self.root, text="O QR kodach", command=self.open_index_html)
        self.open_html_button.pack(pady=5)

        self.cancel_button = tk.Button(self.root, text="Anuluj", command=self.cancel)
        self.cancel_button.pack(pady=5)


        self.qr_color = "black"
        self.bg_color = "white"

        self.root.mainloop()

    def choose_qr_color(self):
        '''Metoda do wyboru koloru kodu QR.'''
        color = colorchooser.askcolor(title="Wybierz kolor kodu QR")
        if color[1]:
            self.qr_color = color[1]

    def choose_bg_color(self):
        '''Metoda do wyboru koloru tła kodu QR.'''
        color = colorchooser.askcolor(title="Wybierz kolor tła kodu QR")
        if color[1]:
            self.bg_color = color[1]

    def generate_qr(self):
        '''Metoda generująca kod QR na podstawie danych wprowadzonych przez użytkownika.'''
        data = self.entry.get()
        creator = self.creator_entry.get()
        size = self.size_var.get()

        size_mapping = {"Mały": 1, "Średni": 2, "Duży": 3, "Bardzo duży": 4}
        qr_size = size_mapping.get(size, 1)

        if data:
            qr = qrcode.QRCode(
                version=qr_size,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color=self.qr_color, back_color=self.bg_color)

            # Zapisz tylko kod QR jako jpg
            qr_img_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "generated_qr.jpg")
            img.save(qr_img_path)

            temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            img.save(temp_img.name)

            script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
            history_file_path = os.path.join(script_path, "qr_history.txt")

            with open(history_file_path, "a") as file:
                file.write(f"Dane: {data}\n")
                file.write(f"Twórca kodu: {creator}\n")
                file.write(f"Data utworzenia: {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                file.write(f"Godzina utworzenia: {datetime.datetime.now().strftime('%H:%M:%S')}\n")
                file.write("\n")

            script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
            output_file_path = os.path.join(script_path, "generated_qr.pdf")

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Wygenerowany kod QR:", ln=True, align="L")
            pdf.cell(200, 10, txt=data, ln=True, align="L")
            pdf.cell(200, 10, txt=f"Twórca kodu: {creator}", ln=True, align="L")
            pdf.cell(200, 10, txt=f"Data utworzenia: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align="L")
            pdf.cell(200, 10, txt=f"Godzina utworzenia: {datetime.datetime.now().strftime('%H:%M:%S')}", ln=True, align="L")
            pdf.image(temp_img.name, x=10, y=100, w=100)
            pdf.output(output_file_path)

            temp_img.close()

            messagebox.showinfo("Sukces", f"Kod QR został wygenerowany i zapisany jako JPG: {qr_img_path}\n\nZapisano również jako PDF: {output_file_path}")
            self.root.destroy()
        else:
            messagebox.showerror("Błąd", "Proszę wprowadzić dane.")


    def cancel(self):
        '''Metoda obsługująca przycisk Anuluj.'''
        messagebox.showinfo("Zakończono", "Dziękujemy za skorzystanie z aplikacji.")
        self.root.destroy()

    def open_index_html(self):
        '''Metoda do otwierania pliku index.html w domyślnej przeglądarce.'''
        script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        index_html_path = os.path.join(script_path, "index.html")

        if os.path.exists(index_html_path):
            webbrowser.open(index_html_path)
        else:
            messagebox.showerror("Błąd", "Plik index.html nie został znaleziony.")

if __name__ == "__main__":
    generator = QRCodeGenerator()

