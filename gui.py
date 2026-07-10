import customtkinter as ctk
import threading
import main
print(main.__file__)
import tkinter as tk
import speech_recognition as sr
# -------------------------
# Theme
# -------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GojoGUI:

    def __init__(self):

        self.root = ctk.CTk()
        self.root.title("Gojo AI Assistant")
        self.root.geometry("1300x750")

        self.create_sidebar()    
        self.create_main_area()
        
        threading.Thread(
            target=self.voice_mode,
            daemon=True
        ).start()
    
    # -------------------------
    # Sidebar
    # -------------------------
    
    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self.root,
            width=220,
            corner_radius=0
        )

        self.sidebar.pack(side="left", fill="y")

        title = ctk.CTkLabel(
            self.sidebar,
            text="Gojo",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=(30, 5))

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Your AI Assistant"
        )

        subtitle.pack()

        ctk.CTkButton(
            self.sidebar,
            text="Home"
        ).pack(fill="x", padx=15, pady=10)

       

        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="Status: Ready"
        )

        self.status_label.pack(side="bottom", pady=80)

    # -------------------------
    # Main Area
    # -------------------------
    def create_main_area(self):

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # =========================
        # GOJO CORE PANEL
        # =========================
        gojo_frame = ctk.CTkFrame(
            self.main_frame,
            width=700,
            height=220,
            corner_radius=25,
            border_width=2,
            border_color="#4DA6FF"
      )
        gojo_frame.pack(pady=30)

        gojo_title = ctk.CTkLabel(
            gojo_frame,
            text="⚡ SATORU GOJO AI ⚡",
            font=("Arial", 30, "bold"),
            text_color="#66CCFF"
        )
        gojo_title.pack(pady=(25, 10))
  
        gojo_subtitle = ctk.CTkLabel(
            gojo_frame,
            text="∞ Limitless Intelligence System ∞",
            font=("Arial", 18),
            text_color="white"
        )
        gojo_subtitle.pack()

        status_core = ctk.CTkLabel(
              gojo_frame,
              text="Blue Eyes Online • Infinity Active",
              font=("Arial", 16),
              text_color="#7FDBFF"
        )
        status_core.pack(pady=15)

    # Main Title
        self.jarvis_text = ctk.CTkLabel(
            self.main_frame,
            text="GOJO CORE ONLINE",
            font=("Arial", 24, "bold"),
            text_color="#66CCFF"
        )
        self.jarvis_text.pack(pady=10)

    # Chat Box
        self.chatbox = ctk.CTkTextbox(
            self.main_frame,
            width=950,
            height=330,
            corner_radius=15,
            font=("Consolas", 15)
        )
        self.chatbox.pack(pady=20)

        self.chatbox.insert(
            "end",
            "⚡ GOJO SYSTEM INITIALIZED ⚡\n\n"
        )

    # Bottom Frame
        bottom_frame = ctk.CTkFrame(self.main_frame)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        self.command_entry = ctk.CTkEntry(
            bottom_frame,
            placeholder_text="Type your command..."
        )
        self.command_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        send_btn = ctk.CTkButton(
            bottom_frame,
            text="⚡ Send",
            command=self.send_command,
            height=40,
            corner_radius=12
        )
        send_btn.pack(side="left", padx=5)

        mic_btn = ctk.CTkButton(
           bottom_frame,
           text="🎤",
           width=60,
           height=40,
           corner_radius=12,
           command=self.listen_voice
        )
        mic_btn.pack(side="left", padx=5)


 
# -------------------------
# Execute Command
# -------------------------
    def send_command(self):

        cmd = self.command_entry.get().strip()

        if not cmd:
            return

        self.chatbox.insert(
            "end",
            f"\nYou: {cmd}\n"
        )

        self.command_entry.delete(0, "end")

        threading.Thread(
            target=self.run_command,
            args=(cmd,),
            daemon=True
        ).start()

    def run_command(self, cmd):

        self.status_label.configure(
            text="Status: Processing..."
        )

        try:

            response = main.process_text_command(cmd)

            self.chatbox.insert(
                "end",
                f"Gojo: {response}\n"
            )

        except Exception as e:

            self.chatbox.insert(
                "end",
                f"Error: {e}\n"
            )

        self.status_label.configure(
            text="Status: Ready"
        )
    def voice_mode(self):

        r = sr.Recognizer()

        while True:

            try:

               with sr.Microphone() as source:

                    audio = r.listen(
                       source,
                       timeout=2,
                       phrase_time_limit=2
                    )

               word = r.recognize_google(audio)

               if word.lower() == "gojo":

                   self.root.after(
                       0,
                       lambda: self.chatbox.insert(
                           "end",
                           "\n[Wake Word Detected: GOJO]\n"
                        )
                   )

                   main.speak("haan boliye")

                   with sr.Microphone() as source:

                       audio = r.listen(source)

                   command = r.recognize_google(audio)

                   self.root.after(
                       0,
                       lambda c=command: self.chatbox.insert(
                           "end",
                           f"\nYou (Voice): {c}\n"
                       )
                   )

                   response = main.process_text_command(command)

                   self.root.after(
                       0,
                       lambda r=response: self.chatbox.insert(
                           "end",
                           f"\nGojo: {r}\n\n"
                       )
                   )

            except:
                pass
    
    def listen_voice(self):

        r = sr.Recognizer()

        try:
           with sr.Microphone() as source:
               self.chatbox.insert("end", "\nListening...\n")
               audio = r.listen(source)

           command = r.recognize_google(audio)

           self.chatbox.insert(
               "end",
               f"\nYou (Voice): {command}\n"
           )

           threading.Thread(
               target=self.run_command,
               args=(command,),
               daemon=True
           ).start()

        except Exception as e:
            self.chatbox.insert(
                "end",
                f"\nError: {e}\n"
            )

        
# -------------------------
# Run GUI
# -------------------------
    def run(self):
        self.root.mainloop()  

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app = GojoGUI()
    app.run()
    