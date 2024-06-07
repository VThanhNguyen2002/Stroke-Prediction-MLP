CREATE DATABASE dulieudotquy
GO

USE dulieudotquy
GO

CREATE TABLE BacSi
(
    ID_BS char(10) NOT NULL,
    Ten_BS nvarchar(30),
    GioiTinh nvarchar(3),
    ChuyenKhoa nvarchar(30),
    Primary KEY (ID_BS)
)

CREATE TABLE BenhNhan
(
    ID_BN char(10) NOT NULL,
    Ten_BN nvarchar(30),
    NgaySinh date,
    GioiTinh nvarchar(3),
    DiaChi nvarchar(100),
    SoDienThoai nvarchar(15),
    Primary KEY (ID_BN)
)

CREATE TABLE TrieuChung
(
    ID_TC char(10) NOT NULL,
    ID_BN char(10) NOT NULL,
    ID_BS char(10) NOT NULL,
    HuyetAp int,
    BenhTim int,
    MucDuongHuyetTrungBinh float,
    TinhTrangHutThuoc nvarchar(30),
    BMI float,
    Primary KEY (ID_TC),
    FOREIGN KEY (ID_BN) REFERENCES BenhNhan(ID_BN),
    FOREIGN KEY (ID_BS) REFERENCES BacSi(ID_BS)
)

-- Thêm dữ liệu mẫu vào bảng BacSi
INSERT INTO BacSi (ID_BS, Ten_BS, GioiTinh, ChuyenKhoa) VALUES 
('BS01', N'Nguyễn Văn Thanh', N'Nam', N'Khoa Tim Mạch'),
('BS02', N'Đoàn Duy Mạnh', N'Nam', N'Khoa Tim Mạch'),
('BS03', N'Lê Thị Hoa', N'Nữ', N'Khoa Tim Mạch');

-- Thêm dữ liệu mẫu vào bảng BenhNhan
INSERT INTO BenhNhan (ID_BN, Ten_BN, NgaySinh, GioiTinh, DiaChi, SoDienThoai) VALUES 
('BN01', N'Vũ Nguyễn Anh Duy', '1994-05-01', N'Nam', N'123 Trường Chinh', '0123456789'),
('BN02', N'Nguyễn Hoài Nam', '1976-02-15', N'Nam', N'456 Trường Chinh', '0123456788'),
('BN03', N'Trần Minh Anh', '1957-08-10', N'Nữ', N'789 Trường Chinh', '0123456787'),
('BN04', N'Nguyễn Thanh Tâm', '1974-03-22', N'Nữ', N'123 Cộng Hoà', '0123456786'),
('BN05', N'Phạm Duy Thái', '1999-11-30', N'Nam', N'456 Cộng Hoà', '0123456785');

-- Thêm dữ liệu mẫu vào bảng TrieuChung
INSERT INTO TrieuChung (ID_TC, ID_BN, ID_BS, HuyetAp, BenhTim, MucDuongHuyetTrungBinh, TinhTrangHutThuoc, BMI) VALUES 
('TC01', 'BN01', 'BS01', 120, 1, 228.69, 'never smoked', 36.6),
('TC02', 'BN02', 'BS02', 140, 1, 100.21, 'smokes', 34.2),
('TC03', 'BN03', 'BS03', 130, 1, 228.69, 'Unknown', 27.1),
('TC04', 'BN04', 'BS01', 110, 0, 95.12, 'Unknown', 18.0),
('TC05', 'BN05', 'BS02', 125, 1, 130.55, 'formerly smoked', 25.3);
