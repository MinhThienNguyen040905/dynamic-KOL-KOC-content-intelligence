# Thiết lập và vận hành local

> **Phạm vi mới:** tài liệu mục tiêu đã chuyển sang phân loại chủ đề dạng cây theo chỉ đạo giảng viên. Runtime và các kết quả kiểm chứng bên dưới vẫn thuộc prototype `rules-v1` trước thay đổi; các trường brand/opinion/sentiment không còn là mục tiêu phát triển. Chưa có classifier phân cấp được triển khai hoặc đánh giá.

## Trạng thái hiện tại

Đã có bộ khung Python, Docker Compose và luồng tích hợp dùng dữ liệu tổng hợp:

`Replay → Kafka → Spark → AI request → Worker → AI service → Result → Spark → PostgreSQL → API/dashboard`

Airflow đã được bổ sung để điều phối các lượt replay và kiểm tra hoàn tất. Xem [hướng dẫn Airflow](10-airflow.md); UI tại <http://localhost:8080>. Khi chạy toàn bộ stack gồm Airflow, đề xuất dành ít nhất 8 GB RAM cho Docker và điều chỉnh theo số liệu thực tế.

AI `rules-v1` là luật cố định để kiểm tra tích hợp cũ. Bước tiếp theo là chốt taxonomy, xây tập nhãn nội dung và chuyển schema/inference/profile/UI/test sang phân loại chủ đề phân cấp.

## Yêu cầu môi trường

- Docker Desktop chạy Linux containers và Docker Compose.
- Đề xuất cấp ít nhất 6 GB RAM cho Docker để thử toàn bộ stack; điều chỉnh theo số liệu thực tế.
- Internet cho lần build đầu và tải Spark Kafka connector từ Maven.
- Python 3.10–3.12 nếu chạy kiểm tra hoặc script ngoài container; container dùng Python 3.11.

## Chạy trên PowerShell

Từ thư mục gốc repository:

```powershell
Copy-Item .env.example .env
docker compose up -d --build
docker compose ps -a
docker compose logs -f spark worker
```

`setup` chạy migration và tạo topic, sau đó thoát với mã 0 là bình thường. Spark lần đầu cần tải connector; chờ log hai streaming query hoạt động trước khi kiểm tra demo. Có thể gửi replay trước: Kafka sẽ giữ sự kiện cho Spark đọc.

```powershell
docker compose run --rm replay
```

- Dashboard: <http://localhost:8000> — chọn run `demo`, bấm **Nạp danh sách** sau khi replay.
- API docs: <http://localhost:8000/docs>.
- AI docs: <http://localhost:8001/docs>.
- Kafka từ máy host: `localhost:9092`; từ container: `kafka:29092`.

Mẫu demo là dữ liệu tổng hợp ngày 25/11/2026, giữ timestamp nguồn; để trống bộ lọc thời gian khi xem lần đầu. Chạy lại cùng run ID dùng cùng định danh để kiểm tra không đếm trùng. Dùng run ID mới để tách lần thực nghiệm:

```powershell
docker compose run --rm replay python -m kol.replay --run-id experiment-01 --interval 0.5
```

## Kiểm tra code

```powershell
py -3.10 -m venv .venv
./.venv/Scripts/python.exe -m pip install -e '.[dev]'
./.venv/Scripts/ruff.exe check .
./.venv/Scripts/ruff.exe format --check .
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe scripts/smoke.py
```

`smoke.py` cần stack đang chạy; tạo run riêng, kiểm tra hoàn tất 4 phân tích, gửi lặp, dẫn chứng và mức tăng lượt xem giữa hai snapshot. Test unit/contract không cần Docker hoặc API key. CI hiện kiểm tra lint, format, unit/contract và cấu hình Compose; chưa chạy smoke toàn stack.

Kiểm tra SQL trên PostgreSQL local (mỗi test dùng run riêng và dọn dữ liệu test khi kết thúc):

```powershell
$env:RUN_DB_TESTS = '1'
./.venv/Scripts/python.exe -m pytest -q
Remove-Item Env:RUN_DB_TESTS
```

## Cấu trúc code

