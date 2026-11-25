# Lộ trình triển khai

Các tuần là mốc tương đối theo học kỳ, chưa gán ngày hoặc người phụ trách. Điều chỉnh sau khi biết lịch môn, nhân sự và tài nguyên.

| Giai đoạn | Công việc chính | Sản phẩm và điều kiện chuyển bước |
| --- | --- | --- |
| Tuần 1–2 | Pilot 2–3 kênh, kiểm tra API, thử nhãn khoảng 200 comment, chọn lĩnh vực | Proposal, data audit, hướng dẫn nhãn v1; xác nhận thu thập khả thi |
| Tuần 3–5 | Thu thập/làm sạch/gán nhãn, chia tập, dựng baseline và Kafka/Spark tối thiểu | Dataset manifest, train/dev/test tách biệt, luồng raw → storage hoạt động |
| Tuần 6–9 | AI service, worker, result stream, profile, API/dashboard | End-to-end có dẫn chứng; duplicate/retry được xử lý; có baseline report |
| Tuần 10–12 | Thực nghiệm AI, đo tải, phục hồi và dữ liệu đến muộn | Kết quả có thể tái lập; lỗi nghiêm trọng đã xử lý; quyết định mở rộng media |
| Tuần 13–15 | Hoàn thiện demo, báo cáo, hướng dẫn chạy và slide | Demo live/replay rõ ràng, đối chiếu yêu cầu và bằng chứng nghiệm thu |

## Backlog đầu tiên

- [ ] Ghi số thành viên, tài nguyên CPU/RAM/GPU và ngân sách API.
- [ ] Chọn lĩnh vực và 2–3 kênh pilot.
- [ ] Thiết lập thông tin truy cập qua biến môi trường và kiểm tra API.
- [ ] Thu metadata, comment và engagement mẫu; ghi quota/lỗi/dữ liệu thiếu.
- [ ] Soạn taxonomy và hướng dẫn nhãn bằng ví dụ thực tế.
- [ ] Gán thử khoảng 200 bình luận, rà soát bất đồng.
- [ ] Chốt schema event và quy tắc version/idempotency.
- [ ] Dựng luồng collector/replay → Kafka → Spark → storage.
- [ ] Khóa các mục tiêu pilot và tiêu chí nghiệm thu định lượng.

## Thứ tự tích hợp

1. Collector/replay → Kafka → Spark → dữ liệu chuẩn hóa.
2. AI request → worker/service → output được kiểm tra schema.
3. AI result → profile có idempotency → API.
4. Dashboard → dẫn chứng → số liệu freshness và xử lý chưa hoàn tất.
5. Kiểm thử lỗi, đo tải và so sánh AI.

## Bộ sản phẩm bàn giao

- Proposal: bối cảnh, nguồn dữ liệu, AI workload và lý do dùng Big Data.
- Data plan và dataset manifest; hướng dẫn nhãn, thống kê và cách chia tập.
- Sơ đồ kiến trúc, hợp đồng sự kiện và mô tả triển khai AI.
- Source code, cấu hình mẫu không chứa secret, hướng dẫn chạy và demo.
- Báo cáo AI và hệ thống, baseline/ablation, phân tích lỗi và giới hạn scale-up.
- Slide và kịch bản demo end-to-end.

## Điều kiện mở rộng

Chỉ mở rộng transcript/keyframe sau khi pipeline chính chạy được, dữ liệu có nhãn dùng để đánh giá và nguồn media khả thi. Nếu đổi phạm vi, cập nhật proposal và ma trận đánh giá trước khi triển khai phần thêm.
