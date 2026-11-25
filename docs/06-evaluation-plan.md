# Kế hoạch đánh giá

## Nguyên tắc

Tách đánh giá AI khỏi đánh giá pipeline. Dùng cùng tập test cho các phương án AI so sánh; dùng cấu hình và workload được ghi nhận cho các lần đo hệ thống. Mục tiêu định lượng được đặt sau pilot và khóa trước thực nghiệm cuối, không điều chỉnh theo kết quả test.

## Chất lượng AI

| Tác vụ | Chỉ số chính | Phân tích bổ sung |
| --- | --- | --- |
| Chủ đề đa nhãn | Micro/macro F1 | F1 theo nhãn, support, lỗi nhãn hiếm |
| Brand/entity mention | Precision/recall/F1 theo span | Exact match chính; overlap chỉ là bổ sung |
| Entity linking | Accuracy trên mention có ID chuẩn | Coverage, trường hợp không xác định |
| Aspect và sentiment | F1 theo thành phần | Macro F1, confusion matrix, support |
| Opinion span | Span precision/recall/F1 | Exact match và overlap báo riêng |
| Tuple ABSA | Precision/recall/F1 tuple end-to-end | Định nghĩa khớp entity/aspect/span/sentiment trước khi chạy |

Quy định cách xử lý thực thể ngầm định và một-một khi ghép tuple dự đoán với nhãn. Báo cả số mẫu và độ bất định khi dữ liệu cho phép. Chất lượng sentiment trên tuple đã khớp không được thay thế điểm end-to-end.

## Ma trận thực nghiệm AI

- A: baseline nội dung và baseline tuple chỉ dùng bình luận.
- B: trích xuất tuple có ngữ cảnh nội dung.
- C, nếu triển khai: bổ sung transcript/keyframe.

Chọn tham số trên dev; đánh giá test đã khóa; lưu dự đoán để so sánh lỗi trên cùng mẫu. Nhãn model hỗ trợ phải được con người kiểm tra, không dùng output cùng model làm ground truth tự động.

## Hiệu năng hệ thống

| Chỉ số | Định nghĩa |
| --- | --- |
| Processing latency | Từ `ingested_at` đến kết quả sẵn sàng qua API; báo p50/p95 |
| Collection freshness | Từ thời gian nguồn đến lúc collector quan sát; tách khỏi processing latency |
| Throughput đầu vào | Số sự kiện nhận/giây theo loại sự kiện |
| Throughput hoàn tất | Số input được xử lý thành công/giây; không dùng số tuple thay số input |
| Kafka lag | Chênh lệch offset producer/consumer theo topic/partition |
| AI backlog | Số request chờ và tuổi request lâu nhất |
| Error rate | Lỗi/tổng request theo công đoạn, kèm retry và DLQ |
| Resource use | CPU/RAM; GPU và chi phí API nếu có |

Không gọi thời gian từ lúc đăng video đến dashboard là riêng độ trễ Spark. Với video cũ mới được phát hiện, ghi rõ ảnh hưởng của backfill và polling.

## Kịch bản kiểm tra tính đúng

1. Gửi hai lần cùng event: số nội dung và đóng góp profile không đổi.
2. Sửa bình luận hoặc chạy lại model: phiên bản cũ không được cộng thêm vào aggregate hiện hành.
3. Event đến muộn trong ngưỡng và ngoài ngưỡng: kiểm tra cập nhật, ghi nhận và tính lại theo chính sách.
4. Restart Spark/worker: đối soát input, completed, pending và DLQ; không chỉ kiểm tra process đã chạy lại.
5. AI timeout, output sai schema hoặc database tạm ngắt: kiểm tra retry và khả năng xử lý lại.
6. Snapshot tương tác lặp, thiếu field hoặc số đếm giảm: không cộng sai và không biến thiếu thành 0.

## Kịch bản tải

- Replay cùng dataset ở tải tăng dần; xác định mức tải bền vững khi backlog không tăng liên tục.
- Gửi burst có một KOL chiếm tỷ trọng lớn để kiểm tra lệch tải.
- So sánh một cấu hình gốc với cấu hình tăng worker hoặc partition; giữ các yếu tố khác ổn định.
- Đo cold start riêng, warm-up trước phép đo ổn định; đề xuất lặp ít nhất ba lần nếu tài nguyên cho phép.
- Chạy một lượt dùng model thật; lượt mock inference chỉ dùng cô lập bottleneck và phải được ghi nhãn.

Tốc độ cụ thể, thời lượng và cấu hình chốt sau pilot. Báo giới hạn máy thử nghiệm; không suy ra đã hỗ trợ hàng nghìn kênh từ một demo nhỏ.

## Hồ sơ thực nghiệm cần lưu

Mỗi run có code commit, dataset manifest, model/prompt/taxonomy version, tham số Spark/Kafka, hardware, tốc độ replay, chế độ timestamp, warm-up, thời gian đo, raw metrics và lỗi. Báo cáo cuối liên kết được biểu đồ với run tương ứng.

## Bản demo nghiệm thu

Chọn KOL và khoảng thời gian → nạp dữ liệu mới → quan sát trạng thái xử lý → profile thay đổi → mở bằng chứng → gửi lại sự kiện để chứng minh không đếm trùng. Hiển thị rõ chế độ live/replay và độ trễ đo được.
