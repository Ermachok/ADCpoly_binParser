import struct
import os


class FileHeader:
    def __init__(self, side, mode, frame_count):
        self.side = side
        self.mode = mode
        self.frame_count = frame_count

    @staticmethod
    def parse(data):
        side, mode, frame_count = struct.unpack('BBH', data[:4])  # read byte(B),byte(B) and 2 more bytes(H) = 4
        return FileHeader(side, mode, frame_count)


class FrameHeader:
    def __init__(self, stop_point, timestamp):
        self.stop_point = stop_point
        self.timestamp = timestamp

    @staticmethod
    def parse(data):
        stop_point, timestamp = struct.unpack('HL', data[:8])
        return FrameHeader(stop_point, timestamp)


class MemoryFrame:
    def __init__(self, header, points):
        self.header = header
        self.points = points

    @staticmethod
    def parse(data):
        header = FrameHeader.parse(data[:16])
        points = []
        offset = 16  # offset from header
        for i in range(1024):
            point = struct.unpack('8H', data[offset:offset + 16])
            points.append(point)
            offset += 16
        return MemoryFrame(header, points)


def parse_bin_file(file_path):
    with open(file_path, 'rb') as f:

        file_header_data = f.read(256)
        file_header = FileHeader.parse(file_header_data)

        frames = []
        for _ in range(file_header.frame_count):
            frame_data = f.read(16400)  # 16400 - header 16 bytes + frame 1024 * 16 = 16400, 16 - element = 8 * 2 bytes
            frame = MemoryFrame.parse(frame_data)
            frames.append(frame)

    return file_header, frames


file_path = r"C:\Users\NE\Desktop\newSOFT_adc\side_a_fast_data.bin"
if os.path.exists(file_path):
    file_header, frames = parse_bin_file(file_path)
    print(f"Side: {file_header.side}, Mode: {file_header.mode}, Frame Count: {file_header.frame_count}")
    print(f"First Frame Stop Point: {frames[0].header.stop_point}, Timestamp: {frames[0].header.timestamp}")
else:
    print("File not found!")
