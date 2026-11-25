# Quyết định và rủi ro

Ngày ghi nhận ban đầu: **25/11/2026**. Các lựa chọn dưới đây phản ánh hướng triển khai hiện tại, chưa phải kết quả thực nghiệm.

## Nhật ký quyết định

| ID | Lựa chọn | Trạng thái | Căn cứ / khi xem xét lại |
| --- | --- | --- | --- |
| D-01 | Giữ đề tài Dynamic KOL/KOC Content Intelligence | Đã thống nhất hướng | Đúng tên project và đề tài gợi ý số 13 |
| D-02 | Một nền tảng YouTube, một lĩnh vực | Kế hoạch ban đầu | Pilot API/dữ liệu trước khi mở rộng |
| D-03 | Hai phần AI: nội dung và tuple ABSA | Kế hoạch ban đầu | Tạo profile có dẫn chứng và tránh sentiment đơn lẻ |
| D-04 | Served AI qua worker và Kafka request/result | Đã có bộ khung local | Luồng end-to-end đã chạy với baseline; cần đo tải và kiểm thử lỗi thêm |
| D-05 | PostgreSQL phục vụ ứng dụng; archive raw Parquet | Đã có bộ khung local | Có snapshot và bản ghi canonical; bổ sung export normalized khi cần |
| D-06 | Dashboard theo thời gian, có dẫn chứng | Đã có bản tối thiểu | API có bộ lọc thời gian và dẫn chứng; chưa kiểm tra trực quan bằng browser |
| D-07 | Bắt đầu bằng văn bản, mở rộng transcript/keyframe sau | Kế hoạch ban đầu | Nguồn media và tài nguyên chưa được xác nhận |
| D-08 | Chưa đưa RAG, recommendation, multi-agent vào MVP | Giới hạn phạm vi | Ưu tiên hoàn tất và đánh giá luồng chính |
| D-09 | Airflow 3.1.8, LocalExecutor và metadata database riêng | Đã bổ sung cấu hình và DAG replay | Điều phối tác vụ hữu hạn; DAG mẫu pause mặc định, không tự khởi động lại service streaming |

## Rủi ro cần kiểm chứng

| Rủi ro | Tác động | Hành động |
| --- | --- | --- |
| API/quota hoặc comment không khả dụng | Thiếu dữ liệu liên tục | Pilot sớm, lưu lỗi, chọn kênh phù hợp, có replay từ dữ liệu thật |
| Không lấy được transcript/media | Chậm phần multimodal | Xác minh riêng nguồn; hoàn tất text pipeline và ghi đúng giới hạn |
| Ít bình luận có ý kiến theo aspect | Nhãn thưa, đánh giá khó | Đo tỷ lệ trên pilot; chọn video/lĩnh vực phù hợp và ghi cách lấy mẫu |
| Tiếng lóng, mỉa mai, nhiều thực thể | Sai sentiment/entity | Hướng dẫn nhãn rõ, thêm ngữ cảnh và phân tích lỗi theo nhóm |
| Inference chậm hoặc tốn chi phí | Backlog tăng | Batch/cache, model phù hợp tài nguyên, đo trước khi mở rộng |
| Trùng/sửa dữ liệu hoặc reprocess | Profile sai số đếm | Version, unique key và reconciliation aggregate |
| Rò rỉ train/test | Điểm AI quá lạc quan | Chia theo video/thread/thời gian, kiểm tra duplicate |
| Snapshot tương tác bị cộng lặp | Nhận định tăng trưởng sai | Lưu snapshot và tính chênh lệch có khoảng đo |
| Thêm quá nhiều tính năng | Thiếu demo end-to-end | Dùng điều kiện mở rộng trong roadmap |

## Các quyết định còn mở

- Lĩnh vực, danh sách kênh, khoảng thời gian và chu kỳ polling.
- Quy mô nhãn sau pilot, cách tổ chức gán nhãn và phân xử.
- Model, prompt, cách huấn luyện/fine-tune nếu có, tài nguyên và chi phí.
- Ngưỡng chấp nhận AI, latency, throughput, freshness và watermark.
- Chính sách giữ/xóa dữ liệu và tập dữ liệu có thể chia sẻ trong báo cáo.
- Phân công thành viên và thời hạn thực tế.

Mỗi lần thay đổi cần ghi ngày, lý do, bằng chứng và tài liệu bị ảnh hưởng. Không đánh dấu một lựa chọn là đã kiểm chứng khi mới có thiết kế.
