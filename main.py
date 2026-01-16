import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="PDF 변환기", page_icon="📄")

st.title("📄 내 맘대로 순서 정하기 (PDF 변환)")
st.write("이미지를 업로드하고, 아래 박스에서 순서를 자유롭게 바꾸세요.")

# 1. 파일 업로더
uploaded_files = st.file_uploader("이미지들을 선택하세요", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if uploaded_files:
    # 파일 이름과 파일 객체를 매칭하는 사전 생성
    file_dict = {file.name: file for file in uploaded_files}
    
    # 2. 순서 변경 위젯 (Multiselect)
    st.markdown("### 👇 여기서 순서를 조정하세요")
    st.info("박스 안의 파일 이름을 드래그하거나, X를 눌러 뺐다가 다시 추가하여 순서를 맞추세요.")
    
    # 기본적으로 업로드된 순서대로 초기화
    selected_filenames = st.multiselect(
        "이미지 순서 (드래그하여 이동)",
        options=list(file_dict.keys()),
        default=list(file_dict.keys())
    )

    # 3. 미리보기 (선택된 순서대로 정렬)
    if selected_filenames:
        st.markdown("---")
        st.markdown("### 👀 미리보기 (이 순서대로 저장됩니다)")
        
        # 선택된 파일들을 순서대로 리스트에 담기
        sorted_images = []
        
        # 미리보기 이미지를 3개씩 나란히 보여주기 위한 컬럼 설정
        cols = st.columns(3)
        
        for idx, filename in enumerate(selected_filenames):
            file_obj = file_dict[filename]
            img = Image.open(file_obj).convert('RGB')
            sorted_images.append(img)
            
            # 미리보기 출력 (3열 그리드)
            with cols[idx % 3]:
                st.image(img, caption=f"{idx+1}번: {filename}", use_container_width=True)

        st.markdown("---")

        # 4. PDF 변환 버튼
        if st.button("이 순서대로 PDF 만들기"):
            with st.spinner('PDF 생성 중...'):
                try:
                    pdf_bytes = io.BytesIO()
                    
                    # 정렬된 이미지 리스트(sorted_images)를 사용하여 PDF 저장
                    if sorted_images:
                        sorted_images[0].save(
                            pdf_bytes, 
                            format='PDF', 
                            save_all=True, 
                            append_images=sorted_images[1:]
                        )
                        
                        st.success("생성 완료! 아래 버튼을 눌러주세요.")
                        st.download_button(
                            label="📥 PDF 다운로드",
                            data=pdf_bytes.getvalue(),
                            file_name="result.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"오류 발생: {e}")
    else:
        st.warning("선택된 이미지가 없습니다. 위 박스에서 이미지를 선택해주세요.")
