# Kế hoạch dữ liệu

## Pilot trước khi mở rộng

1. Chọn 2–3 kênh cùng lĩnh vực và thử truy cập metadata/bình luận bằng API chính thức.
2. Ghi số bản ghi lấy được, quota sử dụng, lỗi, thời gian và tỷ lệ dữ liệu thiếu.
3. Lấy khoảng 200 bình luận để xây hướng dẫn nhãn và khảo sát tỷ lệ có ý kiến hữu ích.
4. Chốt lĩnh vực, taxonomy, chu kỳ polling và quy mô nhãn theo kết quả pilot.

Mốc 200 bình luận phục vụ khảo sát, không được xem là quy mô đủ cho đánh giá cuối kỳ. Không giả định API metadata đồng thời cung cấp file video hoặc transcript; xác minh riêng nguồn và quyền truy cập cho từng loại dữ liệu.

## Dữ liệu cần lưu

| Nhóm | Trường chính |
| --- | --- |
| Creator | ID nguồn, tên hiển thị, URL, lĩnh vực, trạng thái theo dõi |
| Content | ID video, creator ID, tiêu đề, mô tả, thời gian đăng/cập nhật, URL, input version |
| Comment | ID, video ID, parent ID nếu có, text gốc, thời gian đăng/cập nhật, source version |
| Engagement | Video ID, thời điểm quan sát, các số đếm có sẵn và trạng thái thiếu |
| Evidence | Source ID/version, field, offset hoặc timestamp, trích đoạn |
| Analysis | Tuples/labels, model version, taxonomy version, trạng thái và thời gian xử lý |

Giữ văn bản gốc phục vụ dẫn chứng; văn bản chuẩn hóa là trường riêng. ID tác giả bình luận chỉ lưu khi cần cho tác vụ, ưu tiên pseudonym hóa. Không thu thập thông tin riêng tư không cần thiết.

## Thu thập và chất lượng

- Lưu tiến độ phân trang, thời điểm poll và khóa nguồn để thu thập lặp không tạo bản ghi trùng.
- Kiểm tra cách lấy replies; không giả định danh sách comment thread luôn chứa toàn bộ phản hồi.
- Theo dõi nội dung bị xóa, comment bị tắt và field không được nguồn cung cấp.
- Giữ emoji, dấu tiếng Việt, phủ định, từ lóng và dấu hiệu mỉa mai; không xóa chúng bằng tiền xử lý thô.
- Thống kê ngôn ngữ, độ dài, spam, duplicate và tỷ lệ comment không có ý kiến.
- Mọi tập export có manifest: nguồn, khoảng thời gian, bộ lọc, số lượng, version và checksum.

## Hướng dẫn gán nhãn ban đầu

### Nội dung

- `topics`: một hoặc nhiều chủ đề trong taxonomy đã định nghĩa.
- `brand_mentions`: tên thương hiệu, dạng chuẩn hóa và evidence.
- `unknown/other`: dùng khi chưa có nhãn phù hợp; theo dõi để cải tiến taxonomy.

### Bình luận

Mỗi ý kiến có `entity`, `entity_type`, `aspect`, `opinion_span`, `sentiment` và evidence offset. Một bình luận có thể có 0, 1 hoặc nhiều tuple.

- Entity có thể là KOL, thương hiệu hoặc sản phẩm; chỉ liên kết ID khi có đủ bằng chứng.
- Sentiment: `positive`, `negative`, `neutral`; trường hợp không xác định được đánh dấu `uncertain` để rà soát, không ép thành neutral.
- Entity/aspect ngầm định dùng cờ `implicit`; không tạo span văn bản không tồn tại.
- Bình luận không chứa ý kiến có danh sách tuple rỗng; spam có cờ riêng.
- Quy định offset theo chuỗi text gốc và kiểm tra `text[start:end]` khớp đoạn được gán.

Taxonomy khía cạnh được chốt theo lĩnh vực. Ví dụ khảo sát: cách trình bày/độ tin cậy của KOL, giá/chất lượng/tính năng của sản phẩm; chưa coi đây là danh sách nhãn cuối cùng.

## Kiểm soát nhãn và chia tập

- Có ít nhất một phần dữ liệu được hai người gán độc lập, đối chiếu bất đồng và lưu kết quả phân xử. Nếu thiếu nhân sự, ghi rõ hạn chế.
- Đo agreement theo thành phần: sentiment/aspect và span/entity; không dùng một chỉ số để đại diện mọi loại nhãn.
- Chia train/dev/test theo video hoặc chuỗi hội thoại, ưu tiên test ở thời gian muộn hơn. Không để replies cùng thread hoặc bản sao gần giống rơi vào nhiều tập.
- Fit taxonomy phụ trợ, bộ chuẩn hóa và lựa chọn prompt/model bằng train/dev. Khóa test trước đánh giá cuối.
- Nếu cần tuyên bố tổng quát hóa sang KOL mới, tạo thêm tập creator holdout; kết quả theo thời gian không tự chứng minh khả năng này.

## Replay và lưu trữ

Lưu sự kiện nguồn dưới JSONL/Parquet, giữ timestamp gốc. Replay có tốc độ cấu hình, run ID riêng và chế độ timestamp được ghi trong manifest. Khi dịch thời gian để chạy demo hiện tại, giữ thêm timestamp gốc. Tăng tốc replay để đo hệ thống không thay thế đánh giá thay đổi hành vi thực tế.

Thông tin truy cập dùng biến môi trường. Tập công khai và ảnh chụp báo cáo cần rà soát tên/ID người bình luận và điều kiện sử dụng dữ liệu. Chu kỳ giữ/xóa dữ liệu được chốt trước khi thu thập quy mô lớn.

## Tham khảo kỹ thuật

- [YouTube Data API reference](https://developers.google.com/youtube/data/reference/rest).
- [CommentThreads: list](https://developers.google.com/youtube/data/reference/rest/v3/commentThreads/list).
- [Videos: list](https://developers.google.com/youtube/data/reference/rest/v3/videos/list).

Kiểm tra lại quota, field và điều kiện truy cập tại thời điểm triển khai.
