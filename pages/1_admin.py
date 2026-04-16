import json
from pathlib import Path
from datetime import datetime

import streamlit as st

st.set_page_config(
    page_title="관리자 페이지",
    page_icon="🔧",
    layout="wide",
)

DATA_PATH = Path(__file__).parent.parent / "knowledge_base.json"

DEFAULT_DATA = {
    "manuals": {
        "① 개설 및 입출금": {
            "title": "개설 및 입출금",
            "content": "계좌 개설 및 입출금 처리 기준",
            "faq": [["개설 업무 시작 전 가장 먼저 확인할 것은?", "고객 정보, 거래 목적, 필수 입력 항목을 먼저 확인합니다."]]
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
            "faq": [["쿠폰과 카드 복합결제 방법", "쿠폰 적용 가능 여부를 먼저 확인한 뒤 카드 결제를 진행합니다."]]
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
            "faq": [["PAY 결제가 안 될 때는?", "네트워크 상태와 지원 수단 여부를 먼저 확인한 뒤 대체 결제를 안내합니다."]]
        }
    },
    "promotions": [],
    "last_updated": "",
    "updated_by": ""
}


def load_data():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_DATA


def save_data(data):
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data["updated_by"] = "관리자"
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def faq_list_to_text(faq_list):
    lines = []
    for item in faq_list:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            lines.append(f"{item[0]} || {item[1]}")
    return "\n".join(lines)


def faq_text_to_list(text):
    result = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "||" in line:
            q, a = line.split("||", 1)
            result.append([q.strip(), a.strip()])
    return result


data = load_data()

st.title("🔧 관리자 페이지")
st.page_link("app.py", label="🏠 홈페이지 이동")

st.subheader("📘 PDA 매뉴얼 관리")

sections = list(data["manuals"].keys())
selected = st.selectbox("섹션 선택", sections)

manual = data["manuals"][selected]

title = st.text_input("제목", value=manual.get("title", ""))
content = st.text_area("내용", value=manual.get("content", ""), height=220)
faq_text = st.text_area(
    "FAQ (한 줄에 하나씩 입력 / 형식: 질문 || 답변)",
    value=faq_list_to_text(manual.get("faq", [])),
    height=180
)

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 저장", use_container_width=True):
        data["manuals"][selected]["title"] = title
        data["manuals"][selected]["content"] = content
        data["manuals"][selected]["faq"] = faq_text_to_list(faq_text)
        save_data(data)
        st.success("저장 완료! 홈페이지에 바로 반영됩니다.")
        st.rerun()

with col2:
    if st.button("🗑 섹션 삭제", use_container_width=True):
        if len(data["manuals"]) == 1:
            st.error("마지막 섹션은 삭제할 수 없습니다.")
        else:
            del data["manuals"][selected]
            save_data(data)
            st.success("섹션 삭제 완료!")
            st.rerun()

st.markdown("---")
st.subheader("➕ 새 섹션 추가")

new_section = st.text_input("새 섹션 이름")
new_content = st.text_area("새 섹션 기본 내용", height=120, key="new_content")
new_faq = st.text_area("새 섹션 FAQ", height=100, placeholder="질문 || 답변", key="new_faq")

if st.button("섹션 추가"):
    if new_section.strip():
        data["manuals"][new_section.strip()] = {
            "title": new_section.strip(),
            "content": new_content.strip(),
            "faq": faq_text_to_list(new_faq)
        }
        save_data(data)
        st.success("섹션 추가 완료!")
        st.rerun()

st.markdown("---")
st.subheader("🎁 프로모션 관리")

promo_name = st.text_input("프로모션명")
promo_rule = st.text_area("프로모션 내용")
promo_period = st.text_input("프로모션 기간")

if st.button("프로모션 추가"):
    if promo_name.strip():
        data["promotions"].append({
            "name": promo_name.strip(),
            "period": promo_period.strip(),
            "rule": promo_rule.strip(),
            "updated_at": datetime.now().strftime("%Y-%m-%d")
        })
        save_data(data)
        st.success("프로모션 추가 완료!")
        st.rerun()
