"""
💡 Генератор идей — стильная веб-версия на Streamlit (дизайн 2026)

Запуск:
    pip install -r requirements.txt
    streamlit run app.py
"""

import random
import streamlit as st

# ── 1. Настройки страницы (первый вызов st.*) ───────────────────────────────
st.set_page_config(
    page_title="Генератор идей",
    page_icon="💡",
    layout="centered",
)

# ── 2. Данные: словарь {категория: список идей} ─────────────────────────────
IDEAS = {
    "💻 IT-проекты": [
        "Трекер привычек с геймификацией",
        "Бот-напоминалка для полива растений",
        "Конвертер валют с офлайн-курсами",
        "Генератор паролей с проверкой надёжности",
        "Одностраничный сайт-портфолио",
        "Telegram-бот с ежедневным фактом дня",
    ],
    "✍️ Тексты": [
        "Серия постов «одна ошибка новичка в день»",
        "Разбор своего любимого фильма",
        "Дневник обучения программированию",
        "Гайд «с чего начать, если страшно»",
        "Подборка 10 бесплатных инструментов",
        "Рецензия на книгу, изменившую мышление",
    ],
    "🎬 Видео": [
        "Повторить проект из туториала без подсказок",
        "Челлендж: сделать сайт за 1 час",
        "Разбор чужих проектов на GitHub",
        "Видео «день из жизни новичка-программиста»",
        "Сравнение 3 языков на одной задаче",
        "Таймлапс сборки ПК от распаковки до запуска",
    ],
    "🏋️ Хобби": [
        "Пробежать новый маршрут в своём городе",
        "Приготовить блюдо из незнакомой кухни",
        "Собрать плейлист на 30 дней",
        "Научиться жонглировать тремя мячами",
        "Сделать альбом с фото за последний год",
        "Вырастить растение из косточки авокадо",
    ],
}

# Эмодзи, акцентный цвет и описание для каждой категории
META = {
    "💻 IT-проекты": ("💻", "#7c5cff", "код, пет-проекты, автоматизация"),
    "✍️ Тексты": ("✍️", "#22d3ee", "посты, гайды, дневники"),
    "🎬 Видео": ("🎬", "#ff5cae", "ролики, стримы, челленджи"),
    "🏋️ Хобби": ("🏋️", "#4ade80", "спорт, еда, маленькие радости"),
}

# ── 3. Состояние между перезапусками скрипта ────────────────────────────────
st.session_state.setdefault("idea", None)
st.session_state.setdefault("idea_category", None)
st.session_state.setdefault("history", [])
st.session_state.setdefault("count", 0)

# ── 4. Стили (дизайн 2026: тёмная тема, стекло, неон, анимации) ─────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap');

:root{
  --card: rgba(255,255,255,.06);
  --stroke: rgba(255,255,255,.13);
  --text: #eaeaf5;
  --muted: #9aa0b5;
  --p1: #7c5cff;
  --p2: #22d3ee;
  --p3: #ff5cae;
}

html, body, [class*="css"]{ font-family:'Inter', sans-serif; }

.stApp{
  background:
    radial-gradient(1200px 600px at 8% -10%, rgba(124,92,255,.35), transparent 60%),
    radial-gradient(1000px 600px at 95% 0%, rgba(34,211,238,.28), transparent 55%),
    radial-gradient(900px 700px at 50% 120%, rgba(255,92,174,.22), transparent 60%),
    #070711;
  background-attachment: fixed;
}
header[data-testid="stHeader"]{ background:transparent; }
[data-testid="stAppDeployButton"], [data-testid="stToolbar"], [data-testid="stStatusWidget"]{ display:none !important; }
#MainMenu, footer{ visibility:hidden; }

/* ── Плавающие неоновые пятна (анимация фона) ── */
.aurora{ position:fixed; inset:0; z-index:0; overflow:hidden; pointer-events:none; }
.aurora span{ position:absolute; border-radius:50%; filter:blur(90px); opacity:.5;
  animation:float 20s ease-in-out infinite; }
.aurora span:nth-child(1){ width:520px; height:520px; background:var(--p1); top:-140px; left:-90px; }
.aurora span:nth-child(2){ width:460px; height:460px; background:var(--p2); top:8%; right:-130px; animation-delay:-7s; }
.aurora span:nth-child(3){ width:500px; height:500px; background:var(--p3); bottom:-180px; left:30%; animation-delay:-13s; }
@keyframes float{
  0%,100%{ transform:translate(0,0) scale(1); }
  33%{ transform:translate(60px,-40px) scale(1.12); }
  66%{ transform:translate(-50px,35px) scale(.94); }
}

