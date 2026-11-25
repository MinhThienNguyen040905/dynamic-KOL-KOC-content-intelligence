# Thiết kế AI

## Mục tiêu

Tạo kết quả có cấu trúc để cập nhật profile và truy ngược bằng chứng. Model, prompt và ngân sách inference chưa được chọn; quyết định sau pilot dữ liệu và kiểm tra tài nguyên.

## Tác vụ A: hiểu nội dung

- Input MVP: tiêu đề và mô tả video, kèm creator/video ID.
- Output: nhãn chủ đề đa nhãn, mention thương hiệu, entity chuẩn hóa nếu xác định được, evidence theo field/offset.
- Baseline: từ điển thương hiệu có kiểm tra biên từ và một phương án phân loại chủ đề đơn giản, được xây từ train/dev.
- Phương án nâng cao: model ngôn ngữ hoặc trích xuất có cấu trúc sử dụng ngữ cảnh; so sánh trên cùng tập test.

Khi mở rộng transcript/keyframe, giữ riêng nguồn bằng chứng và chi phí xử lý. Mention trong caption hoặc mô tả không tự chứng minh nội dung toàn video; không tuyên bố đã phân tích video nếu chưa xử lý media.

## Tác vụ B: ý kiến theo thực thể và khía cạnh

- Input: bình luận; tùy thực nghiệm thêm tiêu đề/mô tả và parent comment.
- Output: danh sách tuple `entity → aspect → opinion span → sentiment`.
- Baseline so sánh thô: sentiment toàn bình luận để minh họa giới hạn; không dùng nó làm kết quả chính của đề tài.
- Baseline cùng tác vụ: mô hình/prompt trích xuất tuple chỉ dùng bình luận.
- Phương án chính: trích xuất tuple có thêm ngữ cảnh video; xét pipeline tách bước hoặc joint extraction theo kết quả pilot.

Đánh giá cả từng thành phần và tuple hoàn chỉnh. Lỗi liên kết thực thể phải được ghi nhận ngay cả khi sentiment đúng.

## Ví dụ hợp đồng output

```json
{
  "comment_id": "example-comment",
  "input_version": "v1",
  "model_version": "candidate-v1",
  "taxonomy_version": "pilot-v1",
  "status": "success",
  "opinions": [
    {
      "entity_text": "máy X",
      "entity_type": "product",
      "entity_id": null,
      "aspect": "battery",
      "opinion_text": "pin yếu",
      "sentiment": "negative",
      "evidence": {"field": "text", "start": 6, "end": 13}
    }
  ]
}
```

Ví dụ dùng input `máy X pin yếu`; offset tính theo code point, end-exclusive. Đây là fixture minh họa hợp đồng, chưa phải kết quả inference. Client dùng UTF-16 cần chuyển offset trước khi tô sáng.

## Xác thực và độ tin cậy

- Kiểm tra schema, enum, offset và đoạn trích khớp nguồn.
- Không biến output lỗi hoặc thiếu thành danh sách tuple rỗng thành công.
- Tách `success`, `no_opinion`, `invalid_output`, `failed` và `needs_review` ở lớp trạng thái thống nhất khi triển khai.
- Điểm confidence chỉ hiển thị khi có định nghĩa và kiểm chứng; không coi số model tự sinh là xác suất đã hiệu chuẩn.
- Model/prompt nhận input mạng xã hội như dữ liệu, không thực thi chỉ dẫn nằm trong bình luận.
- Lưu version và cấu hình inference để tái lập; tránh log credential hoặc dữ liệu không cần thiết.

## Profile và tổng hợp

Profile gồm phân bố chủ đề, thương hiệu, ý kiến theo entity/aspect và biến động engagement. Mỗi chỉ số có khoảng thời gian, số mẫu, số mẫu đã phân tích và thời điểm cập nhật.

Phân biệt tỷ lệ tuple tiêu cực với tỷ lệ bình luận có ý kiến tiêu cực; một bình luận có thể sinh nhiều tuple. Chốt mẫu số trong API và báo cáo. Tóm tắt MVP dùng template trên số liệu đã tính, kèm dẫn chứng; sinh tóm tắt bằng LLM là mở rộng cần đánh giá riêng về độ trung thực.

## Thực nghiệm ưu tiên

1. Comment-only so với comment + ngữ cảnh nội dung, trên cùng bộ test.
2. Phân tích lỗi theo entity ngầm định, nhiều thực thể, phủ định, slang, sarcasm và thiếu ngữ cảnh.
3. Nếu đủ dữ liệu/media: text-only so với thêm transcript hoặc keyframe.
4. Đo chất lượng cùng latency và chi phí; chỉ chọn model sau khi cân đối cả ba.
