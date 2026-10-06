# Multi-Source Ingestion Tool

CLI tool để fetch dữ liệu từ nhiều nguồn (API, CSV), validate bằng pydantic, 
có retry logic, và ghi kết quả ra Parquet. Cấu hình nguồn qua file YAML, 
thêm nguồn mới không cần sửa code.

## Cài đặt

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Cách dùng

\`\`\`bash
python ingest.py --config sources.yaml --output ./data
\`\`\`

## Cấu hình nguồn (sources.yaml)

\`\`\`yaml
sources:
  - name: dummyjson_products
    type: api
    url: "https://dummyjson.com/products"
    response_key: products
\`\`\`

## Chạy test

\`\`\`bash
pytest -v
\`\`\`