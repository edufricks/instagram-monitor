import streamlit as st
import requests
import json
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIGURAÇÕES GERAIS -----------------
st.set_page_config(
    page_title="Instagram Viral Posts Monitor",
    layout="centered",
    initial_sidebar_state="auto"
)

HEADERS = {
    "User-Agent": "Instagram 219.0.0.12.117 Android",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "X-IG-App-ID": "936619743392459"
}

# ---------------- FUNÇÕES -----------------
def carregar_cookies(uploaded_file):
    try:
        cookies_raw = json.load(uploaded_file)
        cookies_dict = {}
        if isinstance(cookies_raw, list):
            for c in cookies_raw:
                if "name" in c and "value" in c:
                    cookies_dict[c["name"]] = c["value"]
        elif isinstance(cookies_raw, dict):
            cookies_dict = cookies_raw
        return cookies_dict
    except Exception as e:
        st.error(f"Erro ao carregar cookies: {e}")
        return None

def get_user_id(username, cookies):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    r = requests.get(url, headers=HEADERS, cookies=cookies)
    if r.status_code == 200:
        data = r.json()
        return data["data"]["user"]["id"], data["data"]["user"]["edge_followed_by"]["count"]
    else:
        return None, None

def coletar_posts(user_id, limite, cookies):
    url_base = f"https://i.instagram.com/api/v1/feed/user/{user_id}/"
    posts = []
    max_id = None

    while len(posts) < limite:
        params = {"count": 12}
        if max_id:
            params["max_id"] = max_id

        r = requests.get(url_base, headers=HEADERS, cookies=cookies, params=params)
        if r.status_code != 200:
            st.warning(f"Erro na requisição: {r.status_code}")
            break

        data = r.json()
        items = data.get("items", [])
        for item in items:
            post = {
                "id": item.get("id"),
                "link": f"https://www.instagram.com/p/{item['code']}/" if "code" in item else None,
                "likes": item.get("like_count", 0),
                "comments": item.get("comment_count", 0),
                "media_type": item.get("media_type"),
                "caption": item.get("caption", {}).get("text") if item.get("caption") else "",
                "timestamp": pd.to_datetime(item.get("taken_at"), unit="s")
            }
            posts.append(post)
            if len(posts) >= limite:
                break

        max_id = data.get("next_max_id")
        if not max_id:
            break

        time.sleep(random.uniform(2, 4))  # atraso aleatório para imitar comportamento humano

    return posts[:limite]

# ---------------- INTERFACE STREAMLIT -----------------
st.title("📊 Instagram Viral Posts Monitor")
st.write("Analise os **posts mais virais** de um perfil público no Instagram. Faça upload do seu `cookies.json` exportado do navegador.")

uploaded_file = st.file_uploader("📂 Faça upload do cookies.json", type=["json"])
usuario = st.text_input("🔎 Digite o @ do perfil (sem @):")
limite = st.number_input("📌 Quantos posts deseja analisar?", min_value=10, max_value=500, value=50, step=10)

if st.button("🚀 Analisar perfil") and uploaded_file and usuario:
    cookies = carregar_cookies(uploaded_file)
    if not cookies:
        st.error("Cookies inválidos.")
    else:
        user_id, seguidores = get_user_id(usuario, cookies)
        if not user_id:
            st.error("Não consegui obter informações do perfil. Verifique se está público e se os cookies são válidos.")
        else:
            st.success(f"[OK] Perfil: {usuario} | Seguidores: {seguidores:,}")
            posts = coletar_posts(user_id, limite, cookies)

            if not posts:
                st.warning("Nenhum post coletado.")
            else:
                df = pd.DataFrame(posts)
                df["engajamento"] = df["likes"] + df["comments"]
                df = df.sort_values("engajamento", ascending=False)

                # ---------------- RESULTADOS -----------------
                st.subheader("🔝 Posts mais virais")
                st.dataframe(df[["link", "likes", "comments", "engajamento", "caption"]])

                # ---------------- GRÁFICOS -----------------
                st.subheader("📈 Análises gráficas")

                # Engajamento por post
                fig, ax = plt.subplots()
                df.head(20).plot(kind="bar", x="link", y="engajamento", ax=ax, legend=False)
                plt.xticks(rotation=90)
                plt.title("Top 20 posts por engajamento")
                st.pyplot(fig)

                # Evolução temporal
                fig, ax = plt.subplots()
                df.sort_values("timestamp").plot(x="timestamp", y="engajamento", ax=ax, marker="o")
                plt.title("Evolução temporal do engajamento")
                st.pyplot(fig)

                # Likes vs Comentários
                fig, ax = plt.subplots()
                ax.scatter(df["likes"], df["comments"], alpha=0.6)
                ax.set_xlabel("Likes")
                ax.set_ylabel("Comentários")
                ax.set_title("Correlação Likes x Comentários")
                st.pyplot(fig)

                # ---------------- EXPORTAÇÃO -----------------
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Baixar CSV", data=csv, file_name=f"{usuario}_viral_posts.csv", mime="text/csv")
