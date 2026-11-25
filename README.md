# Dynamic KOL/KOC Content Intelligence

Đồ án môn **SE363 — Phát triển ứng dụng trên nền tảng dữ liệu lớn**: theo dõi nội dung và phản ứng người xem để xây dựng hồ sơ KOL/KOC cập nhật theo thời gian, kèm dẫn chứng.

**Trạng thái:** đã thống nhất hướng đề tài, đang chuẩn bị dữ liệu và thiết kế. Repository hiện có tài liệu; chưa có pipeline, mô hình hoặc ứng dụng được triển khai.

## Phạm vi khởi đầu

- Thử thu thập YouTube cho 2–3 kênh, sau đó hướng tới 5–10 KOL/KOC trong cùng lĩnh vực.
- Phân tích chủ đề, thương hiệu và bình luận theo thực thể, khía cạnh, đoạn ý kiến và cảm xúc.
- Cập nhật profile theo cửa sổ thời gian; truy ngược được nội dung làm bằng chứng.
- Xây pipeline near-real-time bằng Kafka, Spark Structured Streaming và AI service.
- Đánh giá chất lượng AI, độ trễ, thông lượng và tính đúng khi xử lý dữ liệu trùng hoặc đến muộn.

Các con số trên là **mốc lập kế hoạch**, chưa phải kết quả hay yêu cầu bắt buộc của môn học. Chi tiết được ghi trong bộ tài liệu dưới đây.

## Tài liệu

| Tài liệu | Nội dung |
| --- | --- |
| [Mục lục tài liệu](docs/README.md) | Cách đọc và tài liệu nguồn |
| [Đề cương và phạm vi](docs/01-project-proposal.md) | Bài toán, mục tiêu, phạm vi và quyết định còn mở |
| [Yêu cầu](docs/02-requirements.md) | Chức năng, yêu cầu hệ thống và điều kiện nghiệm thu |
| [Kiến trúc](docs/03-architecture.md) | Thành phần, luồng sự kiện và khả năng mở rộng |
| [Kế hoạch dữ liệu](docs/04-data-plan.md) | Thu thập, schema, gán nhãn và chia tập |
| [Thiết kế AI](docs/05-ai-design.md) | Tác vụ, baseline, bằng chứng và phiên bản mô hình |
| [Kế hoạch đánh giá](docs/06-evaluation-plan.md) | Thực nghiệm AI và hệ thống |
| [Lộ trình](docs/07-roadmap.md) | Mốc triển khai và sản phẩm bàn giao |
| [Quyết định và rủi ro](docs/08-decisions-and-risks.md) | Lựa chọn hiện tại, giả định và cách kiểm chứng |

## Nguyên tắc triển khai

Ưu tiên một luồng end-to-end hoạt động được trước khi mở rộng tính năng. Mọi kết luận trên dashboard cần gắn với dữ liệu nguồn, khoảng thời gian và phiên bản phân tích. Dữ liệu replay và dữ liệu thu thập trực tiếp phải được phân biệt rõ trong demo và báo cáo.
