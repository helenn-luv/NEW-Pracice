import copy
import json
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="PDA QUICK MANUAL",
    page_icon="💳",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "knowledge_base.json"

DEFAULT_MANUALS = {
    "① 개설 및 입출금": {
        "title": "개설 및 입출금",
        "content": "계좌 개설 및 입출금 처리 기준",
        "faq": [
            ["개설 업무 시작 전 가장 먼저 확인할 것은?", "고객 정보, 거래 목적, 필수 입력 항목을 먼저 확인합니다."]
        ],
    },
    "② 상품등록": {
        "title": "상품등록",
        "content": "상품 등록 및 수정 방법",
        "faq": [],
    },
    "③ 판매보조": {
        "title": "판매보조",
        "content": "판매 보조 기능 안내",
        "faq": [],
    },
    "④ 거래호출": {
        "title": "거래호출",
        "content": "거래 조회 및 호출 방법",
        "faq": [],
    },
    "⑤ 결제형태별 거래": {
        "title": "결제형태별 거래",
        "content": "카드/간편결제/복합결제",
        "faq": [
            ["쿠폰과 카드 복합결제 방법", "쿠폰 적용 가능 여부를 먼저 확인한 뒤 카드 결제를 진행합니다."]
        ],
    },
    "⑥ 조회업무": {
        "title": "조회업무",
        "content": "거래 및 매출 조회",
        "faq": [],
    },
    "⑦ 결제·적립 수단별 우수고객 실적합산 기준": {
        "title": "결제·적립 수단별 우수고객 실적합산 기준",
        "content": "적립 및 실적 기준",
        "faq": [],
    },
    "⑧ 페이 PAY-지원 결제방식": {
        "title": "페이 PAY-지원 결제방식",
        "content": "PAY 결제 방식",
        "faq": [
            ["PAY 결제가 안 될 때는?", "네트워크 상태와 지원 수단 여부를 먼저 확인한 뒤 대체 결제를 안내합니다."]
        ],
    },
}

DEFAULT_PROMOTIONS = []

KPI_TARGETS = {
    "결제 이탈률": "감소 목표",
    "결제 완료율": "증가 목표",
    "대기시간": "단축 목표",
    "직원 사용률": "사용 로그 확인",
}


def normalize_manuals(raw_manuals):
    manuals = {}
    if not isinstance(raw_manuals, dict):
        return copy.deepcopy(DEFAULT_MANUALS)

    for key, value in raw_manuals.items():
        if isinstance(value, dict):
            title = value.get("title", key)
            content = value.get("content", "")
            faq_raw = value.get("faq", [])
            faq = []
            for item in faq_raw:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    faq.append([str(item[0]), str(item[1])])
                elif isinstance(item, dict):
                    faq.append([str(item.get("question", "")), str(item.get("answer", ""))])
            manuals[key] = {"title": title, "content": content, "faq": faq}
        elif isinstance(value, list):
            manuals[key] = {
                "title": key,
                "content": "\n".join(f"{idx}. {line}" for idx, line in enumerate(value, start=1)),
                "faq": [],
            }

    if not manuals:
        manuals = copy.deepcopy(DEFAULT_MANUALS)

    for key, value in DEFAULT_MANUALS.items():
        manuals.setdefault(key, copy.deepcopy(value))

    return manuals


def load_kb():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
    else:
        raw = {}

    manuals_raw = raw.get("manuals", raw.get("manual", {}))
    promotions_raw = raw.get("promotions", [])
    return {
        "manuals": normalize_manuals(manuals_raw),
        "promotions": promotions_raw if isinstance(promotions_raw, list) else copy.deepcopy(DEFAULT_PROMOTIONS),
        "last_updated": raw.get("last_updated", ""),
        "updated_by": raw.get("updated_by", ""),
    }


kb = load_kb()
manuals = kb["manuals"]
promotions = kb["promotions"]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("assistant", "안녕하세요. PDA 퀵매뉴얼에서 필요한 카테고리를 선택하거나 질문을 입력해주세요.")
    ]


