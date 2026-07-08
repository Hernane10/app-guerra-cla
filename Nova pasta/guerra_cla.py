from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import urllib.request
import json
from datetime import datetime

# ---------------------- CONFIGURAÇÕES ----------------------
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVjYzQyYzNkLTcxZDYtNDFhOS1iYTY0LWVjZmMwYmEyYmQ0MCIsImlhdCI6MTc4MzQ3Mjg4NSwic3ViIjoiZGV2ZWxvcGVyLzYwZDE5NTdhLTc4YjUtNzc3Zi1mMzliLWFjYzJhMTkyMDU1OCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzcuMTQ5LjE2My4wIl0sInR5cGUiOiJjbGllbnQifV19.KZy3VF0-DQWJ_E2AKuM9jUhwfJDOE9m-mcU8bR9WCnVNic8sh8NCu4pWpoXVrjlwXZFSmf9Lo0YvKczrw-stmg"
TAG_CLAN = "#YLV9PJ0R"
tag_formatada = TAG_CLAN.replace("#", "%23")
BASE_URL = "https://api.clashroyale.com/v1/clans"

# Cores
COR_PRINCIPAL = get_color_from_hex("#2563EB")
COR_SUCESSO = get_color_from_hex("#16A34A")
COR_ERRO = get_color_from_hex("#DC2626")
COR_FUNDO = get_color_from_hex("#F8FAFC")
COR_TEXTO = get_color_from_hex("#1E293B")
# -----------------------------------------------------------

def requisitar(endpoint):
    """Função para buscar dados da API"""
    try:
        url = f"{BASE_URL}/{tag_formatada}/{endpoint}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {API_KEY}")
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=20) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"erro": str(e)}

def mostrar_mensagem(titulo, mensagem):
    """Exibe aviso em tela"""
    layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
    layout.add_widget(Label(text=mensagem, color=COR_TEXTO))
    btn = Button(text="Fechar", background_color=COR_PRINCIPAL, color=(1,1,1,1), size_hint=(1, 0.3))
    popup = Popup(title=titulo, content=layout, size_hint=(0.85, 0.45))
    btn.bind(on_press=popup.dismiss)
    layout.add_widget(btn)
    popup.open()

