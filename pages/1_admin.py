import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="관리자 페이지",
    page_icon="🔧",
    layout="wide",
)

DATA_PATH = Path(__file__).parent.parent / "knowledge_base.json"

# -----------------------------
# 데이터 로드/저장
# -----------------------------
def load_data():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "manuals": {},
        "promotions": [],
        "last_updated": "",
        "updated_by": ""
    }

def save_data(data):
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data["updated_by"] = "관리자"
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# -----------------------------
# UI
# -----------------------------
st.title("🔧 관리자 페이지")
st.page_link("app.py", label="🏠 홈페이지 이동")

# -----------------------------
# 매뉴얼 관리
# -----------------------------
st.subheader("📘 PDA 매뉴얼 관리")

sections = list(data["manuals"].keys())

if sections:
    selected = st.selectbox("섹션 선택", sections)
    manual = data["manuals"][selected]

    title = st.text_input("제목", value=manual.get("title", ""))
    content = st.text_area("내용", value=manual.get("content", ""), height=200)

    if st.button("💾 저장"):
        data["manuals"][selected]["title"] = title
        data["manuals"][selected]["content"] = content
        save_data(data)
        st.success("저장 완료!")
        st.rerun()
else:
    st.warning("매뉴얼 데이터가 없습니다.")

# -----------------------------
# 새 섹션 추가
# -----------------------------
st.markdown("---")
st.subheader("➕ 새 섹션 추가")

new_section = st.text_input("새 섹션 이름")

if st.button("섹션 추가"):
    if new_section:
        data["manuals"][new_section] = {
            "title": new_section,
            "content": "",
            "faq": []
        }
        save_data(data)
        st.success("추가 완료!")
        st.rerun()

# -----------------------------
# 프로모션 관리
# -----------------------------
st.markdown("---")
st.subheader("🎁 프로모션 관리")

promo_name = st.text_input("프로모션명")
promo_rule = st.text_area("내용")

if st.button("프로모션 추가"):
    if promo_name:
        data["promotions"].append({
            "name": promo_name,
            "period": "",
            "rule": promo_rule,
            "updated_at": datetime.now().strftime("%Y-%m-%d")
        })
        save_data(data)
        st.success("프로모션 추가 완료!")
        st.rerun()