def find_answer(user_text: str) -> str:
    q = user_text.strip()

    mappings = [
        (["쿠폰", "카드"], "⑤ 결제형태별 거래", "쿠폰 적용 가능 여부를 먼저 확인한 뒤 카드 결제를 진행합니다."),
        (["상품권"], "⑤ 결제형태별 거래", "상품권과 카드 복합결제 가능 여부를 먼저 확인해주세요."),
        (["환불"], "⑤ 결제형태별 거래", "원결제 수단 기준으로 환불을 진행하고 예외 기준을 확인해주세요."),
        (["오류"], "⑤ 결제형태별 거래", "오류 유형 확인 → 재시도 → 대체 수단 안내 → 관리자 문의 순으로 대응합니다."),
        (["조회"], "⑥ 조회업무", "조회 유형을 선택한 뒤 검색 조건을 정확히 입력합니다."),
        (["페이"], "⑧ 페이 PAY-지원 결제방식", "지원 가능한 PAY 수단 여부를 먼저 확인한 뒤 결제를 진행합니다."),
    ]

    for keywords, menu, answer in mappings:
        if all(k in q for k in keywords):
            return f"[{menu}] {answer}"

    for menu_name, data in manuals.items():
        if menu_name in q or data["title"] in q:
            return f"[{menu_name}]\n{data['content'].strip()}"

    return "관련 매뉴얼을 찾지 못했습니다. 왼쪽 메뉴에서 PDA 카테고리를 선택하거나 질문을 더 구체적으로 입력해주세요."


def add_chat(role: str, text: str):
    st.session_state.chat_history.append((role, text))


st.title("💳 PDA QUICK MANUAL")
st.caption("PDA 매뉴얼 카테고리 기반으로 결제/조회/오류 대응 정보를 빠르게 확인하는 직원 지원형 화면")

col1, col2, col3, col4 = st.columns(4)
col1.metric("결제 이탈률", KPI_TARGETS["결제 이탈률"])
col2.metric("결제 완료율", KPI_TARGETS["결제 완료율"])
col3.metric("대기시간", KPI_TARGETS["대기시간"])
col4.metric("직원 사용률", KPI_TARGETS["직원 사용률"])

with st.sidebar:
    st.header("PDA 카테고리")
    st.page_link("pages/1_admin.py", label="관리자 페이지", icon="🔐")

    if kb.get("last_updated"):
        st.caption(f"최근 업데이트: {kb['last_updated']}")
        if kb.get("updated_by"):
            st.caption(f"수정자: {kb['updated_by']}")

    selected_menu = st.radio(
        "매뉴얼 선택",
        list(manuals.keys()),
        index=0,
        help="PDA 퀵매뉴얼 카테고리를 직접 탐색할 수 있습니다.",
    )

    st.markdown("---")
    st.subheader("자주 찾는 질문")
    quick_questions = [
        "쿠폰과 카드 복합결제 방법",
        "조회업무는 어디서 확인하나요?",
        "페이 결제가 안 될 때는?",
        "간편결제 오류 시 어떻게 하나요?",
    ]
    for q in quick_questions:
        if st.button(q, use_container_width=True):
            add_chat("user", q)
            add_chat("assistant", find_answer(q))

with st.container():
    tab1, tab2, tab3 = st.tabs(["챗봇", "매뉴얼", "프로모션"])

with tab1:
    left, right = st.columns([1.2, 0.8])

    with left:
        st.subheader("챗봇 질의응답")
        chat_container = st.container(border=True)
        with chat_container:
            for role, msg in st.session_state.chat_history:
                with st.chat_message("assistant" if role == "assistant" else "user"):
                    st.write(msg)

        user_prompt = st.chat_input("예: 페이 결제가 안 될 때는?")
        if user_prompt:
            add_chat("user", user_prompt)
            add_chat("assistant", find_answer(user_prompt))
            st.rerun()

    with right:
        st.subheader("선택된 매뉴얼 요약")
        manual = manuals[selected_menu]
        st.info(f"**{manual['title']}**")
        st.write(manual["content"])

        st.subheader("관련 FAQ")
        if manual["faq"]:
            for q, a in manual["faq"]:
                with st.expander(q):
                    st.write(a)
        else:
            st.caption("등록된 FAQ가 없습니다.")

with tab2:
    st.subheader("PDA 매뉴얼 직접 탐색")
    c1, c2 = st.columns([0.9, 1.1])

    with c1:
        st.markdown("### 카테고리")
        for key in manuals.keys():
            st.write(f"- {key}")

    with c2:
        manual = manuals[selected_menu]
        st.markdown(f"### {manual['title']}")
        st.write(manual["content"])

        st.markdown("### 업무 흐름")
        st.code("카테고리 선택 → 기준 확인 → FAQ 확인 → 필요한 경우 챗봇 질문", language=None)

with tab3:
    st.subheader("최신 프로모션 정보")
    st.caption("관리자 페이지에서 수정한 프로모션이 여기에 반영됩니다.")

    if promotions:
        for idx, promo in enumerate(promotions, start=1):
            with st.container(border=True):
                st.markdown(f"**{idx}. {promo.get('name', '')}**")
                st.write(f"- 기간: {promo.get('period', '')}")
                st.write(f"- 기준: {promo.get('rule', '')}")
                if promo.get("updated_at"):
                    st.write(f"- 업데이트: {promo['updated_at']}")
    else:
        st.warning("등록된 프로모션이 없습니다.")
