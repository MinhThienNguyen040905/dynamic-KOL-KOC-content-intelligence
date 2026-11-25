# Cây chủ đề: bản thảo để thảo luận

## Trạng thái

**Chưa có taxonomy do giảng viên cung cấp.** Ngày 25/11/2026, nhóm xác nhận yêu cầu là phân loại chủ đề theo cây. Cây dưới đây chỉ giải thích hình thức, chưa được duyệt và chưa được đưa vào model/runtime.

## Ví dụ hình thức cây

```text
Nội dung
├── Công nghệ
│   ├── Thiết bị cá nhân
│   │   ├── Điện thoại
│   │   └── Máy tính cá nhân
│   └── Phần mềm
│       ├── Ứng dụng di động
│       └── Công cụ làm việc
└── Làm đẹp
    ├── Chăm sóc da
    │   ├── Chống nắng
    │   └── Làm sạch
    └── Trang điểm
        ├── Trang điểm môi
        └── Trang điểm mắt
```

Ví dụ: “Đánh giá thời lượng pin điện thoại” → `Công nghệ → Thiết bị cá nhân → Điện thoại`.

Đây là chủ đề nội dung, không phải cây sentiment hoặc danh sách thương hiệu. Chủ đề “Điện thoại” không đồng nghĩa đang đánh giá tích cực/tiêu cực và không phụ thuộc nhãn hiệu thiết bị.

## Hợp đồng taxonomy dự kiến

Mỗi node có `id`, `name`, `parent_id`, `description`, ví dụ thuộc/không thuộc nhãn. Cây có `taxonomy_id`, `version`, `status` và ngày hiệu lực. Root kỹ thuật không được tính như một nhãn giúp tăng điểm AI.

Đường dẫn mẫu theo ID: `["technology", "personal_devices", "smartphones"]`, version `example-v0`.

- Một node có tối đa một cha; không chu trình, không node mồ côi.
- ID ổn định trong một phiên bản; đổi tên/cha hoặc gộp/tách node phải có lịch sử thay đổi.
- Kết quả phải ghi đúng version; không ghép đường dẫn từ nhiều phiên bản.
- Độ sâu và số nhánh cần phù hợp dữ liệu; không cố tạo cây sâu chỉ để có nhiều tầng.

## Các điểm phải chốt trước khi gán nhãn

| Quyết định | Ví dụ cần xử lý | Trạng thái |
| --- | --- | --- |
| Phạm vi cây | Chỉ công nghệ hay nhiều lĩnh vực? | Chưa chốt |
| Đơn nhãn/đa nhãn | Bài vừa giới thiệu điện thoại vừa hướng dẫn app | Chưa chốt |
| Nhãn kết thúc | Bắt buộc đến lá hay được dừng ở “Thiết bị cá nhân”? | Chưa chốt |
| Đơn vị phân loại | Một bài/video hay từng đoạn video? | Dự kiến bài/video, cần xác nhận |
| Thiếu thông tin | Caption “Mọi người thấy sao?” nhưng chưa lấy được media | Cần trạng thái riêng và hướng dẫn |
| Ngoài cây | Nội dung không thuộc bất kỳ nhánh đã định nghĩa | Cần quy tắc, không tự thêm nhãn |

## Cách xây dựng bản để trình giảng viên

1. Khảo sát nội dung thật để đề xuất phạm vi và các nhánh ứng viên.
2. Mỗi nhãn có mô tả, ví dụ, phản ví dụ và ranh giới với nhãn anh em.
3. Gán thử, ghi các bất đồng và đo số mẫu tại từng tầng.
4. Điều chỉnh/gộp nhánh chưa phân biệt được hoặc quá ít mẫu.
5. Xác nhận chính sách nhãn và cây với giảng viên, rồi khóa version cho dataset/thực nghiệm.

Chưa dùng cây ví dụ này để gán nhãn sản xuất hoặc khẳng định đã có mô hình phân cấp.
