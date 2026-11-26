# Kế hoạch dữ liệu

## Đơn vị dữ liệu và nhãn

Theo phạm vi giảng viên giới hạn, tập nhãn phục vụ **phân loại chủ đề dạng cây**. Đơn vị dự kiến là một bài đăng/video. Bình luận và engagement không phải điều kiện bắt buộc của dataset phân loại chủ đề.

Giảng viên chưa cung cấp taxonomy. Phải chốt cây, độ sâu, đơn nhãn/đa nhãn và quy tắc nhãn ở node cha trước khi gán nhãn quy mô lớn; xem [taxonomy](11-topic-taxonomy.md).

## Pilot

1. Thu thập nội dung từ nguồn có quyền truy cập, khảo sát độ phủ chủ đề và dữ liệu thiếu.
2. Lấy khoảng 200 nội dung để xây/điều chỉnh định nghĩa nhãn và ví dụ ranh giới.
3. Thử gán nhãn độc lập một phần, phân xử bất đồng, xác định các nhánh quá hẹp hoặc chồng lấn.
4. Xác nhận taxonomy với giảng viên rồi đóng băng phiên bản cho thực nghiệm.
5. Chốt quy mô tập train/dev/test theo số lớp, phân bố và tài nguyên.

Mốc 200 là khảo sát, chưa chứng minh đủ dữ liệu để train. Không mặc định giữ phạm vi chỉ một lĩnh vực nếu taxonomy cần phân biệt nhiều nhóm cấp cao.

## Trường dữ liệu mục tiêu

| Nhóm | Trường chính |
| --- | --- |
| Creator/account | ID KOL, nền tảng, ID tài khoản nguồn và liên kết ánh xạ đã xác nhận |
| Content | ID nguồn, loại nội dung, tiêu đề/caption/text/mô tả, URL, thời gian và input version |
| Media tùy chọn | Storage URI, loại media, transcript/OCR, provenance và version công cụ trích xuất |
| Topic label | Content ID/version, taxonomy version, đường dẫn node ID, annotator, trạng thái và kết quả phân xử |
| Analysis | Input/model/taxonomy version, đường dẫn dự đoán, trạng thái, thời gian xử lý |
| Engagement tùy chọn | Snapshot theo nền tảng và thời điểm quan sát; tách khỏi nhãn AI |

Giữ text nguồn và text chuẩn hóa ở các trường riêng. Metadata API không đồng nghĩa có file video hoặc transcript; xác minh nguồn media riêng. Schema runtime hiện còn dành cho prototype YouTube và phải được chuyển đổi có version khi triển khai thiết kế mục tiêu.

## Quy tắc gán nhãn

- Phân loại nội dung thực sự có trong input; không gán theo danh tiếng, lịch sử hoặc tên KOL.
- Dùng node ID ổn định; lưu toàn bộ đường dẫn và taxonomy version.
- Không tự tạo nhãn mới trong lúc gán nhãn; đánh dấu đề nghị bổ sung để rà soát.
- Tách thiếu thông tin, ngoài taxonomy và đang chờ phân xử.
- Nội dung nhiều chủ đề hoặc chỉ đủ bằng chứng ở node cha phải theo chính sách được chốt; chưa tự ép về một lá.
- Khi dùng nhãn lá, nhãn tổ tiên được suy ra từ cây; không gán thủ công thành các nhãn độc lập mâu thuẫn.
- Với transcript/OCR, lưu nguồn và nhận diện dữ liệu trích xuất lỗi hoặc thiếu.

## Chất lượng và chia tập

- Thống kê số mẫu mỗi node/tầng, độ dài text, ngôn ngữ, media và tỷ lệ chưa gán được.
- Có một phần được hai người gán độc lập; báo agreement ở từng tầng và đường dẫn, kèm phân xử. Ghi rõ nếu thiếu nhân sự.
- Chia theo content gốc và thời gian; bài đăng lại/cắt từ cùng video phải ở cùng một split.
- Nếu đa nền tảng, rà soát cross-post để tránh cùng nội dung ở train và test.
- Tạo creator holdout riêng nếu cần đánh giá sang KOL chưa thấy; không coi temporal split tự chứng minh điều này.
- Không lựa chọn taxonomy hoặc tinh chỉnh model theo lỗi của test cuối. Nếu taxonomy đổi, version dataset và đánh giá lại theo phiên bản mới.
- Không ép đủ mọi lớp vào mọi split bằng cách phá quy tắc chống rò rỉ; ghi rõ lớp không có support.

## Replay và lưu trữ

Lưu raw JSONL/Parquet và manifest có nguồn, thời gian, bộ lọc, số mẫu, version, checksum. Giữ timestamp gốc; replay có run ID và mode riêng. Nội dung sửa tạo input version mới, tránh cộng cả kết quả cũ lẫn mới vào profile.

Collector dùng biến môi trường cho secret, lưu tiến độ phân trang và lỗi/quota. Chỉ thu dữ liệu cần cho tác vụ. Dữ liệu/comment tồn tại từ prototype cũ không tự trở thành dataset gán nhãn cho phạm vi mới.

## Nguồn kỹ thuật

- [YouTube Data API reference](https://developers.google.com/youtube/data/reference/rest).
- [Videos: list](https://developers.google.com/youtube/data/reference/rest/v3/videos/list).

Khả năng truy cập nền tảng, quota và media được xác minh khi triển khai collector.