class TelaPrincipal(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.background_color = COR_FUNDO
        self.tab_background = COR_PRINCIPAL
        self.tab_color = (1,1,1,1)

        # Aba 1: Guerra Atual
        self.aba_atual = TabbedPanelItem(text="⚔️ Guerra Atual")
        self.montar_aba_atual()
        self.add_widget(self.aba_atual)

        # Aba 2: Guerras Anteriores
        self.aba_anteriores = TabbedPanelItem(text="📜 Histórico")
        self.montar_aba_anteriores()
        self.add_widget(self.aba_anteriores)

        self.carregar_atual()

    def montar_aba_atual(self):
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(12))

        self.btn_atualizar = Button(
            text="🔄 Atualizar Guerra",
            background_color=COR_SUCESSO,
            color=(1,1,1,1),
            size_hint=(1, None),
            height=dp(45)
        )
        self.btn_atualizar.bind(on_press=lambda x: self.carregar_atual())
        layout.add_widget(self.btn_atualizar)

        self.scroll_atual = ScrollView()
        self.grid_atual = GridLayout(cols=4, spacing=dp(8), size_hint_y=None)
        self.grid_atual.bind(minimum_height=self.grid_atual.setter('height'))
        self.scroll_atual.add_widget(self.grid_atual)
        layout.add_widget(self.scroll_atual)

        self.aba_atual.add_widget(layout)

    def carregar_atual(self):
        self.grid_atual.clear_widgets()
        dados = requisitar("currentriverrace")

        if "erro" in dados:
            mostrar_mensagem("Erro", "Verifique sua chave e IP da API!")
            return

        membros = dados.get("clan", {}).get("members", [])
        if not membros:
            mostrar_mensagem("Aviso", "Nenhuma guerra ativa no momento")
            return

        # Cabeçalho
        for texto in ["Membro", "Ataques", "Fama", "Status"]:
            self.grid_atual.add_widget(Label(text=texto, bold=True, color=COR_TEXTO, size_hint_y=None, height=dp(35)))

        # Linhas de dados
        for m in membros:
            ataques = m.get("attacks", 0)
            fama = m.get("fame", 0)
            status = "✅ Sim" if ataques > 0 else "❌ Não"

            self.grid_atual.add_widget(Label(text=m.get("name", ""), color=COR_TEXTO, size_hint_y=None, height=dp(35)))
            self.grid_atual.add_widget(Label(text=f"{ataques}/2", color=COR_TEXTO, size_hint_y=None, height=dp(35)))
            self.grid_atual.add_widget(Label(text=str(fama), color=COR_TEXTO, size_hint_y=None, height=dp(35)))
            self.grid_atual.add_widget(Label(text=status, color=COR_SUCESSO if ataques > 0 else COR_ERRO, size_hint_y=None, height=dp(35)))

    def montar_aba_anteriores(self):
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(12))

        self.btn_historico = Button(
            text="📋 Carregar Últimas Guerras",
            background_color=COR_PRINCIPAL,
            color=(1,1,1,1),
            size_hint=(1, None),
            height=dp(45)
        )
        self.btn_historico.bind(on_press=lambda x: self.carregar_historico())
        layout.add_widget(self.btn_historico)

        self.scroll_historico = ScrollView()
        self.grid_historico = GridLayout(cols=5, spacing=dp(8), size_hint_y=None)
        self.grid_historico.bind(minimum_height=self.grid_historico.setter('height'))
        self.scroll_historico.add_widget(self.grid_historico)
        layout.add_widget(self.scroll_historico)

        self.aba_anteriores.add_widget(layout)
        self.guerras = []

    def carregar_historico(self):
        self.grid_historico.clear_widgets()
        self.guerras = []
        dados = requisitar("riverracelog?limit=10")

        if "erro" in dados:
            mostrar_mensagem("Aviso", "Histórico não disponível para sua chave")
            return

        self.guerras = dados.get("items", [])
        if not self.guerras:
            mostrar_mensagem("Aviso", "Nenhuma guerra anterior encontrada")
            return

        # Cabeçalho
        for texto in ["Nº", "Data", "Posição", "Pontos", "Participação"]:
            self.grid_historico.add_widget(Label(text=texto, bold=True, color=COR_TEXTO, size_hint_y=None, height=dp(35)))

        # Linhas
        for idx, guerra in enumerate(self.guerras, 1):
            try:
                data = datetime.fromtimestamp(int(str(guerra["createdDate"])[:-3])).strftime("%d/%m/%Y")
                pos = guerra.get("clan", {}).get("finishPosition", "-")
                pontos = guerra.get("clan", {}).get("clanScore", 0)
                membros = guerra.get("clan", {}).get("members", [])
                perc = f"{int(sum(m.get('attacks',0) for m in membros)/(len(membros)*2)*100)}%" if membros else "-"

                self.grid_historico.add_widget(Label(text=str(idx), color=COR_TEXTO, size_hint_y=None, height=dp(35)))
                self.grid_historico.add_widget(Label(text=data, color=COR_TEXTO, size_hint_y=None, height=dp(35)))
                self.grid_historico.add_widget(Label(text=str(pos), color=COR_TEXTO, size_hint_y=None, height=dp(35)))
                self.grid_historico.add_widget(Label(text=str(pontos), color=COR_TEXTO, size_hint_y=None, height=dp(35)))
                self.grid_historico.add_widget(Label(text=perc, color=COR_TEXTO, size_hint_y=None, height=dp(35)))
            except:
                continue

class AppClashRoyale(App):
    def build(self):
        self.title = "Controle de Guerras CR"
        return TelaPrincipal()

if __name__ == "__main__":
    AppClashRoyale().run()