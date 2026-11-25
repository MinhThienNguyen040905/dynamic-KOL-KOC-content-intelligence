# Quyết định và rủi ro

Cập nhật phạm vi ngày **25/11/2026**, theo thông tin mới từ nhóm về giới hạn giảng viên. Giữ lịch sử quyết định nhưng phân biệt lựa chọn đã bị thay thế và mục tiêu chưa triển khai.

## Nhật ký quyết định

| ID | Lựa chọn | Trạng thái | Căn cứ / khi xem xét lại |
| --- | --- | --- | --- |
| D-01 | Dynamic KOL/KOC Content Intelligence | Giữ hướng ứng dụng | Đầu ra hiện tập trung vào profile chủ đề |
| D-02 | Pilot YouTube trước | Chưa chốt nguồn cuối | Nhóm muốn mở rộng đa nền tảng; nguồn thật phụ thuộc khả năng truy cập |
| D-03 | Hai phần AI: nội dung và tuple ABSA | Đã bị thay thế | Giới hạn mới của giảng viên: chỉ phân loại chủ đề theo cây |
| D-04 | Served AI qua worker và Kafka request/result | Đã có bộ khung local | Tái sử dụng cho classifier chủ đề phân cấp |
| D-05 | PostgreSQL và archive raw Parquet | Đã có bộ khung local | Giữ version/idempotency khi đổi output |
| D-06 | Dashboard theo thời gian | Prototype cần chỉnh | Chuyển sang cây chủ đề, phân bố và nội dung nguồn |
| D-07 | Bắt đầu từ text, bổ sung media khi cần | Kế hoạch có điều kiện | Media chỉ phục vụ cùng tác vụ phân loại chủ đề |
| D-08 | Không thêm RAG/recommendation/multi-agent | Giữ giới hạn | Không mở rộng AI ngoài chủ đề |
| D-09 | Airflow 3.1.8 và metadata DB riêng | Đã chạy DAG replay | Giữ orchestration, cập nhật manifest/test khi đổi schema |
| D-10 | AI chỉ phân loại chủ đề phân cấp | Phạm vi hiện hành | Theo chỉ đạo riêng cho đề tài mà nhóm xác nhận |
| D-11 | Taxonomy chưa có | Chờ xây dựng và xác nhận | Cây minh họa không phải cây được giảng viên cung cấp |
| D-12 | Comment/engagement không bắt buộc cho AI | Giả định lập kế hoạch | Chưa có yêu cầu phân loại riêng bình luận; ưu tiên bài đăng/video |

## Rủi ro

| Rủi ro | Tác động | Hành động |
| --- | --- | --- |
| Cây chưa rõ ranh giới, số tầng hoặc chính sách đa nhãn | Nhãn không nhất quán | Xây định nghĩa/ví dụ và xác nhận trước khi gán nhãn lớn |
| Nhánh quá nhỏ/thiếu dữ liệu | Không đủ để train/đánh giá | Đo support, cân nhắc gộp nhánh bằng train/dev trước khi khóa taxonomy |
| Chọn sai node cha | Sai cả nhánh chi tiết | Báo lỗi từng tầng và đường dẫn; so sánh baseline phẳng |
| Thiếu caption/transcript/media | Không xác định được chủ đề | Ghi trạng thái thiếu thông tin; đo coverage |
| Cross-post và nội dung cắt lại | Rò rỉ train/test | Group theo nội dung gốc, rà soát duplicate đa nền tảng |
| Taxonomy đổi giữa các lượt phân tích | Profile không so sánh được | Version cây, mapping hoặc phân loại lại |
| Đa nhãn bị đếm trùng tại tổ tiên | Phân bố chủ đề sai | Một content/node chỉ đóng góp một lần |
| Giữ nhầm chức năng sentiment từ prototype | Sai phạm vi nghiệm thu | Chuyển schema/UI/test và loại khỏi luồng mục tiêu |
| Quota, inference chậm, backlog | Dữ liệu chậm hoặc thiếu | Pilot nguồn và đo tải trước khi mở rộng |

## Chưa chốt

- Cây chính thức: nhóm tự đề xuất để duyệt hay giảng viên sẽ cung cấp.
- Một hay nhiều nhánh mỗi content; cho phép dừng node cha; cách xử lý ngoài cây.
- Phạm vi chủ đề, nguồn và đơn vị phân loại cuối cùng.
- Nhân sự, tài nguyên, số mẫu, model và cách training/fine-tune.
- Mục tiêu AI/latency/throughput sau pilot.

Thay đổi phạm vi phải được phản ánh trong proposal, nhãn, hợp đồng AI, profile và đánh giá. Tài liệu cập nhật không đồng nghĩa runtime cũ đã được chuyển đổi.
