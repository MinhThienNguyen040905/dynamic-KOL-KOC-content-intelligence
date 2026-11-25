# Yêu cầu và điều kiện nghiệm thu

## Yêu cầu môn học

- Có bối cảnh streaming, near-real-time hoặc dữ liệu liên tục cập nhật.
- Sử dụng hợp lý Kafka, Spark Structured Streaming, storage và AI inference/service.
- AI có chiều sâu kỹ thuật; tránh chỉ làm classification đơn lẻ.
- Đánh giá chất lượng AI, hiệu năng hệ thống và tính hợp lý khi mở rộng.
- Demo pipeline end-to-end; có đề cương, kế hoạch dữ liệu và sơ đồ kiến trúc.

Không yêu cầu tạo Big Data thực sự trên hạ tầng lớp học. Phải chứng minh vai trò kiến trúc bằng thiết kế và thực nghiệm ở quy mô khả thi.

## Yêu cầu chức năng đề xuất

| ID | Yêu cầu | Minh chứng nghiệm thu |
| --- | --- | --- |
| FR-01 | Quản lý danh sách kênh theo dõi | Thêm hoặc vô hiệu hóa kênh qua cấu hình, collector sử dụng đúng cấu hình |
| FR-02 | Thu thập metadata video, bình luận và snapshot tương tác theo chu kỳ | Có bản ghi nguồn, thời điểm lấy dữ liệu, lỗi và tiến độ thu thập |
| FR-03 | Đưa dữ liệu vào Kafka và xử lý bằng Spark | Truy vết được một sự kiện từ nguồn đến bản ghi kết quả |
| FR-04 | Phân tích chủ đề và thương hiệu | Kết quả có nhãn, nguồn bằng chứng, phiên bản model và trạng thái xử lý |
| FR-05 | Phân tích bình luận theo entity/aspect/opinion/sentiment | Một bình luận có thể chứa nhiều tuple, từng tuple có đoạn bằng chứng |
| FR-06 | Cập nhật profile theo thời gian | Dữ liệu mới làm thay đổi đúng profile, có thời điểm cập nhật và số mẫu |
| FR-07 | Lọc theo KOL, khoảng thời gian, chủ đề và thương hiệu | API/dashboard trả kết quả khớp dữ liệu kiểm chứng |
| FR-08 | Mở dẫn chứng từ kết quả tổng hợp | Xem được trích đoạn và liên kết nguồn nếu nguồn còn tồn tại |
| FR-09 | Replay dữ liệu để demo và đo tải | Có tốc độ replay, seed nếu dùng ngẫu nhiên, run ID và nhãn replay |

## Yêu cầu phi chức năng đề xuất

| ID | Yêu cầu | Minh chứng nghiệm thu |
| --- | --- | --- |
| NFR-01 | Xử lý lặp có tính idempotent | Phát lại cùng sự kiện không làm tăng đếm hoặc tạo tuple trùng |
| NFR-02 | Có chính sách dữ liệu đến muộn | Kiểm thử trước/sau watermark và ghi nhận dữ liệu cần tính lại |
| NFR-03 | Có thể phục hồi sau restart | Khôi phục checkpoint, xử lý tiếp, đối soát số sự kiện và kết quả |
| NFR-04 | AI service lỗi không làm mất dữ liệu | Retry có giới hạn, DLQ và khả năng xử lý lại |
| NFR-05 | Đo được hiệu năng | Báo cáo p50/p95 latency, throughput, lag, tỷ lệ lỗi và cấu hình chạy |
| NFR-06 | Có thể tái lập thực nghiệm | Ghi phiên bản code/model/data, tham số, tài nguyên và lệnh chạy |
| NFR-07 | Quản lý cấu hình và thông tin truy cập | Dùng biến môi trường; không commit API key hoặc credential |

## Quy tắc hiển thị

- Tách cảm xúc về KOL khỏi cảm xúc về sản phẩm hoặc thương hiệu.
- Hiển thị khoảng thời gian, số bình luận đã phân tích và số bình luận chưa xử lý.
- Dữ liệu thiếu hoặc chưa đủ mẫu phải được thể hiện rõ; không mặc định thành trung lập.
- Nhận định tăng/giảm phải có khoảng đối chiếu và mẫu số; không so sánh số đếm của hai khoảng dài khác nhau mà không chuẩn hóa.
- Chỉ số tương tác từ nhiều lần thu thập là snapshot, không cộng tổng trực tiếp.

## Điều kiện hoàn thành MVP

FR-01 đến FR-09 có minh chứng; NFR-01 đến NFR-07 được kiểm tra ở mức phù hợp. Có test set tách biệt, baseline, báo cáo AI/hệ thống và demo dữ liệu mới cập nhật profile có dẫn chứng. Ngưỡng F1, latency và throughput sẽ được chốt sau pilot, trước thực nghiệm cuối cùng.
