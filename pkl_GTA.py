import os,sys,time,io
import cv2
import pickle
from PIL import Image

class GTA(object):

    def __init__(self,
                 gif_path='./gif_to_transform/target.gif',          #GIF檔案的路徑，我將目標設為target.gif
                 save_path='./gif_frame/',                          #GIF切片後的圖片存放路徑
                 file_name = './frame_pkl/thebigpkl.pkl',           #寫入的巨大pkl文件路徑
                 WIDTH = 120,                                       #設定輸出圖像寬度
                 HEIGHT = 37,                                       #設定輸出圖像高度
                 ascii_char = "$$$$@@@@####****              "      # rickroll專用
                 ):
        # 指定GIF 文件路徑
        self.gif_path = gif_path
        self.save_path=save_path
        self.gif = Image.open(gif_path)
        self.frame_count = self._count_frames()

        self.file_name = file_name
        self.WIDTH = WIDTH # 寬
        self.HEIGHT = HEIGHT # 高
        self.lines_to_read = self.HEIGHT
        #self.ascii_char ="   ._\"^\:=,;><~+=?][1  "        # 無牙龍專用
        self.ascii_char = ascii_char 


    def _count_frames(self):
        frame_count = 0
        while True:
            try:
                self.gif.seek(frame_count)
                frame_count += 1
            except EOFError:
                break
        self.gif.seek(0)  # 回到 GIF 文件的第一幀
        return frame_count


    def clear_screen(self):
        # if os.name == 'posix':  # Unix/Linux/MacOS
        #     os.system('clear')
        # elif os.name == 'nt':  # Windows
        #     os.system('cls')
        sys.stdout.write("\033[H\033[J")# 使用 ANSI 轉義序列來清除螢幕
        sys.stdout.flush()


    def dancing(self):
        while True:
                # 使用內存緩存讀取和存儲大量文字
            buffer = io.StringIO()

            with open(self.file_name, 'rb') as file:
                ascii_frames = pickle.load(file)

            for frame in ascii_frames:
                for line in frame:
                    buffer.write(line + "\n")
                # buffer.write("\n")  # 每個frame之間加一個空行，方便區分

            buffer.seek(0)  # 將緩存指針移到開頭

            # while True:
            #     buffer.seek(0)  # 每次循環將指針重置到緩存開頭
            #     for _ in range(len(ascii_frames)):
            #         for _ in range(self.HEIGHT):
            #             line = buffer.readline()
            #             sys.stdout.write(line)
            #         sys.stdout.flush()
            #         time.sleep(0.040)
            #         self.clear_screen()
            while True:
                buffer.seek(0)  # 每次循環將指針重置到緩存開頭
                for frame in ascii_frames:
                    sys.stdout.write("\033[H")  # 使用 ANSI 轉義序列將光標移到行首
                    for line in frame:
                        sys.stdout.write(line + "\n")
                    sys.stdout.flush()
                    time.sleep(0.040)


    def files_in_directory(self,directory):
        try:
            files = os.listdir(directory)
            files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
            return files
        except:
            print("檔案不存在")
            return 0


    def count_files_in_directory(self,directory):
        try:
            files = os.listdir(directory)
            files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
            file_count = len(files)
            return file_count
        except:
            print("檔案不存在")
            return 0


    def get_char(self,gray_value):
    
        length = len(self.ascii_char) # 根據傳進來的灰階值判斷此位置要使用哪個字元
        unit = 256.0 / length # 區分灰階範圍
        return self.ascii_char[int(gray_value / unit)]

    def transform_imgtotxt(self):       #將圖片轉成ASCII符號加入pkl
        filepath = self.file_name
        if os.path.exists(filepath):
            os.remove(filepath)

        ascii_frames = []
        file_len = self.count_files_in_directory(self.save_path)
        print(f"transform {file_len} images into pkl...")
        for a1 in range(file_len):
            frame_name = os.path.join(self.save_path, f'frame_{a1}.png')
            img = cv2.imread(frame_name, cv2.IMREAD_GRAYSCALE) # 將圖片自動轉為灰階圖片
            img = cv2.resize(img, (self.WIDTH, self.HEIGHT)) # 將灰階圖縮小成指定大小
            txt_frame = []
            for i in range(self.HEIGHT):
                line = ''
                for j in range(self.WIDTH):
                    line += self.get_char(img[i][j]) # 轉為指定字符
                txt_frame.append(line)
            ascii_frames.append(txt_frame)

        with open(filepath, 'wb') as file:
            pickle.dump(ascii_frames, file)

    def clear_save_path(self):
        if os.path.exists(self.save_path):
            files = os.listdir(self.save_path)
            for f in files:
                os.remove(os.path.join(self.save_path, f))
                print(f"舊資料 '{self.save_path}{f}' 已成功删除。")
        else:
            os.makedirs(self.save_path)
            print(f"新目錄 '{self.save_path}' 已成功創建。")

    def save_frames(self):
        self.clear_save_path()
        for i in range(self.frame_count):
            self.gif.seek(i)
            frame = self.gif.copy()
            frame.save(os.path.join(self.save_path, f'frame_{i}.png'))
            print(f"Saved frame {i}")
        print("All frames saved successfully.")


if __name__=="__main__":
    g=GTA()
    g.save_frames()         # 切割GIF成圖片
    g.transform_imgtotxt()  # 將圖片轉成ASCII符號並保存為PKL文件
    g.dancing()             # 從PKL文件中讀取ASCII符號並顯示動畫
