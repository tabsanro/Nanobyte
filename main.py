import time
import streamlit as st
from loguru import logger # for logging
import base64

def main():
    # 페이지 설정
    st.set_page_config(
        page_title="나노바이트 물품 추천 서비스",
        page_icon=":books:"
    )

    st.title(":red[나노바이트] 물품 추천 서비스")

    # 세션 상태 초기화
    if "conversations" not in st.session_state:
        st.session_state.conversations = []
    if "current_conversation" not in st.session_state:
        # 대화 초기 메시지 설정
        st.session_state.current_conversation = [{"role": "assistant", 
                                                  "content": "안녕하세요.  \n 세종대학교 전자정보통신공학과 나노바이트 팀의 상황 정보 기반 대화형 상품 추천 서비스입니다.  \n다이소에서 필요한 걸 물어보세요!"}]
        st.session_state.conversations.append(st.session_state.current_conversation)

    # New Chat 버튼과 대화 목록 표시
    with st.sidebar:
        if st.button(":pencil2: New Chat"):
            make_new_chat()

        # 기존 대화 목록 버튼
        for i, conversation in enumerate(st.session_state.conversations):
            if st.button(f"대화 {i + 1}"):
                st.session_state.current_conversation = conversation

        # 사진 업로드 기능 추가
        uploaded_files = st.file_uploader("사진 업로드", type=['png', 'jpg'],
                                          accept_multiple_files=False,
                                          help="고객님의 상황을 설명하는데 도움을 줄 사진을 올려주세요."
                                          )
        import speech
        # HTML 및 JavaScript 코드 삽입
        st.components.v1.html(speech.stt_html, height=600)

        # 이벤트 리스너로부터 오디오 데이터 수신
        audio_data = st.experimental_get_query_params().get("audioData", [None])[0]

        if audio_data:
            st.audio(base64.b64decode(audio_data), format="audio/wav")

    # 대화 기록 출력
    for message in st.session_state.current_conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 새로운 메시지를 입력하고 `send` 함수 호출
    if query := st.chat_input("질문을 입력해주세요."):
        st.session_state.current_conversation.append({"role": "user", "content": query})

        with st.chat_message("user"):
            if uploaded_files:
                st.image(uploaded_files)
            st.markdown(query)

        request_response(query)
    
    print("current_session_state: ", time.time())
    print(st.session_state)

def make_new_chat():

    st.session_state.current_conversation = [{"role": "assistant", 
                                            "content": "안녕하세요.  \n 세종대학교 전자정보통신공학과 나노바이트 팀의 상황 정보 기반 대화형 상품 추천 서비스입니다.  \n다이소에서 필요한 걸 물어보세요!"}]
    st.session_state.conversations.append(st.session_state.current_conversation)
        

def request_response(user_input):
    # TODO: 사용자 입력과 이미지를 같이 처리할 수 있는 로직 추가
    # 기본 응답 생성 및 추가
    response = f"입력하신 내용: {user_input}  \n에 대해 도움을 드리겠습니다!"
    with st.chat_message("assistant"):
        st.markdown(response)
    # 대화에 응답 추가
    st.session_state.current_conversation.append({"role": "assistant", "content": response})

if __name__ == '__main__':
    main()
    