import copy
import json
import os
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="관리자 페이지",
    page_icon="🔧",
    layout="wide",
)

DATA_PATH = Path(__file__).parent.parent / "knowledge_base.json"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin1234")


DEFAULT_MANUALS = {
    "결제": {
        "title": "결제 매뉴얼",
        "content": """
1. 고객 결제 수단을 먼저 확인합니다.
2. 쿠폰/프로모션 적용 가능 여부를 확인합니다.
3. 카드/간편결제/복합결제 순서에 따라 결제를 진행합니다.
4. 예외 상황 발생 시 오류 대응 매뉴얼 또는 관리자 문의 기준을 확인합니다.
""".strip(),
        "faq": [
            ["쿠폰과 카드 복합결제 방법", "쿠폰 적용 가능 여부를 먼저 확인한 뒤 카드 결제를 진행합니다. 중복 적용 가능 여부는 프로모션 기준을 함께 확인합니다."],
            ["간편결제 오류 시 어떻게 하나요?", "1차 재시도 후 대체 결제수단을 안내하고, 반복 오류 시 오류 대응 기준에 따라 관리자에게 문의합니다."],
        ],
    },
    "쿠폰/프로모션": {
        "title": "쿠폰/프로모션 매뉴얼",
        "content": """
1. 행사 기간, 대상 브랜드, 적용 조건을 확인합니다.
2. 중복 적용 가능 여부를 확인합니다.
3. 카드사 행사와 백화점 행사 동시 적용 여부를 확인합니다.
4. 매주 변경되는 내용은 관리자 업데이트 항목을 우선 확인합니다.
""".strip(),
        "faq": [
            ["이 쿠폰이 해당 브랜드에 적용되나요?", "브랜드별 적용 여부는 프로모션 운영 기준을 우선 확인합니다. 임대매장은 별도 기준이 있을 수 있습니다."],
            ["사은행사와 카드 프로모션 동시 적용 가능한가요?", "행사별 조건이 다르므로 프로모션 상세 기준을 확인해야 합니다."],
        ],
    },
    "상품권": {
        "title": "상품권 매뉴얼",
        "content": """
1. 상품권 단독 결제 가능 여부를 확인합니다.
2. 상품권 + 카드 복합결제 가능 여부를 확인합니다.
3. 잔액 처리 기준과 제외 대상 브랜드 여부를 확인합니다.
""".strip(),
        "faq": [
            ["상품권과 카드 같이 사용 가능한가요?", "가능 여부는 브랜드 및 결제 유형에 따라 다를 수 있으며, 복합결제 가능 여부를 먼저 확인해야 합니다."],
        ],
    },
    "취소/환불": {
        "title": "취소/환불 매뉴얼",
        "content": """
1. 원결제 수단 기준으로 취소/환불 가능 여부를 확인합니다.
2. 부분 취소 가능 여부를 확인합니다.
3. 쿠폰/프로모션 적용 건은 재계산 기준을 함께 확인합니다.
""".strip(),
        "faq": [
            ["쿠폰 적용 건 환불은 어떻게 하나요?", "원결제 수단 기준으로 처리하되, 쿠폰 및 혜택 재계산 기준을 함께 확인해야 합니다."],
        ],
    },
    "오류 대응": {
        "title": "오류 대응 매뉴얼",
        "content": """
1. 결제기/간편결제 오류 여부를 확인합니다.
2. 동일 수단 재시도 후 대체 수단 안내 여부를 판단합니다.
3. 해결 불가 시 관리자 문의 기준을 따릅니다.
""".strip(),
        "faq": [
            ["POS 오류가 발생했어요.", "오류 유형 확인 → 재시도 → 대체 결제수단 안내 → 관리자 문의 순서로 진행합니다."],
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


def normalize_manuals(raw_manuals):
    manuals = {}
    if isinstance(raw_manuals, dict):
        for key, value in raw_manuals.items():
            if isinstance(value, dict):
                title = value.get("title", f"{key} 매뉴얼")
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
                    "title": f"{key} 매뉴얼",
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


def save_kb(kb, admin_name):
    kb["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    kb["updated_by"] = admin_name
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)


def faq_list_to_text(faq_list):
    return "\n".join([f"{q} || {a}" for q, a in faq_list])


def faq_text_to_list(faq_text):
    faq = []
    for line in faq_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "||" in line:
            q, a = line.split("||", 1)
            faq.append([q.strip(), a.strip()])
    return faq


if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "admin_name" not in st.session_state:
    st.session_state.admin_name = ""

st.title("🔧 관리자 페이지")
st.caption("홈페이지의 매뉴얼/프로모션 데이터를 수정합니다.")

if not st.session_state.admin_logged_in:
    st.subheader("로그인")
    admin_name = st.text_input("이름")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인", use_container_width=True):
        if not admin_name.strip():
            st.error("이름을 입력하세요.")
        elif password != ADMIN_PASSWORD:
            st.error("비밀번호가 올바르지 않습니다.")
        else:
            st.session_state.admin_logged_in = True
            st.session_state.admin_name = admin_name.strip()
            st.rerun()
    st.info("기본 비밀번호는 admin1234 입니다. 배포 시에는 ADMIN_PASSWORD 환경변수 사용을 권장합니다.")
    st.stop()

kb = load_kb()

with st.sidebar:
    st.page_link("app.py", label="홈페이지로 이동", icon="🏠")
    st.write(f"로그인 사용자: {st.session_state.admin_name}")
    if kb.get("last_updated"):
        st.caption(f"최근 저장: {kb['last_updated']}")
    if st.button("로그아웃", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.session_state.admin_name = ""
        st.rerun()

tab1, tab2, tab3 = st.tabs(["매뉴얼 관리", "프로모션 관리", "미리보기"])

with tab1:
    st.subheader("매뉴얼 관리")

    section_names = list(kb["manuals"].keys())
    selected_section = st.selectbox("수정할 섹션", section_names)

    current_manual = kb["manuals"][selected_section]
    new_title = st.text_input("매뉴얼 제목", value=current_manual["title"], key="manual_title")
    new_content = st.text_area("매뉴얼 내용", value=current_manual["content"], height=220, key="manual_content")
    faq_text = st.text_area(
        "FAQ (한 줄에 하나씩 입력, 형식: 질문 || 답변)",
        value=faq_list_to_text(current_manual["faq"]),
        height=180,
        key="manual_faq",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("선택 섹션 저장", use_container_width=True):
            kb["manuals"][selected_section] = {
                "title": new_title.strip() or f"{selected_section} 매뉴얼",
                "content": new_content.strip(),
                "faq": faq_text_to_list(faq_text),
            }
            save_kb(kb, st.session_state.admin_name)
            st.success("매뉴얼이 저장되었습니다.")
            st.rerun()

    with col2:
        if st.button("선택 섹션 삭제", use_container_width=True):
            if len(kb["manuals"]) == 1:
                st.error("마지막 섹션은 삭제할 수 없습니다.")
            else:
                del kb["manuals"][selected_section]
                save_kb(kb, st.session_state.admin_name)
                st.success("섹션이 삭제되었습니다.")
                st.rerun()

    st.markdown("---")
    st.markdown("#### 새 섹션 추가")
    with st.form("add_manual_section", clear_on_submit=True):
        new_key = st.text_input("섹션 이름", placeholder="예: 포인트 결제")
        new_section_title = st.text_input("표시 제목", placeholder="예: 포인트 결제 매뉴얼")
        new_section_content = st.text_area("기본 내용", height=140)
        new_section_faq = st.text_area("FAQ", placeholder="질문 || 답변", height=100)
        submitted = st.form_submit_button("새 섹션 추가", use_container_width=True)

        if submitted:
            key = new_key.strip()
            if not key:
                st.error("섹션 이름을 입력하세요.")
            elif key in kb["manuals"]:
                st.error("이미 존재하는 섹션 이름입니다.")
            else:
                kb["manuals"][key] = {
                    "title": new_section_title.strip() or f"{key} 매뉴얼",
                    "content": new_section_content.strip(),
                    "faq": faq_text_to_list(new_section_faq),
                }
                save_kb(kb, st.session_state.admin_name)
                st.success("새 섹션이 추가되었습니다.")
                st.rerun()

with tab2:
    st.subheader("프로모션 관리")
    st.caption("삭제할 항목은 '삭제'를 체크한 뒤 저장하세요.")

    updated_promotions = []

    for idx, promo in enumerate(kb["promotions"]):
        with st.expander(f"{idx + 1}. {promo['name']}", expanded=False):
            name = st.text_input("프로모션명", value=promo["name"], key=f"promo_name_{idx}")
            period = st.text_input("기간", value=promo["period"], key=f"promo_period_{idx}")
            rule = st.text_area("기준", value=promo["rule"], key=f"promo_rule_{idx}", height=120)
            delete_this = st.checkbox("이 항목 삭제", key=f"promo_delete_{idx}")

            if not delete_this:
                updated_promotions.append(
                    {
                        "name": name.strip(),
                        "period": period.strip(),
                        "rule": rule.strip(),
                        "updated_at": datetime.now().strftime("%Y-%m-%d"),
                    }
                )

    if st.button("프로모션 저장", use_container_width=True):
        kb["promotions"] = [item for item in updated_promotions if item["name"]]
        save_kb(kb, st.session_state.admin_name)
        st.success("프로모션이 저장되었습니다.")
        st.rerun()

    st.markdown("---")
    st.markdown("#### 새 프로모션 추가")
    with st.form("add_promotion", clear_on_submit=True):
        new_name = st.text_input("프로모션명", placeholder="예: 신규 고객 할인")
        new_period = st.text_input("기간", placeholder="예: 2026-05-01 ~ 2026-05-31")
        new_rule = st.text_area("기준", placeholder="예: 첫 결제 시 10% 할인", height=120)
        add_submitted = st.form_submit_button("프로모션 추가", use_container_width=True)

        if add_submitted:
            if not new_name.strip():
                st.error("프로모션명을 입력하세요.")
            else:
                kb["promotions"].insert(
                    0,
                    {
                        "name": new_name.strip(),
                        "period": new_period.strip(),
                        "rule": new_rule.strip(),
                        "updated_at": datetime.now().strftime("%Y-%m-%d"),
                    },
                )
                save_kb(kb, st.session_state.admin_name)
                st.success("새 프로모션이 추가되었습니다.")
                st.rerun()

with tab3:
    st.subheader("현재 저장된 데이터 미리보기")
    st.json(kb)
