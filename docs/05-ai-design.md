# Thiết kế AI: phân loại chủ đề phân cấp

## Phạm vi hiện hành

AI chỉ phân loại chủ đề theo cây, theo giới hạn giảng viên mà nhóm xác nhận ngày **25/11/2026**. ABSA, sentiment và trích xuất thương hiệu như tác vụ riêng đã được bỏ khỏi kế hoạch.

Taxonomy chưa được cung cấp. Chưa chốt đơn nhãn/đa nhãn, số tầng hoặc cho phép dừng ở node cha. Hợp đồng dưới đây là thiết kế mục tiêu, chưa thay thế schema/API runtime cũ.

## Input

Một bài đăng/video gồm content ID, input version, KOL/account ID và các trường nội dung có sẵn: title, caption, text hoặc description. Transcript/OCR/thông tin hình ảnh chỉ bổ sung khi cần và truy cập được.

Bình luận không phải đầu vào mặc định. Không dùng danh tính KOL để suy ra chủ đề thay cho phân tích nội dung. Engagement không phải nhãn hoặc tín hiệu bắt buộc của classifier.

## Output minh họa

```json
{
  "content_id": "example-content",
  "input_version": "v1",
  "model_version": "candidate-v1",
  "taxonomy_version": "example-v0",
  "status": "classified",
  "topic_paths": [
    ["technology", "personal_devices", "smartphones"]
  ]
}
```

Input minh họa: “Review pin và camera điện thoại”. Cây `example-v0` chỉ để giải thích, chưa được duyệt. `topic_paths` dùng dạng danh sách để mô tả hợp đồng; việc chấp nhận một hay nhiều đường dẫn phải theo chính sách đã chốt. Root kỹ thuật không tính là nhãn dự đoán.

Các trạng thái mục tiêu: `classified`, `insufficient_information`, `out_of_taxonomy`, `needs_review`; lỗi vận hành dùng trạng thái xử lý riêng, không giả làm kết quả phân loại hợp lệ. Phải xác thực quan hệ cha–con, phiên bản cây và độ sâu output.

## Các phương án để so sánh sau khi chốt dữ liệu

- **Baseline phẳng:** dự đoán nhãn ở mức chi tiết đã thống nhất, suy ra tổ tiên bằng cây. Chốt cách xử lý node cha nếu cho phép nhãn nội bộ.
- **Phân loại theo cây:** chọn nhóm cấp cao, sau đó phân loại trong các nhóm con. Cần đo lỗi lan truyền khi chọn sai nút cha.
- **Model chung cho các tầng:** dự đoán nhiều tầng và kiểm soát đường dẫn hợp lệ; chỉ triển khai nếu quy mô nhãn/tài nguyên phù hợp.

Đây là các thiết kế ứng viên, chưa chốt kiến trúc model hoặc thư viện. Có thể dùng model pretrained, fine-tune hoặc train baseline đơn giản; không bắt buộc train từ đầu và không mặc định cần một model riêng cho mỗi node.

## Training và inference

Training offline: chuẩn bị dữ liệu → gán nhãn cây → chia train/dev/test → huấn luyện/fine-tune → chọn tham số trên dev → đánh giá test khóa → phát hành model có version.

Inference online: nhận nội dung → chuẩn hóa/trích xuất text nếu cần → phân loại → kiểm tra đường dẫn → lưu kết quả → cập nhật profile. Airflow điều phối workflow hữu hạn; dữ liệu mới không tự kích hoạt training lại.

## Độ tin cậy

- Khi chưa đủ thông tin, không ép model chọn một lá.
- Nếu cho phép dừng ở node cha, phải ghi rõ mức chi tiết và tính coverage; không báo như dự đoán lá thành công.
- Confidence chỉ có ý nghĩa khi có định nghĩa/kiểm chứng; ngưỡng chọn trên dev.
- Lưu text/provenance cần thiết để kiểm tra nhãn; trích đoạn minh họa không tự được xem là lời giải thích trung thực của model.
- Input mạng xã hội là dữ liệu, không phải chỉ dẫn để model thực thi.

## Profile chủ đề

Profile tổng hợp số lượng nội dung thuộc từng node và các tổ tiên trong khoảng thời gian. Đếm tối đa một lần mỗi content/node; khi đa nhãn, cùng một content có thể thuộc nhiều nhánh nên tỷ lệ không bắt buộc cộng thành 100%.

Tách số nội dung đã phân loại, chưa xử lý, thiếu thông tin và ngoài cây. Nội dung được sửa hoặc model/taxonomy đổi phải thay thế kết quả hiện hành hoặc tính lại; không cộng thêm như một bài mới. Không trộn taxonomy version khi chưa mapping hoặc phân loại lại.

## Khoảng cách với prototype

`rules-v1` hiện chỉ có nhãn phẳng theo từ khóa và logic brand/opinion của hướng cũ. Nó chưa phải classifier phân cấp. Cần chuyển schema, inference, profile, dashboard, sample và test đồng bộ sau khi taxonomy/chính sách nhãn được chốt.
