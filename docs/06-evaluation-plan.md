# Kế hoạch đánh giá

## Mục tiêu

Đánh giá **phân loại chủ đề theo cây** và pipeline streaming. Các tiêu chí ABSA/sentiment/entity extraction của kế hoạch cũ không còn áp dụng. Khóa taxonomy, chính sách nhãn, dataset split và mục tiêu trước khi chạy test cuối.

## Chất lượng AI

| Chỉ số | Định nghĩa dùng cho project |
| --- | --- |
| F1 từng tầng | Micro/macro F1 trên các node tại cùng độ sâu; báo support và coverage |
| Đúng toàn đường dẫn | Tỷ lệ input có đường dẫn dự đoán khớp hoàn toàn ground truth; nếu đa nhãn dùng exact set match |
| F1 lá/nhãn kết thúc | Đo ở mức chi tiết đã thống nhất, tách khỏi điểm tổ tiên |
| Hierarchical precision/recall/F1 | Mở rộng nhãn dự đoán/thật bằng tổ tiên, bỏ root kỹ thuật, rồi tính giao giữa hai tập node |
| Tỷ lệ đường dẫn không hợp lệ | Tỷ lệ output chứa node không tồn tại hoặc quan hệ cha–con sai |
| Coverage và từ chối | Tỷ lệ đã phân loại, thiếu thông tin, ngoài taxonomy và cần rà soát |

Với tập node mở rộng P (dự đoán) và T (nhãn thật), hierarchical precision dùng `|P ∩ T| / |P|`, recall dùng `|P ∩ T| / |T|`; F1 là trung bình điều hòa. Khóa cách micro/macro aggregation và xử lý tập rỗng trước thực nghiệm. Root không được cộng điểm. Trạng thái từ chối được báo riêng, không coi hai tập rỗng là dự đoán đúng chủ đề.

Nếu cho phép dừng ở node cha, báo đúng ở cấp đó và coverage ở cấp sâu; không dùng điểm tổ tiên để che lỗi phân loại chi tiết. Với taxonomy có độ sâu không đều, ghi số mẫu được đánh giá tại mỗi tầng.

## Thực nghiệm

- Baseline dự đoán phẳng và suy tổ tiên so với phương án khai thác cây, trên cùng input/test.
- Phân tích lỗi: nhầm cùng node cha, nhầm khác nhánh cấp cao, thiếu ngữ cảnh, đa chủ đề và nhãn hiếm.
- Nếu có media: so sánh text-only với thêm transcript/OCR/thông tin ảnh, giữ cùng test và ghi chi phí/latency.
- Chọn tham số/ngưỡng trên dev; không sửa cây sau khi xem test để tăng điểm.
- Báo support theo node, phương pháp gán nhãn/phân xử và giới hạn dữ liệu.

## Hiệu năng hệ thống

| Chỉ số | Định nghĩa |
| --- | --- |
| Processing latency | `ingested_at` đến kết quả sẵn sàng qua API; p50/p95 |
| Collection freshness | Thời gian nguồn đến lúc collector quan sát; tách khỏi thời gian xử lý |
| Input/completed throughput | Số nội dung nhận/xử lý xong mỗi giây, không dùng số node nhãn thay số nội dung |
| Kafka lag / AI backlog | Offset lag, số request chờ và tuổi request lâu nhất |
| Error rate | Tỷ lệ lỗi theo bước, retry và DLQ |
| Resource use | CPU/RAM/GPU và chi phí API nếu có |

## Kiểm tra tính đúng

1. Gửi lại cùng event: không tăng số content hoặc số đếm node.
2. Sửa nội dung hoặc chạy lại model: chỉ phiên bản phân tích hiện hành đóng góp vào profile.
3. Output node sai cây hoặc taxonomy version không hợp lệ: bị từ chối/ghi lỗi rõ ràng.
4. Đa nhãn có chung tổ tiên: không đếm lặp tổ tiên; nếu đơn nhãn, từ chối nhiều đường dẫn.
5. Dữ liệu muộn/restart: khôi phục checkpoint và đối soát input/completed/pending/DLQ.
6. AI timeout/schema lỗi/database ngắt: kiểm tra retry và xử lý lại.
7. Taxonomy đổi: không trộn thống kê khác version; có mapping hoặc kế hoạch phân loại lại.

## Tải và tái lập

Replay dataset ở tải tăng dần; có burst lệch về một KOL, cấu hình gốc và cấu hình tăng tài nguyên. Tách cold start/warm-up, model thật và mock. Ghi code commit, model/taxonomy/data version, hardware, cấu hình Kafka/Spark, tốc độ/timestamp replay, raw metrics và lỗi.

Mức tải và thời lượng chốt sau pilot. Demo nhỏ chưa chứng minh hỗ trợ hàng nghìn tài khoản.

## Demo nghiệm thu

Nạp nội dung mới → xuất đường dẫn chủ đề → thấy profile theo cây cập nhật → lọc một node cha để xem nội dung ở các nhánh con → mở nguồn → gửi lại event để chứng minh không đếm trùng. Hiển thị run/mode, taxonomy/model version và số input chưa phân loại được.

Các kiểm tra prototype cũ không thay thế đánh giá classifier phân cấp.
