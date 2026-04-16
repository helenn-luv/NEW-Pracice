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

# -----------------------------
# PDA 매뉴얼 기본 데이터
# -----------------------------
DEFAULT_MANUALS = {
    "① 개설 및 입출금": {
        "title": "개설 및 입출금",
        "content": """
1. 개설 업무 전 고객 정보와 필수 입력 항목을 확인합니다.
2. 입금/출금 처리 전 거래 유형과 금액을 재확인합니다.
3. 처리 완료 후 영수증 또는 결과 화면을 고객에게 안내합니다.
4. 예외 상황 발생 시 관리자 또는 상세 매뉴얼 기준을 확인합니다.
""".strip(),
        "faq": [
            ["개설 업무 시작 전 가장 먼저 확인할 것은?", "고객 정보, 거래 목적, 필수 입력 항목을 먼저 확인합니다."],
            ["입출금 처리 중 오류가 나면?", "거래 상태를 먼저 확인한 뒤 재시도 또는 관리자 문의 기준을 따릅니다."],
        ],
    },
    "② 상품등록": {
        "title": "상품등록",
        "content": """
1. 상품 코드, 상품명, 금액 정보를 정확히 입력합니다.
2. 행사 상품 여부와 적용 조건을 확인합니다.
3. 수정/삭제 이력은 관리자 기준에 따라 처리합니다.
4. 등록 완료 후 정상 반영 여부를 조회 화면에서 확인합니다.
""".strip(),
        "faq": [
            ["상품등록 후 바로 반영되지 않아요.", "조회업무 메뉴에서 반영 여부를 확인하고 필요 시 재등록합니다."],
            ["행사 상품도 동일하게 등록하나요?", "기본 등록 후 행사/프로모션 조건을 함께 확인해야 합니다."],
        ],
    },
    "③ 판매보조": {
        "title": "판매보조",
        "content": """
1. 고객 문의 유형을 먼저 파악합니다.
2. 결제/적립/행사 적용 가능 여부를 빠르게 확인합니다.
3. 필요한 경우 관련 매뉴얼 또는 FAQ로 연결합니다.
4. 반복 문의는 자주 찾는 질문으로 표준화합니다.
""".strip(),
        "faq": [
            ["판매보조 기능은 언제 사용하나요?", "즉시 판단이 필요한 응대 상황에서 빠른 기준 확인용으로 사용합니다."],
        ],
    },
    "④ 거래호출": {
        "title": "거래호출",
        "content": """
1. 거래번호 또는 호출 기준 정보를 확인합니다.
2. 해당 거래 상태를 조회한 뒤 필요한 후속 조치를 진행합니다.
3. 미완료 거래 또는 오류 거래는 별도 기준에 따라 처리합니다.
4. 호출 후 변경 내역은 시스템에 기록합니다.
""".strip(),
        "faq": [
            ["거래호출이 필요한 경우는?", "이전 거래 재확인, 오류 거래 추적, 후속 처리 시 사용합니다."],
        ],
    },
    "⑤ 결제형태별 거래": {
        "title": "결제형태별 거래",
        "content": """
1. 카드, 현금, 간편결제, 복합결제 중 거래 유형을 먼저 구분합니다.
2. 결제수단별 승인/취소/부분취소 가능 여부를 확인합니다.
3. 쿠폰·프로모션·상품권 동시 적용 여부를 확인합니다.
4. 예외 상황은 오류 대응 기준과 함께 확인합니다.
""".strip(),
        "faq": [
            ["쿠폰과 카드 복합결제 방법", "쿠폰 적용 가능 여부를 먼저 확인한 뒤 카드 결제를 진행합니다."],
            ["간편결제 오류 시 어떻게 하나요?", "1차 재시도 후 대체 결제수단을 안내하고 반복 오류는 관리자 기준을 따릅니다."],
        ],
    },
    "⑥ 조회업무": {
        "title": "조회업무",
        "content": """
1. 거래조회, 상품조회, 반영조회 등 필요한 조회 유형을 선택합니다.
2. 검색 조건을 정확히 입력합니다.
3. 조회 결과를 고객 응대 또는 후속 업무에 활용합니다.
4. 민감 정보는 내부 기준에 따라 관리합니다.
""".strip(),
        "faq": [
            ["거래 조회가 안 될 때는?", "검색 조건과 거래 상태를 다시 확인한 뒤 관리자 기준을 따릅니다."],
        ],
    },
    "⑦ 결제·적립 수단별 우수고객 실적합산 기준": {
        "title": "결제·적립 수단별 우수고객 실적합산 기준",
        "content": """
1. 결제수단과 적립수단의 실적 반영 기준을 구분합니다.
2. 우수고객 실적합산 대상 여부를 확인합니다.
3. 제외 항목과 예외 기준을 반드시 확인합니다.
4. 프로모션/행사 적용 시 중복 반영 여부를 함께 확인합니다.
""".strip(),
        "faq": [
            ["실적합산 기준은 어디에 쓰이나요?", "우수고객 산정, 혜택 적용, 내부 실적 반영 기준 확인에 사용합니다."],
        ],
    },
    "⑧ 페이 PAY-지원 결제방식": {
        "title": "페이 PAY-지원 결제방식",
        "content": """
1. 지원 가능한 페이 결제수단을 먼저 확인합니다.
2. 바코드, QR, 태깅 등 결제 방식에 따라 절차를 진행합니다.
3. 승인 실패 시 재시도 또는 대체 수단을 안내합니다.
4. 행사/캐시백 적용 여부를 함께 확인합니다.
""".strip(),
        "faq": [
            ["PAY 결제가 안 될 때는?", "네트워크 상태와 지원 수단 여부를 먼저 확인한 뒤 대체 결제를 안내합니다."],
        ],
    },
}

