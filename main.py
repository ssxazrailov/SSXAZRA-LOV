import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock

# Arka plan ve temel renk ayarları
Window.clearcolor = (0.05, 0.05, 0.08, 1)

MODES = {
    "Cyber & Security": "Sen SSXAZRAİLOV AI Siber Güvenlik modusun. Zafiyet analizi, kod denetimi ve güvenlik konularında uzmansın.",
    "Dev & Terminal": "Sen SSXAZRAİLOV AI Yazılım ve Terminal modusun. Linux, Python, Termux ve kodlama konularında uzmansın.",
    "Gaming & Logic": "Sen SSXAZRAİLOV AI Oyun modusun. Oyun mekanikleri, kurgu ve sistem mantıkları üreten bir uzmansın.",
    "Creative & Media": "Sen SSXAZRAİLOV AI Medya modusun. Kreatif içerik, medya kurguları ve fikir üretme konusunda uzmansın."
}

class SSXAZRAILOVApp(App):
    def build(self):
        self.title = "SSXAZRAİLOV"
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Başlık Paneli
        header = Label(
            text="[b]SSXAZRAİLOV AI[/b]", 
            markup=True, 
            font_size='24sp', 
            size_hint_y=None, 
            height=50,
            color=(0, 0.8, 1, 1)
        )
        main_layout.add_widget(header)
        
        # Mod Seçim Menüsü
        self.spinner = Spinner(
            text='Cyber & Security',
            values=list(MODES.keys()),
            size_hint_y=None,
            height=45,
            background_color=(0.1, 0.2, 0.4, 1)
        )
        main_layout.add_widget(self.spinner)
        
        # Yanıt Ekranı (Scroll Edilebilir)
        scroll = ScrollView(size_hint=(1, 1))
        self.chat_label = Label(
            text="[color=808080]SSXAZRAİLOV AI Sistemine Hoş Geldiniz. Bir soru yazın ve Gönder'e basın...[/color]\n",
            markup=True,
            font_size='15sp',
            size_hint_y=None,
            valign='top',
            halign='left'
        )
        self.chat_label.bind(size=self.update_label_size)
        scroll.add_widget(self.chat_label)
        main_layout.add_widget(scroll)
        
        # Girdi Alanı ve Buton
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        
        self.user_input = TextInput(
            hint_text='Komut veya sorunuzu yazın...',
            multiline=False,
            background_color=(0.15, 0.15, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.user_input.bind(on_text_validate=self.send_message)
        
        send_btn = Button(
            text='GÖNDER',
            size_hint_x=None,
            width=100,
            background_color=(0, 0.6, 0.9, 1)
        )
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_btn)
        
        main_layout.add_widget(input_layout)
        
        return main_layout

    def update_label_size(self, instance, value):
        self.chat_label.text_size = (self.chat_label.width, None)
        self.chat_label.height = self.chat_label.texture_size[1]

    def send_message(self, instance):
        query = self.user_input.text.strip()
        if not query:
            return
            
        selected_mode = self.spinner.text
        sys_prompt = MODES[selected_mode]
        
        self.chat_label.text += f"\n[color=00ffcc][b]Siz:[/b] {query}[/color]\n"
        self.user_input.text = ""
        
        self.chat_label.text += "[color=ffcc00][i]SSXAZRAİLOV düşünüyor...[/i][/color]\n"
        
        Clock.schedule_once(lambda dt: self.fetch_ai_response(sys_prompt, query))

    def fetch_ai_response(self, system_prompt, user_query):
        try:
            url = "https://text.pollinations.ai/"
            response = requests.post(
                url, 
                json={
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ]
                },
                timeout=15
            )
            
            if response.status_code == 200:
                reply = response.text
            else:
                reply = f"Hata Oluştu (Kod: {response.status_code})"
        except Exception as e:
            reply = f"Bağlantı Hatası: {str(e)}"
            
        lines = self.chat_label.text.split("\n")
        if lines and "SSXAZRAİLOV düşünüyor..." in lines[-2]:
            lines.pop(-2)
        self.chat_label.text = "\n".join(lines)
        
        self.chat_label.text += f"[color=ffffff][b]SSXAZRAİLOV ({self.spinner.text}):[/b]\n{reply}[/color]\n"

if __name__ == '__main__':
    SSXAZRAILOVApp().run()
          
