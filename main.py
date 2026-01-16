import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="PDF 변환기", page_icon="📄")

st.title("📄 이미지 합치기 (PDF 변환)")
st.write("이미지 파일을 드래그해서 넣으면 순서대로 합쳐줍니다.")

# 파일 업로더
uploaded_files = st.file_uploader("이미지를 선택하세요", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if uploaded_files:
    # 파일 이름 순서대로 정렬 (1.png, 2.png 순서 보장)
    uploaded_files.sort(key=lambda x: x.name)
    
    st.write(f"총 {len(uploaded_files)}개의 이미지가 선택되었습니다.")
    
    # 미리보기 (첫 번째 이미지)
    st.image(uploaded_files[0], caption="첫 번째 페이지 미리보기", width=300)

    if st.button("PDF로 변환하기"):
        with st.spinner('변환 중...'):
            try:
                # 이미지 처리
                images = []
                for file in uploaded_files:
                    img = Image.open(file).convert('RGB')
                    images.append(img)
                
                # PDF 메모리에 저장
                pdf_bytes = io.BytesIO()
                images[0].save(pdf_bytes, format='PDF', save_all=True, append_images=images[1:])
                
                st.success("완료! 아래 버튼을 눌러 다운로드하세요.")
                
                # 다운로드 버튼
                st.download_button(
                    label="📥 PDF 다운로드",
                    data=pdf_bytes.getvalue(),
                    file_name="presentation.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
