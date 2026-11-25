# Đề cương và phạm vi

## Phạm vi được giảng viên giới hạn

Cập nhật ngày **25/11/2026**, theo thông tin nhóm cung cấp: **AI chỉ phân loại nội dung theo chủ đề dạng cây phân cấp**. Chỉ đạo riêng cho đề tài này thay thế hướng AI rộng hơn đã đề xuất từ tài liệu môn học chung.

Giảng viên chưa cung cấp cây chủ đề. Nhóm chưa chốt danh sách nhãn, số tầng, đơn nhãn/đa nhãn hoặc việc cho phép dừng ở nút cha. Cây trong [tài liệu taxonomy](11-topic-taxonomy.md) chỉ là minh họa để thảo luận.

## Bài toán

Nội dung KOL/KOC thay đổi theo thời gian. Hệ thống thu thập nội dung mới, phân loại vào cây chủ đề và cập nhật hồ sơ phân bố chủ đề của KOL/KOC. Mỗi kết quả gắn với bài đăng nguồn và phiên bản taxonomy/model để kiểm tra và tái lập.

## Câu hỏi sản phẩm

1. Bài đăng/video thuộc chủ đề nào, từ nhóm tổng quát đến nhóm chi tiết?
2. KOL/KOC tập trung vào những nhánh chủ đề nào trong một khoảng thời gian?
3. Phân bố chủ đề thay đổi thế nào giữa các khoảng thời gian?
4. Những nội dung nào tạo nên số liệu của từng nhánh?

## Input và output mục tiêu

- **Đơn vị phân loại dự kiến:** một bài đăng hoặc video, cần xác nhận trước khi gán nhãn.
- **Input ban đầu:** tiêu đề, mô tả, caption hoặc văn bản bài đăng, kèm ID nội dung và KOL.
- **Media mở rộng:** OCR, transcript hoặc thông tin ảnh/video nếu cần để xác định chủ đề; chúng hỗ trợ cùng tác vụ phân loại, không mở thêm tác vụ sản phẩm.
- **Output mỗi nội dung:** đường dẫn chủ đề hợp lệ, trạng thái phân loại, phiên bản taxonomy/model và liên kết nguồn.
- **Output cấp KOL:** số lượng/tỷ lệ nội dung theo nút của cây và theo thời gian.

Ví dụ minh họa: “Review camera và pin điện thoại” → `Công nghệ → Thiết bị cá nhân → Điện thoại`. Đây chưa phải taxonomy được duyệt hoặc kết quả model.

## Phạm vi triển khai

| Giai đoạn | Phạm vi |
| --- | --- |
| Chốt taxonomy và dữ liệu | Đề xuất cây, định nghĩa từng nhãn, xác nhận với giảng viên; khảo sát khoảng 200 nội dung |
| MVP | Một nguồn dữ liệu khả thi, phân loại chủ đề phân cấp, profile theo cây/thời gian, pipeline streaming và dashboard |
| Mở rộng có điều kiện | Nhiều nền tảng hoặc bổ sung media để cải thiện cùng bài toán chủ đề |

Mốc 200 nội dung và 2–3 kênh pilot là đề xuất khảo sát, không phải cỡ mẫu đủ cho huấn luyện/đánh giá hoặc yêu cầu của môn. Chọn dữ liệu bao phủ các nhánh thay vì mặc định chỉ chọn một lĩnh vực rất hẹp.

## Ngoài phạm vi AI hiện tại

Không triển khai ABSA, sentiment, trích xuất thương hiệu/sản phẩm như đầu ra riêng, phân tích uy tín, recommendation hoặc chatbot. Bình luận không phải đầu vào bắt buộc để phân loại bài đăng; engagement chỉ là metadata tùy chọn, không phải nhãn chủ đề. Việc phân loại riêng chủ đề bình luận chưa nằm trong kế hoạch.

## Giá trị kỹ thuật và đánh giá

- Xây dựng taxonomy và dữ liệu gán nhãn nhất quán theo cây.
- So sánh phân loại nhãn phẳng với phương án khai thác quan hệ cha–con, nếu dữ liệu cho phép.
- Đánh giá từng tầng, đường dẫn hoàn chỉnh, lỗi nhầm nhánh và khả năng từ chối khi thiếu thông tin.
- Duy trì kết quả/profile đúng khi input, model hoặc taxonomy được cập nhật.
- Đánh giá độ trễ, thông lượng và khả năng mở rộng pipeline Big Data.

## Trạng thái triển khai

Hạ tầng Kafka/Spark/PostgreSQL/Airflow đã có. Code `rules-v1` và dashboard hiện còn các trường brand/opinion/sentiment của prototype cũ; chúng không còn đại diện cho yêu cầu mục tiêu. Cần chuyển hợp đồng AI, profile, dashboard và test sang taxonomy đã chốt trước khi coi MVP đáp ứng phạm vi mới.