/* ── Шапка ── */
.hero{ position:relative; z-index:1; text-align:center; padding:20px 0 8px; animation:rise .8s ease both; }
.hero-badge{ display:inline-block; padding:7px 16px; border-radius:999px; border:1px solid var(--stroke);
  background:linear-gradient(90deg, rgba(124,92,255,.20), rgba(34,211,238,.20));
  font-size:11px; letter-spacing:3px; text-transform:uppercase; color:#cfd3ea; }
.hero h1{ font-family:'Space Grotesk', sans-serif; font-size:clamp(34px,6vw,60px);
  margin:16px 0 0; color:#fff; font-weight:700; letter-spacing:-1.5px; line-height:1.02; }
.grad{ background:linear-gradient(90deg,var(--p1),var(--p2),var(--p3));
  -webkit-background-clip:text; background-clip:text; color:transparent;
  background-size:200% auto; animation:shimmer 6s linear infinite; }
@keyframes shimmer{ to{ background-position:200% center; } }
.hero p{ color:var(--muted); font-size:17px; margin:16px auto 0; max-width:560px; }
@keyframes rise{ from{ opacity:0; transform:translateY(20px); } to{ opacity:1; transform:none; } }

/* ── Бенто-статистика ── */
.stats{ position:relative; z-index:1; display:grid; grid-template-columns:repeat(3,1fr);
  gap:14px; margin:26px 0 8px; }
.stat{ padding:18px 16px; border-radius:20px; border:1px solid var(--stroke); text-align:center;
  background:linear-gradient(160deg, rgba(255,255,255,.09), rgba(255,255,255,.02));
  backdrop-filter:blur(18px); transition:transform .25s, border-color .25s; }
.stat:hover{ transform:translateY(-4px); border-color:rgba(124,92,255,.6); }
.stat-num{ font-family:'Space Grotesk', sans-serif; font-size:30px; font-weight:700; color:#fff; }
.stat-label{ color:var(--muted); font-size:12px; letter-spacing:1px; text-transform:uppercase; margin-top:4px; }

/* ── Кнопки ── */
div[data-testid="stButton"] button, div[data-testid^="stBaseButton"]{
  width:100%; border:none; border-radius:16px; padding:15px 20px; font-weight:700; font-size:16px;
  color:#fff; background:linear-gradient(120deg,var(--p1),var(--p2));
  box-shadow:0 12px 32px rgba(124,92,255,.45);
  transition:transform .2s, box-shadow .2s, filter .2s;
}
div[data-testid="stButton"] button:hover{
  transform:translateY(-2px) scale(1.015); filter:brightness(1.08);
  box-shadow:0 16px 44px rgba(34,211,238,.55);
}
div[data-testid="stButton"] button:active{ transform:scale(.985); }
div[data-testid="stBaseButton-secondary"]{
  background:rgba(255,255,255,.06) !important; box-shadow:none !important;
  border:1px solid var(--stroke) !important;
}

/* ── Карточка идеи ── */
.idea-card{ position:relative; z-index:1; margin-top:24px; padding:36px 32px; border-radius:28px;
  overflow:hidden; border:1px solid var(--stroke);
  background:linear-gradient(160deg, rgba(255,255,255,.11), rgba(255,255,255,.03));
  backdrop-filter:blur(22px); box-shadow:0 28px 70px rgba(0,0,0,.5);
  animation:pop .6s cubic-bezier(.2,.9,.3,1.35) both; }
.idea-card::before{ content:""; position:absolute; inset:0;
  background:linear-gradient(115deg, transparent 30%, rgba(255,255,255,.14) 50%, transparent 70%);
  transform:translateX(-130%); animation:sweep 2.4s ease .35s; }
@keyframes sweep{ to{ transform:translateX(130%); } }
@keyframes pop{ from{ opacity:0; transform:translateY(26px) scale(.96); } to{ opacity:1; transform:none; } }
.idea-emoji{ font-size:54px; line-height:1; animation:floaty 3.4s ease-in-out infinite; }
@keyframes floaty{ 0%,100%{ transform:translateY(0) rotate(-4deg); } 50%{ transform:translateY(-10px) rotate(4deg); } }
.cat-chip{ display:inline-block; margin-top:18px; padding:6px 14px; border-radius:999px;
  font-size:12px; letter-spacing:1.5px; text-transform:uppercase; color:#fff;
  border:1px solid var(--stroke); }
.idea-text{ font-family:'Space Grotesk', sans-serif; color:#fff; font-weight:700;
  font-size:clamp(24px,3.4vw,38px); line-height:1.16; margin:14px 0 4px; }

/* ── Пустое состояние ── */
.empty{ position:relative; z-index:1; text-align:center; margin-top:24px; padding:44px 20px;
  border-radius:28px; border:1px dashed var(--stroke); background:rgba(255,255,255,.03); }
.empty .dice{ font-size:60px; display:inline-block; animation:floaty 3s ease-in-out infinite; }
.empty p{ color:var(--muted); margin-top:12px; font-size:16px; }

/* ── История ── */
.hist-item{ display:flex; gap:12px; align-items:flex-start; padding:12px 14px; margin-bottom:8px;
  border-radius:14px; border:1px solid var(--stroke); background:rgba(255,255,255,.04);
  animation:rise .45s ease both; }
.hist-num{ font-family:'Space Grotesk', sans-serif; font-weight:700; color:var(--p2); min-width:22px; }
.hist-text{ color:var(--text); }
.hist-cat{ color:var(--muted); font-size:12px; margin-top:2px; }

.footer{ position:relative; z-index:1; text-align:center; color:var(--muted);
  font-size:13px; margin:34px 0 10px; opacity:.8; }
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
st.markdown('<div class="aurora"><span></span><span></span><span></span></div>', unsafe_allow_html=True)

# ── 5. Шапка ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
      <div class="hero-badge">✨ генератор идей • 2026</div>
      <h1>Поймай свою <span class="grad">идею</span></h1>
      <p>Выбери категорию и нажми кнопку — получишь случайную идею.
      Нажимай снова, пока не найдёшь ту самую 💫</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── 6. Бенто-статистика ─────────────────────────────────────────────────────
total_ideas = sum(len(v) for v in IDEAS.values())
st.markdown(
    f"""
    <div class="stats">
      <div class="stat"><div class="stat-num">{len(IDEAS)}</div><div class="stat-label">категорий</div></div>
      <div class="stat"><div class="stat-num">{total_ideas}</div><div class="stat-label">идей в базе</div></div>
      <div class="stat"><div class="stat-num">{st.session_state.count}</div><div class="stat-label">поймано</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── 7. Выбор категории ──────────────────────────────────────────────────────
categories = list(IDEAS.keys())

# Современный «сегментный» переключатель; при отсутствии — обычный selectbox.
try:
    category = st.segmented_control(
        "Категория",
        options=categories,
        default=categories[0],
        label_visibility="collapsed",
        key="chosen_cat",
    )
    category = category or categories[0]
except AttributeError:
    category = st.selectbox("Категория", categories, label_visibility="collapsed", key="chosen_cat")

emoji, accent, desc = META[category]
st.markdown(
    f'<div style="position:relative;z-index:1;text-align:center;color:#9aa0b5;'
    f'margin:10px 0 16px;font-size:14px;">{emoji} <b style="color:#cfd3ea">{desc}</b></div>',
    unsafe_allow_html=True,
)

# ── 8. Колбэки ──────────────────────────────────────────────────────────────
# Колбэк выполняется ДО перерисовки скрипта, поэтому счётчик и статистика
# вверху страницы успевают обновиться в том же кадре (нет «отставания на 1»).
def new_idea():
    cat = st.session_state.get("chosen_cat", categories[0])
    idea = random.choice(IDEAS[cat])               # случайная идея выбранной категории
    st.session_state.idea = idea
    st.session_state.idea_category = cat
    st.session_state.history.append((cat, idea))
    st.session_state.count += 1
    st.session_state.celebrate = True

def reset():
    st.session_state.idea = None
    st.session_state.idea_category = None
    st.session_state.history = []
    st.session_state.count = 0

st.session_state.setdefault("celebrate", False)

# ── 9. Кнопки ───────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.button("🎲 Сгенерировать идею", type="primary", use_container_width=True, on_click=new_idea)
with col2:
    st.button("🧹", use_container_width=True, on_click=reset)

if st.session_state.celebrate:                     # праздничная анимация
    st.balloons()
    st.session_state.celebrate = False

# ── 10. Показ результата ────────────────────────────────────────────────────
if st.session_state.idea:
    cat = st.session_state.idea_category
    cat_emoji, cat_accent, _ = META[cat]
    st.markdown(
        f"""
        <div class="idea-card">
          <div class="idea-emoji">{cat_emoji}</div>
          <div class="cat-chip" style="background:linear-gradient(90deg,{cat_accent}55,transparent);">
            {cat}
          </div>
          <div class="idea-text">{st.session_state.idea}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="empty">
          <div class="dice">🎲</div>
          <p>Пока пусто — нажми «Сгенерировать идею»</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── 11. История ─────────────────────────────────────────────────────────────
if st.session_state.history:
    with st.expander(f"📜 История идей — {len(st.session_state.history)}"):
        items = [
            f'<div class="hist-item"><div class="hist-num">{i}</div>'
            f'<div><div class="hist-text">{text}</div>'
            f'<div class="hist-cat">{cat}</div></div></div>'
            for i, (cat, text) in enumerate(reversed(st.session_state.history), start=1)
        ]
        st.markdown("".join(items), unsafe_allow_html=True)

st.markdown(
    '<div class="footer">Сделано на Python + Streamlit · дизайн 2026 💜</div>',
    unsafe_allow_html=True,
)
