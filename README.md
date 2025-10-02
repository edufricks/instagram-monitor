# 📊 Instagram Viral Posts Monitor

Ferramenta em **Python + Streamlit** para analisar os **posts mais virais** de qualquer perfil público do Instagram, usando os cookies da sua conta.

🚀 Permite:
- Upload do `cookies.json`
- Coletar posts de perfis públicos
- Ordenação automática por **engajamento (likes + comentários)**
- Visualização em gráficos interativos (Top posts, evolução temporal, correlação likes x comentários)
- Download dos resultados em **CSV**

---

## ⚙️ Como usar

### 🔹 1. Exportar seus cookies
Você precisa estar logado no Instagram e exportar seus cookies.  
Sugestão: usar a extensão [**Get cookies.txt**](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid) para Chrome/Edge.  

- Acesse [instagram.com](https://instagram.com) logado na sua conta  
- Exporte os cookies  
- Renomeie o arquivo para `cookies.json`

⚠️ Importante: use uma conta normal (não corporativa), para reduzir chance de bloqueio.

---

### 🔹 2. Rodar localmente
Clone este repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/instagram-monitor.git
cd instagram-monitor
pip install -r requirements.txt
