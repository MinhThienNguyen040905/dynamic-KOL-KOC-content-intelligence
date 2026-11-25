# Đề cương và phạm vi

## Bài toán

Nội dung, thương hiệu được nhắc và phản ứng người xem của KOL/KOC thay đổi liên tục. Một profile tĩnh không thể hiện được thay đổi gần đây hoặc nội dung nào tạo nên nhận định đó.

Project xây dựng hệ thống theo dõi near-real-time, phân tích nội dung và bình luận, cập nhật profile theo thời gian và cho phép truy ngược dẫn chứng. Người dùng mục tiêu ban đầu là người phân tích nội dung hoặc phụ trách theo dõi KOL/KOC cho hoạt động marketing.

## Câu hỏi sản phẩm

1. KOL/KOC đang nói về chủ đề và thương hiệu nào?
2. Người xem đánh giá KOL và sản phẩm ở khía cạnh nào, với cảm xúc gì?
3. Những phân bố này thay đổi thế nào giữa các khoảng thời gian?
4. Video hoặc bình luận nào hỗ trợ từng kết luận?

## Phạm vi đề xuất

| Giai đoạn | Phạm vi |
| --- | --- |
| Khảo sát dữ liệu | 2–3 kênh YouTube, một lĩnh vực; thử gán nhãn khoảng 200 bình luận |
| MVP | Hướng tới 5–10 kênh; tiêu đề, mô tả, bình luận và snapshot tương tác; hai tác vụ AI chính; profile theo thời gian; pipeline và dashboard |
| Mở rộng sau MVP | Transcript có nguồn truy cập phù hợp hoặc keyframe; so sánh với baseline chỉ dùng văn bản |

Chọn lĩnh vực sau khảo sát: review công nghệ hoặc mỹ phẩm là hai ứng viên. Chỉ chọn một lĩnh vực cho MVP. Chất lượng và khả năng thu thập dữ liệu quyết định lựa chọn cuối cùng.

## Hai phần AI chính

- **Hiểu nội dung:** xác định chủ đề, trích xuất thương hiệu và lưu bằng chứng trong tiêu đề/mô tả; bổ sung timestamp nếu có transcript.
- **Hiểu phản ứng:** trích xuất cấu trúc `Entity → Aspect → Opinion span → Sentiment` từ bình luận, sử dụng ngữ cảnh video khi cần.

Ví dụ minh họa: “Bạn này review dễ hiểu nhưng máy X pin yếu” chứa nhận xét tích cực về cách trình bày của KOL và nhận xét tiêu cực về pin của sản phẩm X. Đây là ví dụ thiết kế, không phải kết quả mô hình.

## Giá trị kỹ thuật dự kiến

- Liên kết nhận xét với đúng thực thể thay vì chỉ gán cảm xúc toàn câu.
- Cập nhật profile từ sự kiện mới, xử lý trùng và sự kiện đến muộn.
- Đánh giá tác động của ngữ cảnh nội dung lên phân tích bình luận.
- Đo đánh đổi giữa chất lượng, độ trễ và tải của pipeline có AI service.

Đóng góp thực tế chỉ được khẳng định sau thực nghiệm. Không mặc định phải tạo mô hình mới hoặc huấn luyện từ đầu.

## Giới hạn MVP

Chưa đưa vào phạm vi: đa nền tảng, recommendation KOL cho chiến dịch, chatbot/RAG, multi-agent, phát hiện khủng hoảng, nhận diện khuôn mặt và xử lý video đầy đủ. Chúng chỉ được bổ sung sau khi luồng chính đã được đánh giá.

## Những điểm cần chốt

- Lĩnh vực, danh sách kênh và khả năng truy cập dữ liệu.
- Số thành viên, thời gian học kỳ, CPU/RAM/GPU và ngân sách inference.
- Taxonomy chủ đề/khía cạnh, quy mô nhãn và mục tiêu hiệu năng sau pilot.
- Khả năng bổ sung media để phát triển phần đa phương thức trước nghiệm thu cuối kỳ.
