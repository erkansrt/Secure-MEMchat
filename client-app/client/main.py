import customtkinter as ctk
from tkinter import filedialog, messagebox
import socketio
import sys
import os

# Modül yollarını ayarla
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.crypto import DESManager
from client.api_client import APIClient

# Tema Ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secure MEMchat Client")
        self.geometry("1100x700")
        
        # Sunucu IP Sorma
        self.server_ip = ctk.CTkInputDialog(text="Sunucu IP Adresi (Orn: 192.168.1.35):", title="Bağlantı Ayarı").get_input()
        if not self.server_ip: 
            self.server_ip = "127.0.0.1" # Varsayılan localhost olsun
            
        self.server_url = f"http://{self.server_ip}:5000"

        self.sio = socketio.Client()
        self.api = APIClient(self.server_url)
        self.crypto = None
        self.username = None
        self.selected_image_path = None
        self.selected_recipient = None

        self.setup_socket_events()
        self.show_login_frame()
        
        # Pencere kapanırken bağlantıyı kes
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_socket_events(self):
        @self.sio.on('connect')
        def on_connect(): 
            print("Sunucuya bağlantı başarılı!")

        @self.sio.on('user_list_update')
        def on_user_list(data): 
            # Thread güvenliği için self.after kullanımı
            self.after(0, lambda: self.update_user_list_ui(data))

        @self.sio.on('receive_message')
        def on_message(data):
            # Thread güvenliği için self.after kullanımı
            self.after(0, lambda: self.handle_incoming_message(data))

    def handle_incoming_message(self, data):
        # Eğer sohbet ekranı henüz açılmadıysa işlem yapma
        if not hasattr(self, 'chat_display'):
            return

        try:
            msg = self.crypto.decrypt(data['message'])
            prefix = "[OFFLINE] " if data.get('is_offline') else ""
            
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"{prefix}{data['sender']}: {msg}\n")
            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")
        except Exception as e:
            print(f"Mesaj okuma hatası: {e}")

    def show_login_frame(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(self.login_frame, text="GÜVENLİ GİRİŞ", font=("Roboto", 24)).pack(pady=20, padx=40)
        
        self.entry_user = ctk.CTkEntry(self.login_frame, placeholder_text="Kullanıcı Adı")
        self.entry_user.pack(pady=10)
        self.entry_pass = ctk.CTkEntry(self.login_frame, placeholder_text="Şifre", show="*")
        self.entry_pass.pack(pady=10)
        
        self.lbl_img = ctk.CTkLabel(self.login_frame, text="")
        self.lbl_img.pack()
        ctk.CTkButton(self.login_frame, text="Resim Seç", command=self.select_image, fg_color="gray").pack(pady=5)
        
        ctk.CTkButton(self.login_frame, text="KAYIT OL", command=self.do_register, fg_color="#E67E22").pack(pady=5)
        ctk.CTkButton(self.login_frame, text="GİRİŞ YAP", command=self.do_login, fg_color="#27AE60").pack(pady=5)

    def select_image(self):
        fn = filedialog.askopenfilename(filetypes=[("PNG", "*.png")])
        if fn: 
            self.selected_image_path = fn
            self.lbl_img.configure(text=os.path.basename(fn))

    def do_register(self):
        # Girintiler düzeltildi
        username = self.entry_user.get()
        password = self.entry_pass.get()
        
        if not username or not password or not self.selected_image_path:
            messagebox.showwarning("Eksik Bilgi", "Lütfen kullanıcı adı, şifre girin ve bir resim seçin!")
            return
        
        res = self.api.register(username, password, self.selected_image_path)
        
        if res.get("status") == "success":
            messagebox.showinfo("Başarılı", res.get('message'))
        else:
            messagebox.showerror("Kayıt Hatası", res.get('message'))
    
    def do_login(self):
        u, p = self.entry_user.get(), self.entry_pass.get()
        if not u or not p: 
            messagebox.showwarning("Hata", "Kullanıcı adı ve şifre giriniz.")
            return
            
        self.crypto = DESManager(p)
        try:
            self.sio.connect(self.server_url)
            self.sio.emit('login', {'username': u})
            self.username = u
            self.login_frame.destroy()
            self.show_chat_ui()
        except Exception as e: 
            messagebox.showerror("Bağlantı Hatası", f"Sunucuya bağlanılamadı:\n{e}")

    def show_chat_ui(self):
        # Sol Menü
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(self.sidebar, text="KULLANICILAR", font=("Roboto", 18, "bold")).pack(pady=20)
        self.user_scroll = ctk.CTkScrollableFrame(self.sidebar)
        self.user_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Sağ Taraf
        self.chat_area = ctk.CTkFrame(self)
        self.chat_area.pack(side="right", fill="both", expand=True)
        self.chat_header = ctk.CTkLabel(self.chat_area, text="Sohbet Odası", font=("Roboto", 20), height=50, fg_color="#2c3e50")
        self.chat_header.pack(fill="x")
        self.chat_display = ctk.CTkTextbox(self.chat_area, state="disabled", font=("Consolas", 14))
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=20)
        
        input_frame = ctk.CTkFrame(self.chat_area, height=60)
        input_frame.pack(fill="x", padx=20, pady=20)
        self.msg_entry = ctk.CTkEntry(input_frame, placeholder_text="Mesajınızı yazın...")
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.msg_entry.bind("<Return>", lambda e: self.send_message())
        ctk.CTkButton(input_frame, text="GÖNDER", width=100, command=self.send_message).pack(side="right")

    def update_user_list_ui(self, data):
        for w in self.user_scroll.winfo_children(): w.destroy()
        
        all_users = data['users']
        online_users = data['online']

        for u in all_users:
            if u == self.username: continue
            
            is_online = u in online_users
            color = "#27AE60" if is_online else "gray"
            status_text = "Online" if is_online else "Offline"
            
            ctk.CTkButton(
                self.user_scroll, 
                text=f"{u}\n({status_text})", 
                fg_color=color, 
                command=lambda x=u: self.select_recipient(x)
            ).pack(pady=5, fill="x")

    def select_recipient(self, user):
        self.selected_recipient = user
        self.chat_header.configure(text=f"Sohbet: {user}")

    def send_message(self):
        msg = self.msg_entry.get()
        if not msg: return
        
        if not self.selected_recipient:
            messagebox.showwarning("Uyari", "Lutfen listeden mesaj göndereceğiniz kişiyi seçin.")
            return

        try:
            encrypted_msg = self.crypto.encrypt(msg)
            self.sio.emit('send_message', {
                'sender': self.username, 
                'receiver': self.selected_recipient, 
                'message': encrypted_msg
            })
            
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"Ben -> {self.selected_recipient}: {msg}\n")
            self.chat_display.configure(state="disabled")
            self.msg_entry.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Hata", f"Mesaj gönderilemedi: {e}")

    def on_close(self):
        self.sio.disconnect()
        self.destroy()

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()