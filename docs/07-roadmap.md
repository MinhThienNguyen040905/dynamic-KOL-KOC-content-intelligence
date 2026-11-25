# Lộ trình triển khai

Các tuần là mốc tương đối theo học kỳ, chưa gán ngày hoặc người phụ trách. Điều chỉnh sau khi biết lịch môn, nhân sự và tài nguyên.

**Ưu tiên hiện tại:** chốt cây chủ đề với giảng viên trước khi gán nhãn quy mô lớn hoặc sửa hợp đồng AI. Model/profile/dashboard phải chuyển từ prototype cũ sang phân loại chủ đề phân cấp; ABSA và sentiment đã ra khỏi phạm vi.

| Giai đoạn | Công việc chính | Sản phẩm và điều kiện chuyển bước |
| --- | --- | --- |
| Tuần 1–2 | Khảo sát khoảng 200 nội dung, đề xuất cây và chính sách nhãn, kiểm tra nguồn | Taxonomy được xác nhận, data audit, hướng dẫn nhãn v1 |
| Tuần 3–5 | Thu thập/làm sạch/gán nhãn, chia tập, dựng baseline và Kafka/Spark tối thiểu | Dataset manifest, train/dev/test tách biệt, luồng raw → storage hoạt động |
| Tuần 6–9 | Classifier phân cấp, schema kết quả, profile cây và dashboard | End-to-end chủ đề có nội dung nguồn, version và idempotency; baseline report |
| Tuần 10–12 | Thực nghiệm AI, đo tải, phục hồi và dữ liệu đến muộn | Kết quả có thể tái lập; lỗi nghiêm trọng đã xử lý; quyết định mở rộng media |
| Tuần 13–15 | Hoàn thiện demo, báo cáo, hướng dẫn chạy và slide | Demo live/replay rõ ràng, đối chiếu yêu cầu và bằng chứng nghiệm thu |

## Backlog đầu tiên

- [ ] Ghi số thành viên, tài nguyên CPU/RAM/GPU và ngân sách API.
- [ ] Xác nhận phạm vi cây, số tầng, đơn nhãn/đa nhãn và nhãn ở node cha.
- [ ] Chọn nguồn và tài khoản pilot có nội dung bao phủ các nhánh cần khảo sát.
- [ ] Thiết lập thông tin truy cập qua biến môi trường và kiểm tra API.
- [ ] Thu nội dung và metadata cần phân loại; ghi quota/lỗi/dữ liệu thiếu.
- [ ] Soạn taxonomy và hướng dẫn nhãn bằng ví dụ thực tế, trình giảng viên xác nhận.
- [ ] Gán thử khoảng 200 bài đăng/video, rà soát bất đồng và số mẫu mỗi node.
- [ ] Chuyển AI contract, sample, profile, dashboard và test sang kết quả chủ đề theo cây.
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
