# Dynamic KOL/KOC Content Intelligence

Đồ án môn **SE363 — Phát triển ứng dụng trên nền tảng dữ liệu lớn**: phân loại nội dung KOL/KOC theo cây chủ đề và cập nhật hồ sơ chủ đề theo thời gian.

**Phạm vi mới ngày 25/11/2026:** theo chỉ đạo riêng của giảng viên mà nhóm xác nhận, AI chỉ phân loại chủ đề dạng cây. Chưa có cây chính thức; xem [bản thảo taxonomy](docs/11-topic-taxonomy.md). ABSA, sentiment và trích xuất thương hiệu như tác vụ riêng đã được bỏ khỏi kế hoạch.

**Trạng thái:** đã có bộ khung local với Kafka, Spark Structured Streaming, PostgreSQL, AI service, worker, API, dashboard và Airflow điều phối replay. Demo dùng dữ liệu tổng hợp và baseline luật `rules-v1`; chưa kết nối YouTube thật hoặc triển khai mô hình AI nghiên cứu.

Runtime/dashboard/test hiện vẫn thuộc prototype cũ, còn nhãn phẳng và các trường brand/opinion. Tài liệu đã chuyển sang phạm vi mới; code chưa phải classifier chủ đề phân cấp.

## Chạy nhanh

Yêu cầu Docker Desktop chạy Linux containers. Từ thư mục gốc:

```powershell
Copy-Item .env.example .env
docker compose up -d --build
docker compose run --rm replay
```

Mở <http://localhost:8000>, chọn run `demo` và nạp danh sách sau khi pipeline xử lý xong. API docs tại <http://localhost:8000/docs>. Lần đầu cần tải image và Spark Kafka connector.

Xem [hướng dẫn phát triển](docs/09-development.md) để chạy kiểm tra, xem log, thay cấu hình và hiểu các giới hạn của bộ khung.

Airflow UI: <http://localhost:8080>, user `admin`, mật khẩu local mặc định `airflow_local_dev`. DAG `kol_replay_pipeline` mặc định pause; unpause để scheduler thực thi các lượt chạy, rồi pause lại sau khi demo hoàn tất. Xem [hướng dẫn Airflow](docs/10-airflow.md) về trigger, lịch và run ID.

## Phạm vi khởi đầu

- Xây và xác nhận cây chủ đề, độ sâu và chính sách một/nhiều nhánh mỗi nội dung.
- Pilot nội dung bài đăng/video từ nguồn có thể thu thập; khảo sát độ phủ nhãn trước khi mở rộng nhiều nền tảng.
- Phân loại nội dung vào đường dẫn hợp lệ và cập nhật profile theo node/thời gian; xem lại được bài nguồn.
- Bình luận và engagement không phải đầu vào bắt buộc của AI; ưu tiên dữ liệu nội dung.
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
| [Thiết lập và phát triển](docs/09-development.md) | Chạy local, kiểm tra và trạng thái triển khai |
| [Điều phối Airflow](docs/10-airflow.md) | Thành phần Airflow, DAG replay và cách vận hành |
| [Bản thảo taxonomy](docs/11-topic-taxonomy.md) | Cây minh họa và các quy tắc nhãn cần chốt |

## Nguyên tắc triển khai

Ưu tiên một luồng end-to-end hoạt động được trước khi mở rộng tính năng. Mọi kết luận trên dashboard cần gắn với dữ liệu nguồn, khoảng thời gian và phiên bản phân tích. Dữ liệu replay và dữ liệu thu thập trực tiếp phải được phân biệt rõ trong demo và báo cáo.
