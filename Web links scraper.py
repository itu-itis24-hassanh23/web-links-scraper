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
        
        return f"Successfully extracted {len(links)} links to '{output_path}'"
    except Exception as e:
        return f"Error: {str(e)}"

class LinkExtractorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Web Links Scraper")
        self.master.geometry("500x450")
        self.master.resizable(False, False)
        self.setup_ui()
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TEntry', padding=5)

    def setup_ui(self):
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):
        self.url_label = ttk.Label(self.master, text="Website URL:")
        self.url_entry = ttk.Entry(self.master, width=50)

        self.output_folder_label = ttk.Label(self.master, text="Save Folder:")
        self.output_folder_frame = ttk.Frame(self.master)
        self.output_folder_entry = ttk.Entry(self.output_folder_frame)
        self.browse_button = ttk.Button(
            self.output_folder_frame, 
            text="Browse", 
            command=self.browse_folder
        )

        self.filename_label = ttk.Label(self.master, text="Filename:")
        self.filename_entry = ttk.Entry(self.master)
        self.filename_entry.insert(0, "links.csv")

        self.max_links_label = ttk.Label(self.master, text="Maximum Links:")
        self.max_links_entry = ttk.Entry(self.master, width=10)
        self.max_links_entry.insert(0, "100")

        self.extract_button = ttk.Button(
            self.master, 
            text="Extract Links", 
            command=self.extract,
            style='TButton'
        )

    def layout_widgets(self):
        self.url_label.pack(pady=(20, 5), padx=20, anchor='w')
        self.url_entry.pack(pady=5, padx=20, fill='x')

        self.output_folder_label.pack(pady=5, padx=20, anchor='w')
        self.output_folder_frame.pack(pady=5, padx=20, fill='x')
        self.output_folder_entry.pack(side='left', expand=True, fill='x')
        self.browse_button.pack(side='right')

        self.filename_label.pack(pady=5, padx=20, anchor='w')
        self.filename_entry.pack(pady=5, padx=20, fill='x')

        self.max_links_label.pack(pady=5, padx=20, anchor='w')
        self.max_links_entry.pack(pady=5, padx=20, anchor='w')

        self.extract_button.pack(pady=20, ipadx=10, ipady=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder_entry.delete(0, tk.END)
            self.output_folder_entry.insert(0, folder_selected)

    def validate_url(self, url):
        return url.startswith(('http://', 'https://'))

    def extract(self):
        url = self.url_entry.get().strip()
        output_folder = self.output_folder_entry.get().strip()
        output_filename = self.filename_entry.get().strip()

        if not all([url, output_folder, output_filename]):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not self.validate_url(url):
            messagebox.showerror("Error", "Invalid URL format. Must start with http:// or https://")
            return

        try:
            max_links = int(self.max_links_entry.get())
            if max_links <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number greater than 0")
            return

        try:
            result = extract_links(url, output_folder, output_filename, max_links)
            messagebox.showinfo("Success", result)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkExtractorGUI(root)
    root.mainloop()
