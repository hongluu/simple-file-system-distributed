# Sử dụng docker container để mô phỏng chương trình thống nhất dữ liệu lưu trữ của các máy trong ngữ cảnh hệ phân tán.
## 1. Giới thiệu các thành phần
* `Master(Name Node)`: Lưu trữ cấu hình và xử lý đồng bộ data đến các Data Node
* `Minions`: Tập những Data Node, lưu trữ data cần sao lưu. Mặc định đang có 2 Data Node (hpt-slave-a, hpt-slave-b)
* `Client`: 
 Kiểm tra trạng thái dữ liệu file .txt trong folder client/data. 
Khi có hành động thêm mới file .txt hoặc thay đổi nội dung file .txt trong folder client/data chương trình sẽ tự động đồng bộ dữ liệu lên các Data Node (slave-a, slave-b)

## 2. Cài đặt
- Cài đặt docker tại link
https://www.docker.com/get-started
- Sau khi cài đặt xong docker lấy source code về máy 
```
git clone https://github.com/hongluu/simple-file-system-distributed.git
```
- Vào folder simple-file-system-distributed chạy lệnh
```
docker-compose up -d
```
- Sau đó hệ thống sẽ tạo ra 4 container `hpt-master`, `hpt-client`, `hpt-slave-a`, `hpt-slave-b` . Kiểm tra lại bằng lệnh 
```
docker ps
```

## 3. Sử dụng chương trình

### 3.1 Kiểm tra việc sao lưu data khi tạo mới file trong folder client/data
- Trong folder `client/data` . Tạo file test.txt có nội dung bất kỳ. VD: '123'
- Sau đó kiểm tra Get nội dung file test.txt từ data node bằng câu lệnh bên dưới
```
docker exec -it hpt-client python3 client.py get test.txt
```
- Các trường hợp kiểm tra
   - TH1: 2 container data node: hpt-slave-a, hpt-slave-a đang chạy -> Câu lệnh trên trả về nội dung '123'
   - TH2: 2 container data node: hpt-slave-a chạy, hpt-slave-a không chạy -> Câu lệnh trên trả về nội dung '123'
   - TH3: 2 container data node: hpt-slave-a chạy, hpt-slave-a đều không chạy -> Câu lệnh trên trả về nội dung 'INFO:__main__:No blocks found. Possibly a corrupt file' (Do không có data-node nào hoạt động)

### Các câu lệnh hỗ trợ
- Tắt container : `docker stop [container name]`. VD: `docker stop hpt-slave-a`
- Bật container : `docker start [container name]`. VD: `docker start hpt-slave-a`

### 3.1 Kiểm tra việc sao lưu data khi có thay đổi file .txt trong folder client/data
- Trong folder `client/data` . Sửa file test.txt có nội dung bất kỳ. VD: '123 123123'
- Kiểm tra nội dung file đã được cập nhật lên data node chưa bằng lệnh
```
docker exec -it hpt-client python3 client.py get test.txt
```