| Đường dẫn | Vai trò |
| --- | --- |
| `src/kol/models.py` | Schema, timestamp, định danh nguồn và xác thực bằng chứng |
| `src/kol/replay.py` | Phát JSONL vào các raw topic |
| `src/kol/streaming.py` | Hai query Spark, archive, chuyển yêu cầu AI và sink database |
| `src/kol/worker.py` | Gọi inference, retry và DLQ trước khi commit offset |
| `src/kol/ai.py` | FastAPI và baseline luật |
| `src/kol/db.py`, `src/kol/sql/` | Kết nối, migration và lưu dữ liệu idempotent |
| `src/kol/api.py`, `src/kol/profiles.py` | Truy vấn profile hiện hành và snapshot |
| `src/kol/static/` | Dashboard tích hợp API |
| `data/samples/` | Mẫu tổng hợp được commit |
| `tests/`, `scripts/smoke.py` | Kiểm tra hợp đồng và tích hợp |

## Dữ liệu và tính đúng

- Named volumes giữ PostgreSQL, Kafka, archive/checkpoint và cache Maven sau khi dừng container.
- Raw Kafka records được archive Parquet theo batch; sự kiện lỗi schema đi DLQ.
- PostgreSQL lưu lịch sử sự kiện và khóa canonical của phiên bản mới nhất. API chỉ tổng hợp phân tích gắn với phiên bản canonical và model đang cấu hình.
- Profile hiện được tổng hợp khi truy vấn, chưa phải aggregate materialized hay stateful window trong Spark. Dữ liệu muộn được giữ trong database, không bị watermark loại; triển khai watermark/window và đo hiệu năng sẽ là bước tiếp theo.
- Đây là cấu hình local hai Spark thread, một Kafka broker; chưa có xác thực ứng dụng, TLS, HA hoặc benchmark quy mô lớn. Các cổng chỉ bind localhost.
- `DATABASE_URL` dùng cho process host phải khớp credential Compose khi thay `.env`. URL-encode ký tự đặc biệt trong mật khẩu khi dùng URI.
- Python process không tự nạp `.env`; Compose đọc file để nội suy. Khi chạy worker/replay trên host, thiết lập biến môi trường rõ ràng.

## Dừng và xem lỗi

```powershell
docker compose logs --tail 100 spark worker api setup
docker compose stop
```

`docker compose down` gỡ container/network và giữ volumes. Không thêm tùy chọn xóa volume nếu còn cần dữ liệu/checkpoint. Nếu đổi schema streaming, dùng checkpoint version mới và lên kế hoạch replay; không xóa checkpoint như cách sửa lỗi mặc định.

## Bước tiếp theo

1. Chốt taxonomy và chính sách nhãn với giảng viên; chọn nguồn nội dung bao phủ cây.
2. Gán nhãn nội dung pilot, khóa taxonomy/version và tách train/dev/test.
3. Chuyển hợp đồng `/analyze`, profile, dashboard và test sang đường dẫn chủ đề; thay baseline và version model.
4. Bổ sung metrics, window/watermark, backfill/reconciliation và kiểm thử lỗi.
5. Đánh giá chất lượng AI và benchmark trước khi mở rộng media.

## Kiểm chứng local ngày 25/11/2026

- Build image thành công; Kafka, PostgreSQL, API và AI healthcheck đạt; setup chạy lặp được và thoát mã 0.
- 11 test contract/database đạt khi bật `RUN_DB_TESTS=1`.
- `scripts/smoke.py` đạt trên stack thật: 6 sự kiện, 4 kết quả AI, gửi lặp không tăng đếm, 4 dẫn chứng và delta lượt xem bằng 60.
- Lint, format, cú pháp JavaScript và cấu hình Compose đạt.
- Chưa kiểm tra trực quan dashboard vì browser access host không khả dụng trong phiên làm việc. Chưa benchmark, đo chất lượng AI hoặc thử collector thật.

Tham khảo connector: [Spark 3.5.7 Kafka integration](https://spark.apache.org/docs/3.5.7/structured-streaming-kafka-integration.html), [Kafka Docker 3.9](https://kafka.apache.org/39/getting-started/docker/).
