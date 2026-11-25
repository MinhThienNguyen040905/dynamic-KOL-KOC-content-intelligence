# Bộ tài liệu đồ án

Bộ tài liệu này chuyển hướng đề tài đã thống nhất thành kế hoạch có thể triển khai và kiểm chứng. Ngày khởi tạo: **25/11/2026**.

## Thứ tự đọc

1. [Đề cương và phạm vi](01-project-proposal.md).
2. [Yêu cầu và nghiệm thu](02-requirements.md).
3. [Kiến trúc hệ thống](03-architecture.md).
4. [Kế hoạch dữ liệu](04-data-plan.md).
5. [Thiết kế AI](05-ai-design.md).
6. [Kế hoạch đánh giá](06-evaluation-plan.md).
7. [Lộ trình triển khai](07-roadmap.md).
8. [Quyết định và rủi ro](08-decisions-and-risks.md).
9. [Thiết lập và phát triển](09-development.md).
10. [Điều phối bằng Airflow](10-airflow.md).

## Tài liệu nguồn trong thư mục

- [Hướng dẫn đồ án SE363](Hướng%20dẫn%20đồ%20án%20môn%20SE363%20–%20Phát%20triển%20ứng%20dụng%20trên%20nền%20tảng%20dữ%20liệu%20lớn.pdf): trang 1–2 nêu yêu cầu chung; trang 6 mô tả đề tài số 13, Dynamic KOL/KOC Content Intelligence.
- [Slide hướng dẫn đồ án](SE363_Project_Guidance_Deck.pptx.pdf): trang 4–8 về kiến trúc, AI và đánh giá; trang 17 về lộ trình và sản phẩm bàn giao.
- [Ảnh tổng quan SE363](Copy%20of%20SE363.png): minh họa luồng offline/online và các cách triển khai AI.

## Cách hiểu trạng thái tài liệu

- **Yêu cầu môn học:** rút ra từ tài liệu giảng viên, như streaming/near-real-time, AI đủ sâu, đánh giá AI và hệ thống, giải thích khả năng mở rộng.
- **Thiết kế đề xuất:** lựa chọn của project để đáp ứng yêu cầu; được điều chỉnh khi có bằng chứng thực nghiệm.
- **Chưa chốt:** thiếu thông tin về nguồn dữ liệu, tài nguyên hoặc nhân sự; không được coi là cam kết đã hoàn thành.

Chưa có rubric chấm điểm chi tiết, ngưỡng latency/F1 bắt buộc hay yêu cầu xử lý đủ mọi loại media trong tài liệu nguồn. Không tự biến mốc thử nghiệm của nhóm thành yêu cầu của giảng viên.

Khi thay đổi phạm vi, cập nhật đồng thời yêu cầu, kế hoạch đánh giá và lộ trình; ghi lý do vào [nhật ký quyết định](08-decisions-and-risks.md).
