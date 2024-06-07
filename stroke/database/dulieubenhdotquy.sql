CREATE DATABASE dulieudotquy
GO

USE dulieudotquy
GO

CREATE TABLE BacSi
(
	ID_BS char(10) not null,
	Ten_BS nvarchar(30),
	ChuyenKhoa nvarchar(30),
	GioiTinh nvarchar(3),
	Phong int,
	SoDienThoai int,
	Primary key(ID_BS)
)

CREATE TABLE BenhNhan
(
	ID_BN char(10) not null,
	Ten_BN nvarchar(30),
	GioiTinh nvarchar(3),
	Tuoi int,
	DiaChi nvarchar(30),
	Primary key(ID_BN)
)

CREATE TABLE TrieuChung
(
	ID_TC char(10) not null,
	ID_BN char(10) not null,
	HuyetAp int,
	BenhTim int,
	MucDuongHuyetTrungBinh float,
	TinhTrangHutThuoc varchar(30),
	BMI char(10),
	Primary key(ID_TC),
	FOREIGN KEY (ID_BN) REFERENCES BenhNhan(ID_BN),
)

CREATE TABLE StrokePrediction (
        Gender NVARCHAR(255),
        Age INT,
        Hypertension INT,
        HeartDisease INT,
        EverMarried NVARCHAR(255),
        WorkType NVARCHAR(255),
        ResidenceType NVARCHAR(255),
        AvgGlucoseLevel FLOAT,
        BMI FLOAT,
        SmokingStatus NVARCHAR(255),
        Result NVARCHAR(255),
		Primary key(Hypertension,HeartDisease,EverMarried,AvgGlucoseLevel,BMI)
)
DROP TABLE StrokePrediction

-- Thêm dữ liệu 
INSERT INTO BacSi VALUES ('BS01',N'Nguyễn Văn Thanh',N'Khoa Tim Mạch','Nam','205','0123456789')
INSERT INTO BacSi VALUES ('BS02',N'Đoàn Duy Mạnh',N'Khoa Tim Mạch','Nam','204','0123456780')
INSERT INTO BacSi VALUES ('BS03',N'Lê Thị Hoa',N'Khoa Tim Mạch',N'Nữ','203','0123456781')

--
INSERT INTO BenhNhan VALUES ('BN01',N'Vũ Nguyễn Anh Duy','Nam','30',N'123 Trường Chinh')
INSERT INTO BenhNhan VALUES ('BN02',N'Nguyễn Hoài Nam','Nam','48',N'456 Trường Chinh')
INSERT INTO BenhNhan VALUES ('BN03',N'Trần Minh Anh',N'Nữ','67',N'789 Trường Chinh')
INSERT INTO BenhNhan VALUES ('BN04',N'Nguyễn Thanh Tâm',N'Nữ','50',N'123 Cộng Hoà')
INSERT INTO BenhNhan VALUES ('BN05',N'Phạm Duy Thái','Nam','25',N'456 Cộng Hoà')

--
INSERT INTO TrieuChung VALUES ('TC01','BN01','0','1','228.69','never smoked','36.6')
INSERT INTO TrieuChung VALUES ('TC02','BN02','1','1','100.21','smokes','34.2')
INSERT INTO TrieuChung VALUES ('TC03','BN03','0','1','228.69','Unknown','27.1')
INSERT INTO TrieuChung VALUES ('TC04','BN04','0','0','95.12','Unknown','18')


DELETE StrokePrediction WHERE Gender = 'Female'
DELETE StrokePrediction WHERE Gender = 'Male'