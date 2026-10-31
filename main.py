import customtkinter as ctk
import psutil
import threading
import time
import os
import sys
import ctypes
import winreg
from tkinter import filedialog, messagebox

# ==========================================
# CONFIGURACIÓN DE INTERFAZ Y MARCA DE AGUA
# ==========================================
ctk.set_appearance_mode("dark")  # Modo oscuro profesional
ctk.set_default_color_theme("blue")

# Marca de agua y firma del desarrollador
WATERMARK = "Miguel Desarrollador © 2026 | UCV Sistemas"
VERSION = "V1.0 - Zero Trust Edition"

class SecuritySuite(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Security Suite - {VERSION}")
        self.geometry("700x500")
        self.resizable(False, False)

        # Variables de estado
        self.watchdog_active = True
        self.bunker_status = ctk.StringVar(value="Desconocido")

        self.setup_ui()
        self.check_bunker_status()
        self.start_watchdog()

    def setup_ui(self):
        # Panel lateral (Menú)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🛡️ M-Security", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20, padx=20)

        # Botones de navegación (Visuales por ahora, controlan el scroll o vistas)
        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="Watchdog (CPU)", command=lambda: self.tabview.set("Watchdog"))
        self.btn_dashboard.pack(pady=10, padx=20)

        self.btn_bunker = ctk.CTkButton(self.sidebar_frame, text="Interruptor (Búnker)", command=lambda: self.tabview.set("Búnker"))
        self.btn_bunker.pack(pady=10, padx=20)

        self.btn_forense = ctk.CTkButton(self.sidebar_frame, text="Analizador Forense", command=lambda: self.tabview.set("Forense"))
        self.btn_forense.pack(pady=10, padx=20)

        # Marca de agua en el menú lateral
        self.watermark_label = ctk.CTkLabel(self.sidebar_frame, text=WATERMARK, font=ctk.CTkFont(size=10), text_color="gray")
        self.watermark_label.pack(side="bottom", pady=20)

        # Contenedor Central
        self.tabview = ctk.CTkTabview(self, width=480, height=480)
        self.tabview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tabview.add("Watchdog")
        self.tabview.add("Búnker")
        self.tabview.add("Forense")

        # --- PESTAÑA 1: WATCHDOG ---
        self.lbl_cpu_title = ctk.CTkLabel(self.tabview.tab("Watchdog"), text="Monitoreo Silencioso de Procesador", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_cpu_title.pack(pady=20)
        
        self.lbl_cpu_usage = ctk.CTkLabel(self.tabview.tab("Watchdog"), text="CPU: Calculando...", font=ctk.CTkFont(size=40))
        self.lbl_cpu_usage.pack(pady=30)
        
        self.lbl_cpu_alert = ctk.CTkLabel(self.tabview.tab("Watchdog"), text="Estado: Normal", text_color="green")
        self.lbl_cpu_alert.pack(pady=10)

        # --- PESTAÑA 2: BÚNKER ---
        self.lbl_bunker_title = ctk.CTkLabel(self.tabview.tab("Búnker"), text="Control de Windows Script Host", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_bunker_title.pack(pady=20)

        self.lbl_bunker_desc = ctk.CTkLabel(self.tabview.tab("Búnker"), text="Bloquea la ejecución de scripts .vbs (Malware Fileless)", text_color="gray")
        self.lbl_bunker_desc.pack(pady=5)

        self.lbl_bunker_status_display = ctk.CTkLabel(self.tabview.tab("Búnker"), textvariable=self.bunker_status, font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_bunker_status_display.pack(pady=20)

        self.btn_toggle_bunker = ctk.CTkButton(self.tabview.tab("Búnker"), text="Cambiar Estado de Búnker", command=self.toggle_bunker, fg_color="#8B0000", hover_color="#5C0000")
        self.btn_toggle_bunker.pack(pady=20)

        # --- PESTAÑA 3: FORENSE ---
        self.lbl_forense_title = ctk.CTkLabel(self.tabview.tab("Forense"), text="Laboratorio de Repacks", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_forense_title.pack(pady=20)
        
        self.btn_scan = ctk.CTkButton(self.tabview.tab("Forense"), text="Seleccionar Carpeta para Analizar", command=self.run_forensics)
        self.btn_scan.pack(pady=10)

        self.textbox_forense = ctk.CTkTextbox(self.tabview.tab("Forense"), width=400, height=250)
        self.textbox_forense.pack(pady=10)
        self.textbox_forense.insert("0.0", "Esperando directorio para analizar...\n")

    # ==========================================
    # MÓDULO 1: WATCHDOG (THREADING SEGURO)
    # ==========================================
    def start_watchdog(self):
        # Daemon=True asegura que el hilo muera si cierras la ventana
        self.thread = threading.Thread(target=self.monitor_cpu, daemon=True)
        self.thread.start()

    def monitor_cpu(self):
        while self.watchdog_active:
            try:
                cpu_percent = psutil.cpu_percent(interval=None)
                # Actualizar UI de forma segura
                self.after(0, self.update_cpu_ui, cpu_percent)
                
                # Regla de detección de mineros
                if cpu_percent > 80:
                    self.after(0, lambda: self.lbl_cpu_alert.configure(text="¡ALERTA! Consumo inusual detectado", text_color="red"))
                else:
                    self.after(0, lambda: self.lbl_cpu_alert.configure(text="Estado: Normal", text_color="green"))
                
                time.sleep(5) # Optimización: Descansa 5 segundos para no consumir recursos
            except Exception as e:
                pass

    def update_cpu_ui(self, percent):
        self.lbl_cpu_usage.configure(text=f"CPU: {percent}%")

    # ==========================================
    # MÓDULO 2: BÚNKER (REGISTRY EDITOR)
    # ==========================================
    def check_bunker_status(self):
        try:
            # Revisa la llave de Windows Script Host
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows Script Host\Settings", 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "Enabled")
            winreg.CloseKey(key)
            if value == 0:
                self.bunker_status.set("BÚNKER CERRADO (Seguro)")
                self.lbl_bunker_status_display.configure(text_color="green")
            else:
                self.bunker_status.set("BÚNKER ABIERTO (Vulnerable)")
                self.lbl_bunker_status_display.configure(text_color="red")
        except FileNotFoundError:
            # Si no existe, por defecto Windows lo permite
            self.bunker_status.set("BÚNKER ABIERTO (Vulnerable)")
            self.lbl_bunker_status_display.configure(text_color="red")

    def toggle_bunker(self):
        try:
            # Requiere Admin. Escribe en HKLM.
            key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows Script Host\Settings", 0, winreg.KEY_WRITE)
            if "CERRADO" in self.bunker_status.get():
                # Abrir Búnker (Permitir Scripts)
                winreg.SetValueEx(key, "Enabled", 0, winreg.REG_DWORD, 1)
            else:
                # Cerrar Búnker (Bloquear Scripts)
                winreg.SetValueEx(key, "Enabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            self.check_bunker_status()
            messagebox.showinfo("Éxito", "Política de Búnker actualizada. " + WATERMARK)
        except PermissionError:
            messagebox.showerror("Error de Privilegios", "Faltan permisos de Administrador. Reinicia la app como Admin.")
        except Exception as e:
            messagebox.showerror("Error", f"Error crítico: {str(e)}")

    # ==========================================
    # MÓDULO 3: FORENSE (STATIC SCANNER)
    # ==========================================
    def run_forensics(self):
        folder_selected = filedialog.askdirectory()
        if not folder_selected:
            return
        
        self.textbox_forense.delete("0.0", "end")
        self.textbox_forense.insert("0.0", f"Iniciando escaneo en:\n{folder_selected}\n\n")
        
        amenazas_encontradas = 0
        extensiones_peligrosas = ['.vbs', '.bat', '.cmd']
        
        for root, dirs, files in os.walk(folder_selected):
            for file in files:
                file_lower = file.lower()
                # Regla 1: Doble extensión (ej. setup.pdf.exe)
                if file_lower.endswith('.exe') and file_lower.count('.') > 1:
                    if file_lower.split('.')[-2] in ['pdf', 'png', 'jpg', 'meta']:
                        self.textbox_forense.insert("end", f"[!] PELIGRO (Doble Extensión): {file}\n")
                        amenazas_encontradas += 1
                
                # Regla 2: Scripts camuflados en texturas
                for ext in extensiones_peligrosas:
                    if file_lower.endswith(ext):
                        self.textbox_forense.insert("end", f"[!] ADVERTENCIA (Script Sospechoso): {file}\n")
                        amenazas_encontradas += 1

        self.textbox_forense.insert("end", f"\nEscaneo finalizado. Amenazas detectadas: {amenazas_encontradas}\n")
        self.textbox_forense.insert("end", f"Motor Forense - {WATERMARK}\n")

# ==========================================
# CONTROL DE ELEVACIÓN UAC (CRÍTICO)
# ==========================================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if is_admin():
        # Si ya es admin, corre la app
        app = SecuritySuite()
        app.mainloop()
    else:
        # Si no es admin, se auto-reinicia pidiendo permisos
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)