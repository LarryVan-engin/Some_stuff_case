flowchart TB
    %% STYLE
    classDef user fill:#E6F4FF,stroke:#2C82C9,stroke-width:1px,color:#000;
    classDef admin fill:#FFF2CC,stroke:#D4A017,stroke-width:1px,color:#000;

    %% --- NGƯỜI DÙNG ---
    subgraph U["🧑‍💻 Người dùng"]
    direction TB
        U1([Start]):::user --> U2["Truy cập trang đăng nhập / đăng ký"]:::user
        U2 --> U3{"Đã có tài khoản?"}:::user
        U3 -->|Có| U4["Chọn Đăng nhập"]:::user
        U4 --> U5["Nhập thông tin đăng nhập"]:::user
        U5 --> U6["Submit thông tin lên server"]:::user

        U3 -->|Không| U7["Chọn Đăng ký"]:::user
        U7 --> U8["Nhập thông tin đăng ký - email bắt buộc"]:::user
        U8 --> U9{"Thông tin trùng?"}:::user
        U9 -->|Có| U10["Thông báo người dùng thay đổi"]:::user
        U9 -->|Không| U11["Submit thông tin đăng ký lên server"]:::user
        U11 --> U12["Gửi mail xác nhận đăng ký"]:::user
        U12 --> U13(["Kết thúc bước 1"]):::user

        %% Sau khi được duyệt
        U14(["Bắt đầu bước 3"]):::user --> U15["Đăng nhập, xem danh sách món hàng"]:::user
        U15 --> U16["Chọn món hàng, xác nhận mua"]:::user
        U16 --> U17["Hiển thị mã QR thanh toán"]:::user
        U17 --> U18(["Kết thúc bước 3"]):::user

        %% Thanh toán
        U19(["Bắt đầu bước 4"]):::user --> U20["Hiển thị giao diện thanh toán và mã QR"]:::user
        U20 --> U21["Quét mã QR hoặc chuyển khoản"]:::user
        U21 --> U22["Nhấn 'Xác nhận đã thanh toán'"]:::user
        U22 --> U23["Đơn hàng sang trạng thái 'Chờ xác nhận'"]:::user
        U23 --> U24["Gửi email thông báo cho admin"]:::user
        U24 --> U25(["Kết thúc bước 4"]):::user
    end

    %% --- ADMIN ---
    subgraph A["🧑‍💼 Admin"]
    direction TB
        A1(["Bắt đầu bước 2"]):::admin --> A2["Nhận tài khoản mới 'Đang chờ duyệt'"]:::admin
        A2 --> A3["Kiểm tra thông tin tài khoản"]:::admin
        A3 --> A4{"Chấp nhận?"}:::admin
        A4 -->|Có| A5["Kích hoạt tài khoản"]:::admin
        A5 --> A6["Gửi mail kích hoạt người dùng"]:::admin
        A6 --> A7["Lưu thông tin tài khoản trên server"]:::admin
        A4 -->|Không| A8["Xóa tài khoản khỏi danh sách chờ"]:::admin
        A7 --> A9(["Kết thúc bước 2"]):::admin
        A8 --> A9

        %% Xác nhận đơn hàng
        A10(["Bắt đầu bước 5"]):::admin --> A11["Thấy đơn hàng 'Đang chờ xác nhận'"]:::admin
        A11 --> A12{"Xác nhận hay từ chối?"}:::admin
        A12 -->|Xác nhận| A13["Cập nhật trạng thái đơn hàng: Đã xác nhận"]:::admin
        A12 -->|Từ chối| A14["Hủy hoặc cập nhật trạng thái đơn hàng"]:::admin
        A13 --> A15["Gửi email kết quả cho người dùng"]:::admin
        A14 --> A15
        A15 --> A16(["Kết thúc bước 5"]):::admin
    end

    %% --- KẾT NỐI GIỮA USER & ADMIN ---
    U11 -.-> A2
    A5 -.-> U14
    U24 -.-> A11
    A15 -.-> U1
