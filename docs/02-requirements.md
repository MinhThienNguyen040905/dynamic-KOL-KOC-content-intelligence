# Yêu cầu và điều kiện nghiệm thu

## Căn cứ ưu tiên

Ngày **25/11/2026**, nhóm xác nhận giảng viên giới hạn AI của đề tài vào **phân loại chủ đề theo cây**. Áp dụng chỉ đạo này thay cho yêu cầu AI rộng hơn trong đề xuất ban đầu. Giữ pipeline streaming/near-real-time và đánh giá hệ thống của SE363.

Taxonomy chưa được giảng viên cung cấp. Chưa chốt một nội dung có một hay nhiều đường dẫn nhãn, số tầng và khả năng dừng ở nút cha. Không xem cây minh họa là yêu cầu chính thức.

## Yêu cầu chức năng mục tiêu

Các ID dưới đây được giữ để tiện đối chiếu, nhưng nội dung FR-04/05/07 đã thay đổi theo phạm vi mới.

| ID | Yêu cầu | Minh chứng nghiệm thu |
| --- | --- | --- |
| FR-01 | Quản lý nguồn/tài khoản KOL theo dõi | Collector dùng đúng cấu hình |
| FR-02 | Thu thập bài đăng/video và metadata cần cho phân loại | Có nguồn, ID, timestamp và trạng thái dữ liệu thiếu; comment/engagement không bắt buộc |
| FR-03 | Đưa dữ liệu qua Kafka và Spark | Truy vết được input đến kết quả |
| FR-04 | Phân loại chủ đề theo cây đã chốt | Đường dẫn gồm các node hợp lệ và đúng quan hệ cha–con |
| FR-05 | Quản lý phiên bản taxonomy và các trường hợp chưa phân loại được | Có taxonomy ID/version, trạng thái thiếu thông tin/ngoài cây; không tự sinh nhãn |
| FR-06 | Cập nhật profile chủ đề theo KOL/thời gian | Không đếm trùng; phiên bản phân tích cũ không cộng vào kết quả hiện hành |
| FR-07 | Lọc theo KOL, thời gian và nhánh chủ đề | Lọc nút cha truy xuất đúng các nội dung thuộc nhánh con |
| FR-08 | Mở nội dung nguồn từ số liệu tổng hợp | Xem ID, link, văn bản nguồn và đường dẫn nhãn |
| FR-09 | Replay để demo và kiểm tra tải | Run ID, mode và cấu hình replay được ghi nhận |

## Yêu cầu phi chức năng

| ID | Yêu cầu | Minh chứng nghiệm thu |
| --- | --- | --- |
| NFR-01 | Idempotency | Gửi lại input không tăng số nội dung hoặc đóng góp vào profile |
| NFR-02 | Chính sách dữ liệu đến muộn | Kiểm thử cập nhật và reconciliation theo thiết kế đã triển khai |
| NFR-03 | Phục hồi sau restart | Khôi phục checkpoint và đối soát input/completed/pending/DLQ |
| NFR-04 | Lỗi inference không làm mất input | Retry có giới hạn, DLQ và xử lý lại được |
| NFR-05 | Đo hiệu năng | p50/p95 latency, throughput, lag, lỗi và tài nguyên |
| NFR-06 | Tái lập | Ghi code/model/taxonomy/data version, tham số và cấu hình |
| NFR-07 | Quản lý secret | Biến môi trường; không commit credential |
| NFR-08 | Tính hợp lệ phân cấp | Không chu trình, không node mồ côi; output không chứa đường dẫn không tồn tại |

## Quy tắc hiển thị và tổng hợp

- Hiển thị cây, số mẫu, khoảng thời gian và phiên bản taxonomy/model đang xem.
- Đếm một nội dung tối đa một lần tại mỗi node, dù nhiều đường dẫn cùng đi qua node đó.
- Nếu đa nhãn, các nhánh có thể chồng lấp; tỷ lệ của các nhánh không nhất thiết cộng thành 100%.
- Hiển thị riêng pending, thiếu thông tin và ngoài taxonomy; không ép chúng vào một chủ đề.
- Không so sánh trực tiếp số liệu dùng taxonomy khác phiên bản khi chưa có mapping hoặc phân loại lại.
- Nếu còn hiển thị engagement, giữ snapshot và định nghĩa mẫu số riêng; không dùng chúng để suy ra chủ đề.

## Điều kiện hoàn thành MVP

Cây và chính sách gán nhãn được chốt; có tập nhãn được kiểm tra, test set tách biệt, baseline và kết quả phân cấp. FR-01 đến FR-09 và NFR-01 đến NFR-08 có minh chứng phù hợp. Demo dữ liệu mới cập nhật nhánh chủ đề/profile; có báo cáo AI và hệ thống. Ngưỡng chất lượng/hiệu năng chốt sau pilot, trước đánh giá cuối.

Các test của prototype cũ chỉ chứng minh luồng tích hợp cũ; chưa nghiệm thu classifier phân cấp.