DEFAULT_PROMOTIONS = [
    {
        "name": "주말 카드 프로모션",
        "period": "매주 금~일",
        "rule": "지정 카드 결제 시 5% 즉시 할인",
        "updated_at": "2026-04-01",
    },
    {
        "name": "앱 쿠폰 행사",
        "period": "4월 한정",
        "rule": "앱 다운로드 고객 대상 쿠폰 적용",
        "updated_at": "2026-04-03",
    },
]

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


def normalize_promotions(raw_promotions):
    promotions = []
    if isinstance(raw_promotions, list):
        for item in raw_promotions:
            if not isinstance(item, dict):
                continue
            if "name" in item:
                promotions.append(
                    {
                        "name": item.get("name", ""),
                        "period": item.get("period", ""),
                        "rule": item.get("rule", ""),
                        "updated_at": item.get("updated_at", ""),
                    }
                )
            elif "title" in item:
                desc = item.get("description", "")
                condition = item.get("condition", "")
                combined_rule = desc
                if condition:
                    combined_rule = f"{desc} / 조건: {condition}" if desc else f"조건: {condition}"
                promotions.append(
                    {
                        "name": item.get("title", ""),
                        "period": item.get("period", ""),
                        "rule": combined_rule,
                        "updated_at": item.get("updated_at", ""),
                    }
                )

    if not promotions:
        promotions = copy.deepcopy(DEFAULT_PROMOTIONS)

    return promotions


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
        "promotions": normalize_promotions(promotions_raw),
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

    if "프로모션" in q or "행사" in q:
        if promotions:
            latest = promotions[0]
            return f"[프로모션] 현재 대표 프로모션은 '{latest['name']}'이며, 기간은 {latest['period']} / 기준은 {latest['rule']} 입니다."
        return "현재 등록된 프로모션 정보가 없습니다."

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

    st.markdown("---")
    st.subheader("운영 포인트")
    st.write("- PDA 카테고리 구조 기반 탐색")
    st.write("- 매뉴얼 + 질문 방식 병행")
    st.write("- 관리자 페이지에서 최신 정보 업데이트")

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
                st.markdown(f"**{idx}. {promo['name']}**")
                st.write(f"- 기간: {promo['period']}")
                st.write(f"- 기준: {promo['rule']}")
                if promo.get("updated_at"):
                    st.write(f"- 업데이트: {promo['updated_at']}")
    else:
        st.warning("등록된 프로모션이 없습니다.")

st.markdown("---")
st.markdown(
    """
**기획 요약**  
- PDA 퀵매뉴얼 카테고리 기반으로 현장 응대를 표준화합니다.  
- 질문형 인터페이스와 메뉴형 탐색을 함께 제공합니다.  
- 관리자 업데이트 구조를 통해 최신 프로모션/매뉴얼 정보를 유지합니다.  
"""
)
