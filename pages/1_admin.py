import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="관리자 페이지",
    page_icon="🔧",
    layout="wide",
)

DATA_PATH = Path(__file__).parent.parent / "knowledge_base.json"

# -----------------------------
# 기본 데이터
# -----------------------------
DEFAULT_DATA = {
    "manuals": {
        "① 개설 및 입출금": {
            "title": "개설 및 입출금",
            "content": "계좌 개설 및 입출금 처리 기준",
            "faq": []
        },
        "② 상품등록": {
            "title": "상품등록",
            "content": "상품 등록 및 수정 방법",
            "faq": []
        },
        "③ 판매보조": {
            "title": "판매보조",
            "content": "판매 보조 기능 안내",
            "faq": []
        },
        "④ 거래호출": {
            "title": "거래호출",
            "content": "거래 조회 및 호출 방법",
            "faq": []
        },
        "⑤ 결제형태별 거래": {
            "title": "결제형태별 거래",
            "content": "카드/간편결제/복합결제",
            "faq": []
        },
        "⑥ 조회업무": {
            "title": "조회업무",
            "content": "거래 및 매출 조회",
            "faq": []
        },
        "⑦ 결제·적립 기준": {
            "title": "결제·적립 기준",
            "content": "적립 및 실적 기준",
            "faq": []
        },
        "⑧ 페이 결제": {
            "title": "페이 결제",
            "content": "PAY 결제 방식",
            "faq": []
        }
    },
    "promotions": [],
    "last_updated": "",
}

# -----------------------------
# 데이터 로드
# -----------------------------
def load_data():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_DATA

def save_data(data):
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# -----------------------------
# UI 시작
# -----------------------------
st.title("🔧 관리자 페이지")

# 홈 이동 버튼
st.page_link("app.py", label="🏠 홈페이지 이동")

# -----------------------------
# 매뉴얼 관리
# -----------------------------
st.subheader("📘 PDA 매뉴얼 관리")

sections = list(data["manuals"].keys())

selected = st.selectbox("섹션 선택", sections)

manual = data["manuals"][selected]

title = st.text_input("제목", value=manual["title"])
content = st.text_area("내용", value=manual["content"], height=200)

if st.button("저장"):
    data["manuals"][selected]["title"] = title
    data["manuals"][selected]["content"] = content
    save_data(data)
    st.success("저장 완료!")

# -----------------------------
# 새 섹션 추가
# -----------------------------
st.markdown("---")
st.subheader("➕ 새 섹션 추가")

new_section = st.text_input("새 섹션 이름")

if st.button("추가"):
    if new_section:
        data["manuals"][new_section] = {
            "title": new_section,
            "content": "",
            "faq": []
        }
        save_data(data)
        st.success("섹션 추가 완료!")
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
            "rule": promo_rule
        })
        save_data(data)
        st.success("추가 완료!")
        st.rerun()

# -----------------------------
# 데이터 확인
# -----------------------------
st.markdown("---")
st.subheader("📊 현재 데이터")

st.json(data)
