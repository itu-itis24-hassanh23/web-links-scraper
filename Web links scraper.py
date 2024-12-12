import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os

def extract_links(url, output_folder, output_filename, max_links):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)[:max_links]
        
        csv_data = [['Link Text', 'URL']]
        csv_data.extend([[link.text.strip(), urljoin(url, link['href'])] for link in links])
        
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            csv.writer(file).writerows(csv_data)
        
        return f"Links extracted and saved to '{output_path}'"
    except requests.RequestException as e:
        return f"An error occurred: {e}"

class LinkExtractorGUI:
    def __init__(self, master):
        self.master = master
        self.setup_ui()
        self.apply_neumorphic_style()

    def setup_ui(self):
        self.master.title("Web Links Scraper")
        self.master.geometry("400x500")

        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):
        self.url_label = ttk.Label(self.master, text="Enter URL:")
        self.url_entry = ttk.Entry(self.master, width=50)

        self.output_folder_label = ttk.Label(self.master, text="Output Folder:")
        self.output_folder_frame = ttk.Frame(self.master)
        self.output_folder_entry = ttk.Entry(self.output_folder_frame)
        self.browse_button = ttk.Button(self.output_folder_frame, text="Browse", command=self.browse_folder)

        self.filename_label = ttk.Label(self.master, text="Output Filename:")
        self.filename_entry = ttk.Entry(self.master, width=50)
        self.filename_entry.insert(0, "links.csv")

        self.max_links_label = ttk.Label(self.master, text="Max Links to Extract:")
        self.max_links_entry = ttk.Entry(self.master, width=10)
        self.max_links_entry.insert(0, "100")

        self.extract_button = ttk.Button(self.master, text="Extract Links", command=self.extract)

    def layout_widgets(self):
        for widget in (self.url_label, self.url_entry, self.output_folder_label, 
                       self.output_folder_frame, self.filename_label, self.filename_entry, 
                       self.max_links_label, self.max_links_entry, self.extract_button):
            widget.pack(pady=10, padx=20, fill='x')

        self.output_folder_entry.pack(side='left', expand=True, fill='x')
        self.browse_button.pack(side='right')

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.output_folder_entry.delete(0, tk.END)
        self.output_folder_entry.insert(0, folder_selected)

    def extract(self):
        url = self.url_entry.get()
        output_folder = self.output_folder_entry.get()
        output_filename = self.filename_entry.get()
        max_links = int(self.max_links_entry.get())

        if not all([url, output_folder, output_filename]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        result = extract_links(url, output_folder, output_filename, max_links)
        messagebox.showinfo("Result", result)


if __name__ == "__main__":
    root = tk.Tk()
    app = LinkExtractorGUI(root)
    root.mainloop()
